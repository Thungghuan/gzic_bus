import os.path as path
from datetime import datetime
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

    campus = ["广州国际校区", "大学城校区", "五山校区"]

    start_campus = questionary.select("请选择起点", choices=campus).ask()
    end_campus = questionary.select(
        "请选择终点", choices=list(filter(lambda x: x != start_campus, campus))
    ).ask()

    today = datetime.today().strftime("%Y/%m/%d")
    date = questionary.text("请输入查询日期，格式为：yyyy/mm/dd".format(today), default=today).ask()

    bus_list = bus.get_bus_list(start_campus, end_campus, date)
    bus_choices = []

    if len(bus_list) > 0:
        for idx, bus in enumerate(bus_list):
            bus_choices.append(
                {
                    "name": "{}. {}-{}".format(
                        idx + 1, bus["startDate"], bus["endDate"]
                    ),
                    "value": idx,
                    "disabled": bus["tickets"] == 0,
                }
            )

        bus_idx = questionary.select(
            "请选择班次（灰色为被预约完的班次）：",
            choices=bus_choices,
            style=questionary.Style(
                [
                    ("disabled", "#858585 italic"),
                ]
            )
        ).ask()

        print(bus_list[bus_idx])

    else:
        print("{}已经没有校巴了".format(date))


if __name__ == "__main__":
    main()
