import re
import requests
from api.des import str_enc


# TODO: QR_code
# 1. generate qrcode: qrcode.makeCode("https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx39f121ed798af736&redirect_uri=https%3A%2F%2Fsso.scut.edu.cn%2Fcas%2Fscutwxsso&response_type=code&scope=snsapi_base&state="+uuid+"#wechat_redirect");
# 2. check scan "https://sso.scut.edu.cn/cas/scutqqcheck?uuid=" + uuid, get token
# 3. window.location.href="qRCode?token="+token+"&"+queryString; redirect with token, get tickie from headers.Location
# 4. now can get token of gzic_bus
# 5. qrcode expired in 2min
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

        captcha_page = self.session.post(url="https://sso.scut.edu.cn/cas/login", data=login_post_param)

        need_captcha = True
        if "PM1" in captcha_page.text:
            return need_captcha, lt
        else:
            return False, None

    # TODO: CAPTCHA
    # 1. wait for input captcha manually
    # 2. login again and get token
    def relogin(self, username: str, password: str, captcha: str, lt: str):
        login_post_param = {
            "PM1": captcha,
            "ul": len(username),
            "pl": len(password),
            "lt": lt,
            "rsa": str_enc(username + password + lt, "1", "2", "3"),
            "execution": "e1s2",
            "_eventId": "submit",
        }

        login_page = self.session.post(url="https://sso.scut.edu.cn/cas/login", data=login_post_param)
        
        return "PM1" not in login_page
    
    def get_token(self):
        # Post first, then can get the token
        self.session.post("https://life.gzic.scut.edu.cn/auth/login/cas/token")
        token = self.session.get("https://life.gzic.scut.edu.cn/auth/login/cas/token").json()

        return token["data"]


# TODO: error username/password/captcha handler
def get_token(username: str, password: str):

    # A fake user agent
    user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2"

    session = requests.session()
    session.trust_env = False
    session.headers["User-Agent"] = user_agent

    # This will be rediect to the login page
    redirect_login_page = session.get("https://life.gzic.scut.edu.cn/")

    # TODO: QR_code
    # 1. generate qrcode: qrcode.makeCode("https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx39f121ed798af736&redirect_uri=https%3A%2F%2Fsso.scut.edu.cn%2Fcas%2Fscutwxsso&response_type=code&scope=snsapi_base&state="+uuid+"#wechat_redirect");
    # 2. check scan "https://sso.scut.edu.cn/cas/scutqqcheck?uuid=" + uuid, get token
    # 3. window.location.href="qRCode?token="+token+"&"+queryString; redirect with token, get tickie from headers.Location
    # 4. now can get token of gzic_bus
    # 5. qrcode expired in 2min

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

    captcha_page = session.post(url="https://sso.scut.edu.cn/cas/login", data=login_post_param)
    if "PM1" in captcha_page.text:
        # TODO: CAPTCHA
        # 1. wait for input captcha manually
        # 2. login again and get token

        # Actually it's the same as before
        lt_pattern = re.compile(r'<input.+name="lt"\s+value="([^"]+)"')
        lt = re.search(lt_pattern, captcha_page.text).group(1)

        captcha = input("请输入验证码：")
        login_post_param = {
            "PM1": captcha,
            "ul": len(username),
            "pl": len(password),
            "lt": lt,
            "rsa": str_enc(username + password + lt, "1", "2", "3"),
            "execution": "e1s2",
            "_eventId": "submit",
        }

        _login_page = session.post(url="https://sso.scut.edu.cn/cas/login", data=login_post_param)

    # Post first, then can get the token
    session.post("https://life.gzic.scut.edu.cn/auth/login/cas/token")
    token = session.get("https://life.gzic.scut.edu.cn/auth/login/cas/token").json()

    return token["data"]


def check_token_expired(token):
    user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2"

    session = requests.session()
    session.trust_env = False
    session.headers["User-Agent"] = user_agent
    session.headers["authorization"] = token

    result = session.get(
        "https://life.gzic.scut.edu.cn/commute/open/commute/commuteOrder/orderFindAll?status=0&PageNum=1&PageSize=1"
    ).json()

    if "code" in result:
        code = result["code"]
    elif "status" in result:
        code = result["status"]
    else:
        code = -1

    return code != 200
