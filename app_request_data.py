'''Get the last price of a ticker.
The threading is added to keep API connection separate and avoid blocking.
Application class created to separate IB data functions from our script functions.
'''
# Import EClient for outgoing requests and EWrapper for incoming messages
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time

# Class for IB connection 
class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
    # Overwrite EWrapper function tickPrice to pass the output to our app
    def tickPrice(self, reqId, tickType, price, attrib):
        #app.on_tick_update(reqId, tickType, price, attrib)
        print(price)

    def historicalData(self, reqId, bar):
        print(f'Time: {bar.date} Close: {bar.close}')

    def realtimeBar(self, reqId, date, open_, high, low, close, volume, wap,count):
        app.on_bar_update(reqId, date, open_, high, low, close, volume, wap,count)
        print(close)

# Script logic
class Application():
    ib = None
    def __init__(self):
        # Initiate the connection
        self.ib = IBapi()
        self.ib.connect('127.0.0.1', 7497, 123)
        
        # Start the socket in a thread
        api_thread = threading.Thread(target=self.run_loop, daemon=True)
        api_thread.start()
        time.sleep(1) #sleep interval to allow time for connection to server
        
        # Get symbol info
        symbol = 'AAPL'
        contract = Contract()
        contract.symbol = symbol.upper()
        contract.secType = 'STK'
        contract.exchange = 'SMART'
        contract.currency = 'USD'
        
        # Request market tick data
        #self.ib.reqMktData(1, contract, '', False, False, [])
        # Request 5 sec Bar data
        self.ib.reqRealTimeBars(1, contract, 5, 'TRADES', 0, [])
        # Request market historical data
        #self.ib.reqHistoricalData(1, contract, '', '2 D', '1 hour', 'TRADES', 1, 2, False, [])
        
        # End the session when the app is done
        time.sleep(2) #sleep interval to allow time for incoming price data
        self.ib.disconnect()

    def run_loop(self):
        '''Run the main loop to start the session'''
        self.ib.run()

    def on_tick_update(self, reqId, tickType, price, attrib):
        '''Receive the price from EWrapper function tickPrice'''
        print(price if tickType == 2 and reqId == 1 else f'Wrong type {tickType} for request {reqId}')
    
    def on_bar_update(self, reqId, date, open_, high, low, close, volume, wap,count):
        '''Receive the price from EWrapper function realtimeBar'''
        print(close)

app = Application()