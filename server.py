from wsgiref.simple_server import make_server
from tg import expose, TGController, AppConfig
import pickle
from datetime import datetime, timedelta

EVENTS_CACHE = None
LAST_UPDATED = None
UPDATE_INTERVAL = timedelta(minutes=30)
def fetchEvents():
    global EVENTS_CACHE, LAST_UPDATED, UPDATE_INTERVAL

    def eventFilter(event):
        return event.start is not None and event.start >= datetime.today() \
            and event.location is not None \
            and event.coords is not None

    if EVENTS_CACHE is None or (LAST_UPDATED - datetime.now()) >= UPDATE_INTERVAL:
        with open('eventobjs.dat', 'rb') as f:
            events = pickle.load(f)
            events = [event.__dict__ for event in events if eventFilter(event)]
            EVENTS_CACHE = events
            LAST_UPDATED = datetime.now()

    return EVENTS_CACHE

class RootController(TGController):
    @expose('index.jinja')
    def index(self):
        return dict()

    @expose("json")
    def getEvents(self):
        return dict(events=fetchEvents())

config = AppConfig(minimal=True, root_controller=RootController())
config.renderers = ['jinja']
config.serve_static = True
config.paths['static_files'] = 'static'
httpd = make_server('', 8080, config.make_wsgi_app())
httpd.serve_forever()
