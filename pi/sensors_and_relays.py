from autobahn import wamp

class SainsmartTwoChannelUSBRelay(object):
    """
    The USB Relay built by Sainsmart.
    """
    @wamp.register(u'com.ten08.louvre.toggle')
    def toggle(self, x, y):
        return x + y


class TemperatureSensor(object):
    """
    Allows you to read get updates on 
    """
    
    @wamp.register(u'com.ten08.louvre.temperature')
    def get_temperature(self):
        return 75