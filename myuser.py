from google.appengine.ext import ndb
from gpu import Gpu


class MyUser(ndb.Model):
    username = ndb.StringProperty()
    details = ndb.StructuredProperty(Gpu, repeated=True)

