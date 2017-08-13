from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import *

import threading


# Create your app class
class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        
        # CONNECTION OPTIONS
        self.socket_port = 7497  # Gateway: 4002; Workstation: 7496
        self.ip_address = "127.0.0.1"
        self.client_id = 0

        self.connect(self.ip_address, self.socket_port, clientId=self.client_id)  # Connect to server
        print(f"serverVersion:{self.serverVersion()} connectionTime:{self.twsConnectionTime()}")  # Check connection

    # Override wrapper methods (wrapper methods receive information from server; 
    # check wrapper class for all available methods)
    def position(self, account: str, contract: Contract, position: float,
                 avgCost: float):
        """This event returns real-time positions for all accounts in
        response to the reqPositions() method."""

        super().position(account, contract, position, avgCost)
        print("Position.", account, "Symbol:", contract.symbol, "SecType:",
              contract.secType, "Currency:", contract.currency,
              "Position:", position, "Avg cost:", avgCost)

    # This is the loop which will be running parallel to the scanner receiving information from the server.
    # This is where the logic of your app goes
    def loop(self):
        usr_in = input('\nWhat to do next?')
        while usr_in != 'exit':
            usr_in = input('What to do next?')
            if usr_in == 'p':
                self.reqPositions()


def main():
    app = TestApp()  # Initialize your app

    reader_thread = threading.Thread(target=app.run)  # Initialize a thread which will run the client class run() method
    loop_thread = threading.Thread(target=app.loop)  # Initialize a thread which will run the logic of your app

    # Start both threads
    reader_thread.start()
    loop_thread.start()

if __name__ == '__main__':
    main()
