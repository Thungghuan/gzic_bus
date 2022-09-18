import re
import requests
from des import str_enc


def get_token(username: str, password: str):

    # A fake user agent
    user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2"

    session = requests.session()
    session.trust_env = False
    session.headers["User-Agent"] = user_agent

    # This will be rediect to the login page
    redirect_login_page = session.get("https://life.gzic.scut.edu.cn/")

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

    session.post(url="https://sso.scut.edu.cn/cas/login", data=login_post_param)

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

    return result["code"] != 200
