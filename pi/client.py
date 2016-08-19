"""
This client will continually be connected to the
crossbar server.

When it is disconnected... we go ahead and startup
the hotspot_server.
"""

try:
    import asyncio
except ImportError:
    # Trollius >= 0.3 was renamed
    import trollius as asyncio

from os import environ
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp import ApplicationError


class Component(ApplicationSession):
    """
    An application component that reports its current name, enables name changes,
    """
    name = 'pi_zero'

    @asyncio.coroutine
    def onJoin(self, details):

        def on_new_name(name):
            """
            Enable name changes
            """
            self.name = name
            self.log.info("Changing name to {}".format(name))
            self.publish('com.example.ongoodbye', [self.name])
            self._unregister('com.ten08.louver.{}.new_name'.format(self.name))
            self.register(on_new_name, 'com.ten08.louver.{}.new_name'.format(self.name))
            self.publish('com.example.onhello', [name])

        # Register function so we can change our name
        self.register(on_new_name, 'com.ten08.louver.{}.new_name'.format(self.name))

        # Publish name
        self.publish('com.example.onhello', [self.name])


        try:
            # li = yield self.call("com.ten08.louver.iot_devices")
            # print(li)
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
        """
        Remove your name from the list of devices
        """
        self.publish('com.example.ongoodbye', [self.name]);






if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get('AUTOBAHN_ROUTER', u'ws://127.0.0.1:8080/ws'),
        u'realm1'
    )
    runner.run(Component)
