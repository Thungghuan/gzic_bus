import questionary
import os.path as path
import time
from api.get_token import check_token_expired, LoginSession

TOKEN_PATH = ".token"


def load_token(username=None, password=None):
    token = ""
    print("读取token文件中...")

    if path.exists(TOKEN_PATH):
        with open(TOKEN_PATH) as f:
            token = f.read().strip()

            if token == "" or check_token_expired(token):
                print("token过期")
                login(username, password)
            else:
                print("token读取成功")
    else:
        token = login(username, password)

    return token


def login(username=None, password=None):
    print("请先使用统一认证账号登陆获取token")
    useQRCode = questionary.select(
        "请选择登陆方式",
        choices=[
            {"name": "(1) 账号密码登录", "value": False},
            {"name": "(2) 二维码登录", "value": True},
        ],
    ).ask()

    login_sess = LoginSession()
    if useQRCode:
        qrcode_path, uuid = login_sess.gen_qrcode()
        print(f"请扫描二维码登录： {qrcode_path} (有效期2分钟)")

        start_time = round(time.time())
        while True:
            print(".", end="", flush=True)
            scan_status = login_sess.check_qrcode_scan(uuid)

            if scan_status:
                break
            else:
                curr_time = round(time.time())
                if curr_time - start_time > 120:
                    start_time = round(time.time())
                    qrcode_path, uuid = login_sess.gen_qrcode()
                    print("")
                    print("二维码过期，刷新二维码")
                else:
                    time.sleep(2)

    else:
        if not username or not password:
            username = questionary.text("学号：").ask()
            password = questionary.password("密码：").ask()

        if not username or not password:
            print("请输入用户名和密码")
            exit()

        need_captcha, lt = login_sess.login(username, password)

        if need_captcha:
            captcha = questionary.text("验证码：").ask()
            login_sess.relogin(username, password, captcha, lt)

    token = login_sess.get_token()
    print("登陆成功，写入token文件")

    with open(TOKEN_PATH, "w+") as f:
        f.write(token)

    return token
