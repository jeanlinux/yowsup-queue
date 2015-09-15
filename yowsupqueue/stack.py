import queue
import threading

from yowsup.layers.network import YowNetworkLayer
from yowsup.layers import YowLayerEvent
from yowsup.stacks import YowStackBuilder
from yowsup.layers.auth import AuthError

from .layer import QueueLayer
from yowsupqueue.beanstalkstack import BeanstalkStack
#import Queue.Queue
#from Queue import queue
from axolotl.duplicatemessagexception import DuplicateMessageException

class QueueStack():
    def __init__(self):
        pass

    def start(self,config):


        yowsupConfig = config['Yowsup']
        credentials = (yowsupConfig["Username"], yowsupConfig["Password"])  # replace with your phone and password


        sendQueue = queue.Queue()






        stackBuilder = YowStackBuilder()
        self.stack = stackBuilder \
            .pushDefaultLayers(True) \
            .push(QueueLayer(sendQueue)) \
            .build()


        beanstalkdConfig = config['Beanstalkd']
        beanstalkdStack = BeanstalkStack()
        beanstalkdStack.setConnectParams(beanstalkdConfig["Host"], beanstalkdConfig["Port"],sendQueue,self.stack)

        beanstalkdStack.daemon = True
        beanstalkdStack.start()


        self.stack.setCredentials(credentials)
        connectEvent = YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT)
        self.stack.broadcastEvent(connectEvent)

        while 1:
            try:
                #self.stack.loop(timeout = 0.5, discrete = 0.5)
                self.stack.loop(timeout = 0.5)
            except AuthError as e:
                print("Auth Error, reason %s" % e)
            # Bugfix for : https://github.com/tgalal/yowsup/issues/978
            except DuplicateMessageException as e:
                print('Please delete .yowsup/<yournumber>/axolotl.db')
                break
                pass




