

try:
    import asyncio
except ImportError:
    # Trollius >= 0.3 was renamed
    import trollius as asyncio

from os import environ
from autobahn import wamp
from autobahn.asyncio.wamp import ApplicationSession
from autobahn.asyncio.wamp import ApplicationRunner
from autobahn.wamp import ApplicationError

from sensors_and_relays import SainsmartTwoChannelUSBRelay
from sensors_and_relays import TemperatureSensor

class Device(ApplicationSession):
    """
    This signifies a Raspberry Pi device which will have 
    multiple types of connectors.
    """
    
    @asyncio.coroutine
    def onJoin(self, details):

        # register all methods on this object decorated with "@wamp.register"
        # as a RPC endpoint
        ##
        results = yield from self.register(self)
        for res in results:
            if isinstance(res, wamp.protocol.Registration):
                # res is an Registration instance
                print("Ok, registered procedure with registration ID {}".format(res.id))
            else:
                # res is an Failure instance
                print("Failed to register procedure: {}".format(res))
        
        self.publish('com.example.onhello', self.name)
    
    def onLeave(self, details):
        """
        Remove your name from the list of devices
        """
        self.publish('com.example.ongoodbye', self.name);

    def onDisconnect(self):
        asyncio.get_event_loop().stop()

        
class PiZero(Device):
    """
    This is the device that we'll eventually setup.  
    """
    name = "ffw09D32eqoa"
    devices = []

    def __init__(self):
        light_switch = SainsmartTwoChannelUSBRelay()

if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get('AUTOBAHN_ROUTER', u'ws://127.0.0.1:8080/ws'),
        u'realm1'
    )
    runner.run(PiZero)