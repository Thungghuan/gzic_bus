from get_token import get_token
import os.path as path

print("gzic_bus / gzic校巴预约")

token = ""
print("读取token文件中...")

if path.exists("token"):
    with open("token") as f:
        token = f.read().strip()
        print("token读取成功")
else:
    print("请先使用统一认证账号登陆获取token")
    username = input("学号：")
    password = input("密码：")

    token = get_token(username, password)
    print("登陆成功，写入token文件")

    with open("token", "w+") as f:
        f.write(token)
