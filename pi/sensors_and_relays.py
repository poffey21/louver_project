from abc import abstractmethod, ABCMeta

from autobahn import wamp

class Component(metaclass=ABCMeta):
    """
    Generic component created.
    """

    @abstractmethod
    def badge(self):
        """
        For this particular component, the badge is what is returned.
        :return:
        """
        return None


class BadChannelException(BaseException):
    pass


class ReassignChannelException(BaseException):
    pass


class HardwareRegistry(object):
    __shared_state = {}
    VALID_CHANNELS = ['PSUIS_1', 'PSUIS_2', '0U70M_1', '0U70M_2']

    def __init__(self, hw_id, *assigned, **assigned_with_owners):
        self.__dict__ = self.__shared_state
        reassign_allowed = assigned_with_owners.pop('reassign_allowed', True)
        if not hasattr(self, 'assignments'):
            self.assignments = {}
        if hw_id not in self.assignments:
            self.assignments[hw_id] = {}

        if not reassign_allowed:
            for key in tuple(x for x in assigned_with_owners.keys()) + assigned:
                if key in self.assignments[hw_id].keys():
                    raise ReassignChannelException('Unable to reassign channel')

        if assigned or assigned_with_owners:
            self.assignments[hw_id].update(**assigned_with_owners)
            self.assignments[hw_id].update(**{x: 'no owner described' for x in assigned})


class SainsmartTwoChannelUSBRelay(object):
    """
    The Two Channel USB Relay built by Sainsmart.
    """
    __shared_state = {}
    DEFAULT_USB_ID = '16c0:05df'
    VALID_CHANNELS = ['PSUIS_1', 'PSUIS_2', '0U70M_1', '0U70M_2']
    registry = None
    usb_id = None
    channel = None

    def __init__(self, channel, **kwargs):
        if channel not in self.VALID_CHANNELS:
            raise BadChannelException('Unable to assign to bad channel')

        usb_id = kwargs.pop('usb_id', self.DEFAULT_USB_ID)
        self.registry = HardwareRegistry(usb_id, channel, reassign_allowed=False)
        self.usb_id = usb_id
        self.channel = channel

        # for key in assigned + tuple(x for x in assigned_with_owners.keys()):



        # if assigned or assigned_with_owners:
        #     self.assignments[usb_id].update(**assigned_with_owners)
        #     self.assignments[usb_id].update(**{x: 'no owner described' for x in assigned})

    def __str__(self):
        return '{}: {}'.format(self.usb_id, self.channel, )


class TemperatureSensor(object):
    """
    Allows you to read get updates on 
    """
