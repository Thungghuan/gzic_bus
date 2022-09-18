import os.path as path
import questionary
from get_token import get_token, check_token_expired
from bus import Bus


def login():
    print("请先使用统一认证账号登陆获取token")
    username = questionary.text("学号：").ask()
    password = questionary.password("密码：").ask()

    if not username or not password:
        print("请输入用户名和密码")
        exit()

    token = get_token(username, password)
    print("登陆成功，写入token文件")

    with open("token", "w+") as f:
        f.write(token)


def main():

    print("gzic_bus / gzic校巴预约")

    token = ""
    print("读取token文件中...")

    if path.exists("token"):
        with open("token") as f:
            token = f.read().strip()

            if check_token_expired(token):
                print("token过期")
                login()
            else:
                print("token读取成功")
    else:
        login()

    bus = Bus(token)
    print(bus.list_reserve())


if __name__ == "__main__":
    main()
