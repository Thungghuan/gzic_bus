import os
import re
import requests
from urllib.parse import quote
from api.des import str_enc


class LoginSession:
    user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2"

    def __init__(self):
        session = requests.session()
        session.trust_env = False
        session.headers["User-Agent"] = self.user_agent

        self.session = session

    def login(self, username: str, password: str):
        # This will be rediect to the login page
        redirect_login_page = self.session.get("https://life.gzic.scut.edu.cn/")

        lt_pattern = re.compile(r'<input.+name="lt"\s+value="([^"]+)"')
        lt = re.search(lt_pattern, redirect_login_page.text).group(1)

        login_post_param = {
            "ul": len(username),
            "pl": len(password),
            "lt": lt,
            "rsa": str_enc(username + password + lt, "1", "2", "3"),
            "execution": "e1s1",
            "_eventId": "submit",
        }

        captcha_page = self.session.post(
            url="https://sso.scut.edu.cn/cas/login", data=login_post_param
        )

        need_captcha = True
        if "PM1" in captcha_page.text:
            return need_captcha, lt
        else:
            return False, None

    def relogin(self, username: str, password: str, captcha: str, lt: str):
        """#CAPTCHA
        1. wait for input captcha manually
        2. login again and get token
        """

        login_post_param = {
            "PM1": captcha,
            "ul": len(username),
            "pl": len(password),
            "lt": lt,
            "rsa": str_enc(username + password + lt, "1", "2", "3"),
            "execution": "e1s2",
            "_eventId": "submit",
        }

        login_page = self.session.post(
            url="https://sso.scut.edu.cn/cas/login", data=login_post_param
        )

        return "PM1" not in login_page

    def gen_uuid(self):
        import time
        import random

        ts = round(time.time() * 1000)
        uuid = ""
        for ch in "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx":
            r = int((ts + random.random() * 16) % 16)
            if ch == "x":
                uuid += hex(r)[2:]
                ts //= 16
            elif ch == "y":
                uuid += hex(r & 0x3 | 0x8)[2:]
                ts //= 16
            else:
                uuid += ch

        return uuid

    def gen_qrcode(self):
        """# QR_code
        1. generate qrcode: qrcode.makeCode("https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx39f121ed798af736&redirect_uri=https%3A%2F%2Fsso.scut.edu.cn%2Fcas%2Fscutwxsso&response_type=code&scope=snsapi_base&state="+uuid+"#wechat_redirect");
        2. check scan "https://sso.scut.edu.cn/cas/scutqqcheck?uuid=" + uuid, get token
        3. window.location.href="qRCode?token="+token+"&"+queryString; redirect with token, get tickie from headers.Location
        4. now can get token of gzic_bus
        5. qrcode expired in 2min
        """

        import qrcode

        uuid = self.gen_uuid()
        url = (
            "https://open.weixin.qq.com/connect/oauth2/authorize"
            + "?appid=wx39f121ed798af736"
            + f"&redirect_uri={quote('https://sso.scut.edu.cn/cas/scutwxsso', safe='')}"
            + "&response_type=code"
            + "&scope=snsapi_base"
            + f"&state={uuid}"
            + "#wechat_redirect"
        )

        login_qrcode = qrcode.QRCode(box_size=2)
        login_qrcode.add_data(url)
        qrcode_img = login_qrcode.make_image()

        save_path = os.path.join(os.getcwd(), "qrcode.jpg")
        qrcode_img.save(save_path)

        return save_path, uuid

    def check_qrcode_scan(self, uuid):
        url = "https://sso.scut.edu.cn/cas/scutqqcheck?uuid=" + uuid
        result = self.session.get(url)

        resp_pattern = re.compile(r'null\("(..+)"\)')
        token_match = re.search(resp_pattern, result.text)
        if token_match:
            token = token_match[1]
            self.session.get(
                "https://sso.scut.edu.cn/cas/qRCode"
                + f"?token={token}"
                + f"&service={quote('https://life.gzic.scut.edu.cn/login/cas/', safe='')}"
            )

            return True
        else:
            return False

    def get_token(self):
        # Post first, then can get the token
        self.session.post("https://life.gzic.scut.edu.cn/auth/login/cas/token")
        token = self.session.get(
            "https://life.gzic.scut.edu.cn/auth/login/cas/token"
        ).json()

        return token["data"]


def check_token_expired(token):
    user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2"

    session = requests.session()
    session.trust_env = False
    session.headers["User-Agent"] = user_agent
    session.headers["authorization"] = token

    result = session.get("https://life.gzic.scut.edu.cn/auth/info").json()

    try:
        print(result["msg"])
        return result["code"] != 200
    except:
        return True
