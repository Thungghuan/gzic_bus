from unittest import result
import requests


class Bus:
    def __init__(self, token) -> None:
        user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2"

        session = requests.session()
        session.headers["User-Agent"] = user_agent
        session.headers["authorization"] = token
        session.headers["Content-Type"] = "application/json"

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

    def cancel_ticket(self, ticket_id):
        url = "{}/commuteOrder/cancelTicket?id={}".format(self.base_url, ticket_id)

        result = self.session.get(url).json()

        return result

    def delete_ticket(self, ticket_id):
        url = "{}/commuteOrder/removeOrderCanal?id={}".format(self.base_url, ticket_id)

        result = self.session.get(url).json()

        return result

    def get_bus_list(self, start_campus, end_campus, date):
        url = self.base_url + "/commuteOrder/frequencyChoice?PageNum=0&PageSize=0"

        data = {
            "startDate": date,
            "startCampus": start_campus,
            "endDate": date,
            "endCampus": end_campus,
            "startHsTime": "00:00",
            "endHsTime": "23:59",
        }

        result = self.session.post(url, json=data).json()

        return result["list"]

    def reserve_bus(self, tickets):
        url = self.base_url + "/commuteOrder/submitTicket"

        result = self.session.post(url, json=tickets).json()

        return result

    def qrcode_data(self, ticket_id):
        result = self.ticket_detail(ticket_id)["data"]

        return {"id": result["id"], "frequencyId": result["frequencyId"]}
