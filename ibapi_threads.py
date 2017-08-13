from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import *

import threading
import time


# Create your app class
class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)

        # CONNECTION OPTIONS
        self.socket_port = 7497  # Gateway: 4002; Workstation: 7496
        self.ip_address = "127.0.0.1"
        self.client_id = 0

        # APP VARS
        self.account = None  # Stores account number
        self.reqID = None  # Used to store the next valid server request id

        self.connect(self.ip_address, self.socket_port, clientId=self.client_id)  # Connect to server
        print(f"serverVersion:{self.serverVersion()} connectionTime:{self.twsConnectionTime()}")  # Check connection

    # OVERRIDEN WRAPPER METHODS (wrapper methods receive information from server;
    # check wrapper class for all available methods)

    def position(self, account: str, contract: Contract, position: float,
                 avgCost: float):
        """This event returns real-time positions for all accounts in
        response to the reqPositions() method."""

        super().position(account, contract, position, avgCost)
        print("Position.", account, "Symbol:", contract.symbol, "SecType:",
              contract.secType, "Currency:", contract.currency,
              "Position:", position, "Avg cost:", avgCost)

    def nextValidId(self, orderId: int):
        """ Receives next valid order id. This is triggered once upon connection to server and
            is received when the run function is called."""

        self.reqID = orderId

    def managedAccounts(self, accountsList: str):
        """Receives a comma-separated string with the managed account ids. This is triggered
           once upon connection to server and is received when the run function is called."""

        self.account = accountsList.split(',')[0]  # Exctract the acc number from the comma-delimited list

    # OTHER METHODS

    # This is the loop which will be running parallel to the scanner receiving information from the server.
    # This is where the logic of your app goes
    def loop(self):

        # This makes sure we receive the account number and next valid request id
        # both of which are not used in this script, but might be useful for more advanced things
        # like passing orders etc.
        time.sleep(2)

        # USER MENU

        while True:
            time.sleep(2) # To allow server messages to be printed out
            usr_in = input('\nWhat to do next? (p for open positions):')
            if usr_in == 'p':
                self.reqPositions()

    # Used to increment the id used to make requests to the server
    def increment_id(self):
        self.reqID += 1


def main():
    app = TestApp()  # Initialize your app

    reader_thread = threading.Thread(target=app.run)  # Initialize a thread which will run the client class run() method
    loop_thread = threading.Thread(target=app.loop)  # Initialize a thread which will run the logic of your app

    # Start both threads
    reader_thread.start()
    loop_thread.start()


if __name__ == '__main__':
    main()
