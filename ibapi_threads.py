from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.order import Order

import threading
import time


class IBApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)  # Instantiate a wrapper object
        EClient.__init__(self, wrapper=self)  # Instantiate a client object

        # CONNECTION OPTIONS

        self.socket_port = 7497  # Gateway: 4002; Workstation: 7497
        self.ip_address = "127.0.0.1"
        self.client_id = 0

        # APP VARIABLES

        self.reqID = None  # Stores the next valid request id
        self.account = None  # Stores the account number

        # CONNECT TO SERVER

        self.connect(self.ip_address, self.socket_port, clientId=self.client_id)  # Connect to server
        print(f"serverVersion:{self.serverVersion()} connectionTime:{self.twsConnectionTime()}\n")  # Check connection

    # WRAPPER OVERRIDEN METHODS

    def nextValidId(self, orderId:int):
        """ Receives next valid order id. This function is called by the server upon connection
        and the information is received upon calling the run function."""

        self.reqID = orderId  # Assign the received id to the app variable

    def managedAccounts(self, accountsList:str):
        """Receives a comma-separated string with the managed account ids. This function is called
        by the server upon connection and the information is received upon calling the run funtion."""

        self.account = accountsList.split(',')[0]  # Get the first item of the comma-delimited list

    # OTHER METHODS

    def loop(self):
        """Loop containing the app logic."""

        # This makes sure we receive the account number and next valid request id
        # both of which are not used in this script, but might be useful for more advanced things
        # like passing orders etc.
        time.sleep(2)

        while True:
            usr_in = input('What do? (o for order, d for data:')  # Collect user input
            if usr_in == 'o':
                contract = self.create_contract('TSLA')  # Create a contract
                order = self.create_order('BUY', 5)  # Create an order

                self.increment_id()  # Increment the order id
                self.placeOrder(self.reqID, contract, order)  # Place an order
            elif usr_in == 'd':
                contract = self.create_contract('TSLA')  # Create a contract
                self.increment_id()  # Increment the order id
                self.reqMktData(self.reqID, contract, '', True, False, [])  # Request the market data

            time.sleep(2)  # Allows for all server messages to be delivered before going into the loop again

    def increment_id(self):
        """ Increments the request id"""

        self.reqID += 1

    def create_contract(self, symbol):
        """ Creates an IB contract."""

        contract = Contract()
        contract.symbol = symbol
        contract.exchange = 'SMART'
        contract.secType = 'STK'
        contract.currency = 'USD'

        return contract

    def create_order(self, action, quantity):
        """ Creates an IB order."""

        order = Order()
        order.action = action
        order.totalQuantity = quantity
        order.account = self.account
        order.orderType = 'MKT'
        self.increment_id()
        order.orderId = self.reqID

        return order


def main():
    app = IBApp()  # Initialize your app

    reader_thread = threading.Thread(target=app.run)  # Initialize a thread which will run the client class run() method
    loop_thread = threading.Thread(target=app.loop)  # Initialize a thread which will run the logic of your app

    # Start both threads
    reader_thread.start()
    loop_thread.start()


if __name__ == '__main__':
    main()
