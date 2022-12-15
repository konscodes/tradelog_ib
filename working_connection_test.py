'''Test for connectivity
'''
# Import EClient for outgoing requests and EWrapper for incoming messages
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import time

# Initiate the class for connection 
class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

# Test the connection
app = IBapi()
app.connect('127.0.0.1', 7497, 123)

# Run the script
app.run()

# End the session when the app is done
time.sleep(2)
app.disconnect()