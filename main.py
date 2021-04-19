from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass

from loader import worksheet, lb_client


@dataclass
class Order:
    date: str
    amount_btc: str
    amount_rub: str


class DataReceiver:
    data: Dict
    new_orders: List
    orders_count = 0

    def _get_order_list(self):
        self.data = lb_client.get_dashboard_released()

    def _separate_new_orders(self):
        new_orders_count = self.data['contact_count'] - self.orders_count
        if new_orders_count:
            self.orders_count = self.data['contact_count']
            self.new_orders = self.data['contact_list'][:new_orders_count + 1]

    def get_new_orders(self) -> List:
        self._get_order_list()
        self._separate_new_orders()

        new_orders = list()
        for order in self.new_orders:
            date = datetime.fromisoformat(order['data']['released_at'])
            new_order = Order(
                date=date.strftime("%d.%m.%Y %H:%M"),
                amount_btc=order['data']['amount_btc'],
                amount_rub=order['data']['amount'],
            )
            new_orders.append(new_order)
        return new_orders


class Writer:
    current_row: int = 2

    def write_row(self, row_data: Order):
        worksheet.update_value('A' + str(self.current_row), row_data.date)
        worksheet.update_value('B' + str(self.current_row), row_data.amount_btc)
        worksheet.update_value('C' + str(self.current_row), row_data.amount_rub)
        self.current_row += 1


class Manager:
    data: List
    receiver: DataReceiver
    writer: Writer

    def __init__(self):
        self.receiver = DataReceiver()
        self.writer = Writer()

    def check_new_data(self):
        self.data = self.receiver.get_new_orders()

    def write_data(self):
        for order in self.data:
            self.writer.write_row(order)


if __name__ == '__main__':
    manager = Manager()
    while True:
        manager.check_new_data()
        if manager.data:
            manager.write_data()
