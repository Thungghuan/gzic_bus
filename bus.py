import requests


class Bus:
    def __init__(self, token) -> None:
        user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2"

        session = requests.session()
        session.headers["User-Agent"] = user_agent
        session.headers["authorization"] = token

        self.session = session
        self.base_url = "https://life.gzic.scut.edu.cn/commute/open/commute"

    def list_reserve(self, status=0, page_num=1, page_size=8):
        url = "{}/commuteOrder/orderFindAll?status={}&PageNum={}&PageSize={}".format(
            self.base_url, status, page_num, page_size
        )

        result = self.session.get(url).json()

        return result

    def ticket_detail(self, ticket_id):
        url = "{}/commuteOrder/ticketDetail?id={}".format(self.base_url, ticket_id)

        result = self.session.get(url).json()

        return result

    def get_bus_list(self, page_num=0, page_size=0):
        url = "{}/commuteOrder/frequencyChoice?PageNum={}&PageSize={}".format(
            self.base_url, page_num, page_size
        )

        data = {
            "endCampus": "大学城校区",
            "endDate": "2022/09/25",
            "startDate": "2022/09/18",
            "startCampus": "广州国际校区",
            "startHsTime": "00:00",
            "endHsTime": "23:59",
        }

        result = self.session.post(url, data).json()

        return result

    def reserve_bus(self):
        url = "{}/commuteOrder/submitTicket"

        data = [
            {
                "ids": "17501,17502",
                "dateDeparture": "2022/09/19",
                "startDate": "07:10",
                "endDate": "07:35",
                "startLocation": "国际校区D5",
                "downtown": "大学城校区音乐厅",
                "tickets": 1,
                "ischecked": True,
                "subTickets": 1,
            }
        ]

        result = self.session.post(url, data).json()

        return result
