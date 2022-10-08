from enum import Enum
from datetime import datetime
import questionary
from bus import Bus


class ReserveState(Enum):
    START_CAMPUS = 1
    END_CAMPUS = 2
    DATE = 3
    TIME = 4
    CONFIRM = 5
    END = 6


class ReserveBus:
    default_date = datetime.today().strftime("%Y/%m/%d")
    start_campus = ""
    end_campus = ""
    date = ""
    ticket = {}

    def __init__(self, bus: Bus) -> None:
        self.bus = bus
        self.state = ReserveState.START_CAMPUS
        self.change_state(ReserveState.START_CAMPUS)

    def change_state(self, state: ReserveState):
        self.state = state

        match state:
            case ReserveState.START_CAMPUS:
                self.set_start_campus()

            case ReserveState.END_CAMPUS:
                self.set_end_campus()

            case ReserveState.DATE:
                self.set_date()
            case ReserveState.TIME:
                self.set_time()

            case ReserveState.END:
                print(self.ticket)

    def set_start_campus(self):
        campus = ["广州国际校区", "大学城校区", "五山校区", "返回主菜单"]
        self.start_campus = questionary.select("请选择起点", choices=campus).ask()

        if self.start_campus != "返回":
            self.change_state(ReserveState.END_CAMPUS)
        else:
            self.change_state(ReserveState.END)

    def set_end_campus(self):
        campus = ["广州国际校区", "大学城校区", "五山校区", "返回"]
        self.end_campus = questionary.select(
            "请选择终点",
            choices=list(filter(lambda x: x != self.start_campus, campus)),
        ).ask()

        if self.end_campus != "返回":
            self.change_state(ReserveState.DATE)
        else:
            self.change_state(ReserveState.START_CAMPUS)

    def set_date(self):
        self.date = questionary.text(
            "请输入查询日期，格式为：yyyy/mm/dd", default=self.default_date
        ).ask()

        self.default_date = self.date
        self.change_state(ReserveState.TIME)

    def set_time(self):
        bus_list = self.bus.get_bus_list(self.start_campus, self.end_campus, self.date)
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

            bus_choices.append(
                {"name": "{}. 重选日期".format(len(bus_list) + 1), "value": -1}
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

            if bus_idx == -1:
                self.change_state(ReserveState.DATE)
            else:
                print("校巴完整信息：")
                print("ID: {}".format(bus_list[bus_idx]["ids"]))
                print("日期: {}".format(bus_list[bus_idx]["dateDeparture"]))
                print(
                    "时间: {}-{}".format(
                        bus_list[bus_idx]["startDate"],
                        bus_list[bus_idx]["endDate"],
                    )
                )
                print(
                    "起点-终点: {}-{}".format(
                        bus_list[bus_idx]["startLocation"],
                        bus_list[bus_idx]["downtown"],
                    )
                )

                choices = [
                    {"name": "是", "value": True},
                    {"name": "否", "value": False},
                ]
                is_confirm = questionary.select("确认预定", choices=choices).ask()

                if is_confirm:
                    self.ticket = bus_list[bus_idx]
                    self.change_state(ReserveState.END)
                else:
                    self.change_state(ReserveState.TIME)

        else:
            print("{}已经没有校巴了".format(self.date))

            choices = [
                {"name": "是", "value": True},
                {"name": "否", "value": False},
            ]
            is_confirm = questionary.select("是否重选日期", choices=choices).ask()

            if is_confirm:
                self.change_state(ReserveState.DATE)
            else:
                self.change_state(ReserveState.END)
