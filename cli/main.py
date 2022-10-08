from datetime import datetime
import questionary
from cli.console import clear, reset_console
from cli.token import load_token
from bus import Bus
from enum import Enum


class MenuState(Enum):
    START = 1
    RESERVE_BUS = 2
    CHECK_RESERVE = 3
    QUIT = 4


class Menu:
    state: MenuState

    def __init__(self) -> None:
        self.state = MenuState.START

        reset_console()
        self.token = load_token()
        self.bus = Bus(self.token)

    def run(self):
        self.start_menu()

    def start_menu(self):
        reset_console()

        menu = ["预约校巴", "查看已预约校巴", "退出"]
        choice_state = [
            MenuState.RESERVE_BUS,
            MenuState.CHECK_RESERVE,
            MenuState.QUIT,
        ]

        menu_choices = []
        for idx, choice in enumerate(menu):
            menu_choices.append(
                {
                    "name": "({}) {}".format(idx + 1, choice),
                    "value": idx,
                }
            )

        choice = questionary.select(
            "请选择功能：",
            choices=menu_choices,
        ).ask()

        print(menu[choice])
        self.change_state(choice_state[choice])

    def change_state(self, state: MenuState):
        self.state = state

        match state:
            case MenuState.START:
                self.start_menu()
            case MenuState.RESERVE_BUS:
                self.reserve_bus()
            case MenuState.CHECK_RESERVE:
                self.check_reserve()
            case MenuState.QUIT:
                self.quit()

    def reserve_bus(self):
        campus = ["广州国际校区", "大学城校区", "五山校区"]

        start_campus = questionary.select("请选择起点", choices=campus).ask()
        end_campus = questionary.select(
            "请选择终点", choices=list(filter(lambda x: x != start_campus, campus))
        ).ask()

        today = datetime.today().strftime("%Y/%m/%d")
        date = questionary.text(
            "请输入查询日期，格式为：yyyy/mm/dd".format(today), default=today
        ).ask()

        bus_list = self.bus.get_bus_list(start_campus, end_campus, date)
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
                ),
            ).ask()

            print(bus_list[bus_idx])

        else:
            print("{}已经没有校巴了".format(date))

        self.back_main_menu(True)

    def check_reserve(self):
        tickets = self.bus.list_reserve(status=1)["list"]
        ticket_choices = []

        for idx, bus in enumerate(tickets):
            ticket_choices.append(
                {
                    "name": "{}. {} {}".format(
                        idx + 1, bus["ruteName"], bus["startTime"]
                    ),
                    "value": idx,
                }
            )

        if len(ticket_choices) > 0:
            choice = questionary.select(
                "请选择班次：",
                choices=ticket_choices,
            ).ask()

            print(choice)
        else:
            print("没有找到预约的校巴哦")

        self.back_main_menu()

    def quit(self):
        print("88")

    def back_main_menu(self, last_page=False):
        if not last_page:
            choices = [
                {"name": "返回主菜单", "value": MenuState.START},
                {"name": "退出", "value": MenuState.QUIT},
            ]
        else:
            choices = [
                {"name": "返回主菜单", "value": MenuState.START},
                {"name": "重新选择", "value": self.state},
                {"name": "退出", "value": MenuState.QUIT},
            ]

        choice = questionary.select("请选择下一步操作", choices=choices).ask()

        self.change_state(choice)


def main():
    menu = Menu()
    menu.run()
