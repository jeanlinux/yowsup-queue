from yowsupqueue.stack import QueueStack

import configparser
import sys





if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    stack = QueueStack()
    stack.start(config)


