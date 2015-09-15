from pystalkd.Beanstalkd import Connection
import json
import threading
import sys
import traceback

import queue
from yowsup.layers import YowLayerEvent
from yowsupqueue.layer import QueueLayer


class BeanstalkStack(threading.Thread):
    def setConnectParams(self, host, port, sendQueue,yowsUpStack):
        self.host = host
        self.port = port
        self.sendQueue = sendQueue
        self.yowsUpStack = yowsUpStack


    def run(self):
        self.beanstalk = Connection(host=self.host, port=int(self.port))
        self.beanstalk.watch('whatsapp-send')
        while 1:
            job = self.beanstalk.reserve(0.05)
            if not job is None:
                try:
                    messageBody = str(job.body)
                    message = json.loads(messageBody)
                    if message["type"] == "simple":
                        print(messageBody)
                        self.sendMessageToWhatsapp(message["address"], message["body"])
                    elif message["type"] == "image":
                        print(messageBody)
                        self.sendImage(message["address"], message["body"])
                    else:
                        raise Exception("Unrecognized Message: %s" % message)
                    print("Sucessfully sent Message")
                    job.delete()

                except Exception as e:
                    job.bury()
                    traceback.print_exc()
            try:
                messageToSend = self.sendQueue.get(True, 0.05)
                self.sendMessage2BeanStalkd(messageToSend)
            except queue.Empty as e:
                pass



    def sendMessage2BeanStalkd(self, message):
        self.beanstalk.use("whatsapp-receive")
        if type(message) is not str:
            message = json.dumps(message)
        self.beanstalk.put(message)
        pass

    def sendMessageToWhatsapp(self, number, msg):
        #self.output(msg)
        #self.output(number)
        self.yowsUpStack.broadcastEvent(YowLayerEvent(name=QueueLayer.EVENT_SEND_MESSAGE, msg=msg, number=number))

    def sendImage(self, number, path):
       self.yowsUpStack.broadcastEvent(YowLayerEvent(name=QueueLayer.EVENT_SEND_IMAGE, path=path, number=number))

