from enum import Enum
import questionary
from api.bus import Bus


class CheckState(Enum):
    LIST = 1
    DETAIL = 2
    CANCEL = 3
    DELETE = 4
    QUIT = 5


class CheckReserveMenu:
    state = 0
    ticket = {}

    def __init__(self, bus: Bus) -> None:
        self.bus = bus
        self.change_state(CheckState.LIST)

    def run(self):
        while self.state != CheckState.QUIT:
            match self.state:
                case CheckState.LIST:
                    is_quit = self.list_tickets()

                    if is_quit:
                        return 1

                case CheckState.DETAIL:
                    self.get_ticket_detail()

                case CheckState.CANCEL:
                    self.cancel_ticket()

                case CheckState.DELETE:
                    self.delete_ticket()

        return 0

    def change_state(self, state: CheckState):
        self.state = state

    def list_tickets(self):
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

            ticket_choices.append(
                {
                    "name": "{}. 返回主菜单".format(len(tickets) + 1),
                    "value": -1,
                }
            )

            choice = questionary.select(
                "请选择班次：",
                choices=ticket_choices,
            ).ask()

            if choice == -1:
                self.change_state(CheckState.QUIT)
                return True

            else:
                self.ticket = tickets[choice]
                self.change_state(CheckState.DETAIL)
                
                return False

        else:
            print("没有找到预约的校巴哦")
            self.change_state(CheckState.QUIT)

            return False

    def get_ticket_detail(self):
        result = self.bus.ticket_detail(self.ticket["id"])["data"]

        print("校巴完整信息：")
        print("ID: {}".format(result["id"]))
        print("日期: {}".format(result["dateDeparture"]))
        print(
            "时间: {}-{}".format(
                result["startTime"],
                result["endTime"],
            )
        )
        print(
            "起点-终点: {}".format(
                result["ruteName"],
            )
        )
        print("车牌：{}".format(result["licensePlate"]))
        print("司机：{}".format(result["driverName"]))

        choices = [
            {"name": "返回", "value": CheckState.LIST},
            {"name": "取消本班次", "value": CheckState.CANCEL},
        ]
        next_state = questionary.select("请选择操作", choices=choices).ask()
        self.change_state(next_state)

    def cancel_ticket(self):
        choices = [
            {"name": "是", "value": True},
            {"name": "否", "value": False},
        ]
        is_confirm = questionary.select(
            "是否取消 {} {}".format(self.ticket["ruteName"], self.ticket["startTime"]),
            choices=choices,
        ).ask()

        if is_confirm:
            result = self.bus.cancel_ticket(self.ticket["id"])

            if result["code"] == 200:
                print("取消车票成功")
                self.change_state(CheckState.DELETE)
            else:
                print("取消车票失败，请重试")
                self.change_state(CheckState.LIST)
        else:
            self.change_state(CheckState.LIST)

    def delete_ticket(self):
        choices = [
            {"name": "是", "value": True},
            {"name": "否", "value": False},
        ]
        is_confirm = questionary.select(
            "是否删除记录 {} {}".format(self.ticket["ruteName"], self.ticket["startTime"]),
            choices=choices,
        ).ask()

        if is_confirm:
            self.bus.delete_ticket(self.ticket["id"])

        self.change_state(CheckState.QUIT)
