import questionary
from cli.check import CheckReserveMenu
from cli.console import reset_console
from cli.reserve import ReserveBusMenu
from cli.token import load_token
from api.bus import Bus
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
        while self.state != MenuState.QUIT:
            match self.state:
                case MenuState.START:
                    self.start_menu()
                case MenuState.RESERVE_BUS:
                    self.reserve_bus()
                case MenuState.CHECK_RESERVE:
                    self.check_reserve()

        self.quit()

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

        self.change_state(choice_state[choice])

    def change_state(self, state: MenuState):
        self.state = state

    def reserve_bus(self):
        reserve_menu = ReserveBusMenu(self.bus)
        result = reserve_menu.run()

        if result == 1:
            self.change_state(MenuState.START)

        else:
            self.back_main_menu()

    def check_reserve(self):
        check_reserve_menu = CheckReserveMenu(self.bus)
        result = check_reserve_menu.run()

        if result == 1:
            self.change_state(MenuState.START)

        else:
            self.back_main_menu()

    def quit(self):
        print("88")

    def back_main_menu(self):
        choices = [
            {"name": "返回主菜单", "value": MenuState.START},
            {"name": "退出", "value": MenuState.QUIT},
        ]
        choice = questionary.select("请选择下一步操作", choices=choices).ask()

        self.change_state(choice)


def main():
    menu = Menu()
    menu.run()


if __name__ == "__main__":
    main()
