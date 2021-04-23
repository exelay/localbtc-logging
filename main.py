from time import sleep
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass

from loguru import logger

from loader import worksheet, lb_client, storage


@dataclass
class Order:
    date: str
    amount_btc: str
    amount_rub: str


class DataReceiver:
    data: Dict
    new_orders: List = []
    orders_count: int

    def __init__(self):
        self.orders_count = int(storage.get('orders_count')) if storage.get('orders_count') else 0

    def _get_order_list(self):
        self.data = lb_client.get_dashboard_released()

    def _separate_new_orders(self):
        new_orders_count = self.data['contact_count'] - self.orders_count
        if new_orders_count:
            logger.info(f'New orders count: {new_orders_count}')
            self.orders_count = self.data['contact_count']
            self.new_orders = self.data['contact_list'][:new_orders_count + 1]
            storage.set('orders_count', self.orders_count)

    def get_new_orders(self) -> List:
        self._get_order_list()
        self._separate_new_orders()
        logger.info('Getting new orders...')
        new_orders = list()
        for order in self.new_orders:
            date = datetime.fromisoformat(order['data']['released_at'])
            new_order = Order(
                date=date.strftime("%d.%m.%Y %H:%M"),
                amount_btc=order['data']['amount_btc'],
                amount_rub=order['data']['amount'],
            )
            new_orders.append(new_order)
        self.new_orders = []
        logger.info('New orders got.')
        return new_orders


class Writer:
    current_row: int

    def __init__(self):
        self.current_row = int(storage.get('current_row')) if storage.get('current_row') else 2

    def write_row(self, row_data: Order):
        logger.info('Writing row...')
        logger.debug(self.current_row)
        worksheet.update_value('A' + str(self.current_row), row_data.date)
        worksheet.update_value('B' + str(self.current_row), row_data.amount_btc)
        worksheet.update_value('C' + str(self.current_row), row_data.amount_rub)

        self.current_row += 1
        storage.set('current_row', self.current_row)
        logger.info('Row wrote.')


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
        self.data = []


if __name__ == '__main__':
    manager = Manager()
    logger.info('Start polling')
    while True:
        manager.check_new_data()
        if manager.data:
            manager.write_data()
        sleep(60)
