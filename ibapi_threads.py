from ibapi import wrapper
from ibapi.client import EClient
from ibapi.contract import *

import threading


class TestApp(wrapper.EWrapper, EClient):
    def __init__(self):
        wrapper.EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)

        self.connect("127.0.0.1", 7497, clientId=0)
        print(f"serverVersion:{self.serverVersion()} connectionTime:{self.twsConnectionTime()}")

    def position(self, account: str, contract: Contract, position: float,
                 avgCost: float):
        """This event returns real-time positions for all accounts in
        response to the reqPositions() method."""

        super().position(account, contract, position, avgCost)
        print("Position.", account, "Symbol:", contract.symbol, "SecType:",
              contract.secType, "Currency:", contract.currency,
              "Position:", position, "Avg cost:", avgCost)

    def loop(self):
        usr_in = input('What to do next?')
        while usr_in != 'exit':
            usr_in = input('What to do next?')
            if usr_in == 'p':
                self.reqPositions()


def main():
    app = TestApp()

    reader_thread = threading.Thread(target=app.run)
    loop_thread = threading.Thread(target=app.loop)

    reader_thread.start()
    loop_thread.start()

if __name__ == '__main__':
    main()
