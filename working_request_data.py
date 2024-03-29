'''Get the last price of a ticker.
The threading is added to keep API connection separate and avoid blocking.
'''
# Import EClient for outgoing requests and EWrapper for incoming messages
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time

# Initiate the class for connection 
class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
    def tickPrice(self, reqId, tickType, price, attrib):
        if tickType == 2 and reqId == 1:
            print('The current ask price is: ', price)

def run_loop():
	app.run()

# Test the connection
app = IBapi()
app.connect('127.0.0.1', 7497, 123)

# Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()
time.sleep(1) #sleep interval to allow time for connection to server

# Create contract object
apple_contract = Contract()
apple_contract.symbol = 'AAPL'
apple_contract.secType = 'STK'
apple_contract.exchange = 'SMART'
apple_contract.currency = 'USD'

# Request Market Data
app.reqMktData(1, apple_contract, '', False, False, [])

# End the session when the app is done
time.sleep(10) #sleep interval to allow time for incoming price data
app.disconnect()