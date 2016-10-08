import ConfigParser


class Config(object):

    def __init__(self):
        config = ConfigParser.RawConfigParser()
        config.read('test.ini')

        self.options = dict(config.items('main'))
