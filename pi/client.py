"""
This client will continually be connected to the
crossbar server.

When it is disconnected... we go ahead and startup
the hotspot_server.
"""
from autobahn.wamp import ApplicationError

try:
    import asyncio
except ImportError:
    # Trollius >= 0.3 was renamed
    import trollius as asyncio

from os import environ
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner

class Component(ApplicationSession):
    """
    An application component that reports its current name, enables name changes,
    """
    name = 'pi_zero'

    @asyncio.coroutine
    def onJoin(self, details):

        self.publish('com.example.onhello', [self.name])

        def on_new_name(x):
            self.publish('com.example.ongoodbye', [self.name])
            self.name = x
            self.log.info("Changing name to {}".format(x))
            self.publish('com.example.onhello', [x])

        self.register(on_new_name, 'com.ten08.louver.zero.new_name')

        try:
            li = yield self.call("com.ten08.louver.iot_devices")
            print(li)
            li = yield self.call("wamp.session.list")
            print(li)
            # res = yield self.call('com.example.mul2', counter, 3)
            # self.log.info("mul2() called with result: {result}",
            #               result=res)
        except ApplicationError as e:
            # ignore errors due to the frontend not yet having
            # registered the procedure we would like to call
            if e.error != 'wamp.error.no_such_procedure':
                raise e


    def onLeave(self, details):
        self.publish('com.example.ongoodbye', [self.name]);






if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get('AUTOBAHN_ROUTER', u'ws://127.0.0.1:8080/ws'),
        u'realm1'
    )
    runner.run(Component)
