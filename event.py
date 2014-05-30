class Event(object):
    __slots__=('name', 'start', 'end', 'location')

    def __init__(self):
        self.name = None
        self.start = None
        self.end = None
        self.location = None

    def __str__(self):
        return 'Name:\t\t%s\nStart:\t\t%s\nEnd:\t\t%s\nLocation:\t%s' % (self.name, self.start, self.end, self.location)
