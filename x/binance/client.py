import logging
from binance.spot import Spot
from binance.lib.utils import config_logging
from binance.error import ClientError


class Client:
	def __init__(self, api_key: str, secret_key: str):
		self.client = Spot(key=api_key, secret=secret_key, base_url="https://api.binance.com")


	# weight: 10
	def get_account_info(self):
		try:
			res = self.client.account()
			logging.info(res)
		except ClientError as error:
			logging.error("get_account_info error. status: {}, error code: {}, error message: {}".format(error.status_code, error.error_code, error.error_message))


	# weight: 1
	# need to add other time_in_force options(like FOK, IOC, ...)?
	def open_order(self, symbol: str, side: str, type: str, quantity: float, price: float):
		params = {
			"timeInForce": "GTC",
			"quantity": quantity,
			"price": price,
		}

		try:
			res = self.client.new_order(symbol, side, type, **params)
			logging.info(res)
		except ClientError as error:
			logging.error("open_order error. status: {}, error code: {}, error message: {}".format(error.status_code, error.error_code, error.error_message))


	# weight: 3 per symbol
	def get_all_open_orders(self, symbol: str):
		try:
			res = self.client.get_open_orders(symbol)
			logging.info(res)
		except ClientError as error:
			logging.error("get_all_open_orders error. status: {}, error code: {}, error message: {}".format(error.status_code, error.error_code, error.error_message))


	# weight: 1
	def cancel_order(self, symbol: str, order_id: int):
		try:
			if order_id > 0:
				params = {
                    "orderId": order_id
                }
				res = self.client.cancel_order(symbol, order_id)
			else:
				res = self.client.cancel_open_orders(symbol)
				
			logging.info(res)
		except ClientError as error:
			logging.error("cancel_order error. status: {}, error code: {}, error message: {}".format(error.status_code, error.error_code, error.error_message))

