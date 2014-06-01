class Event(object):
    def __init__(self):
        self.name = None
        self.start = None
        self.end = None
        self.location = None
        self.link = None

    def __str__(self):
        return 'Name:\t\t%s\nStart:\t\t%s\nEnd:\t\t%s\nLocation:\t%s\nLink:\t\t%s' % (self.name, self.start, self.end, self.location, self.link)
