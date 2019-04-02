from datetime import datetime
import os
import webapp2
import jinja2
from google.appengine.ext import ndb


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Edit(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        name = self.request.get('name')
        mygpu_key = ndb.Key('Gpu', name)
        mygpu = mygpu_key.get()
        template_values = {
            'mygpu': mygpu

        }
        template = JINJA_ENVIRONMENT.get_template('edit.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        if action == 'update':
            name = self.request.get('name')
            mygpu_key = ndb.Key('Gpu', name)
            mygpu = mygpu_key.get()
            mygpu.manufacturer = self.request.get('manufacturer')
            mygpu.dateIssued = datetime.strptime(self.request.get('dateIssued'),  '%Y-%m-%d')
            mygpu.geometryShader = bool(self.request.get('geometryShader'))
            mygpu.tesselationShader = bool(self.request.get('tesselationShader'))
            mygpu.shaderInt16 = bool(self.request.get('shaderInt16'))
            mygpu.sparseBinding = bool(self.request.get('sparseBinding'))
            mygpu.textureCompressionETC2 = bool(self.request.get('textureCompressionETC2'))
            mygpu.vertexPipelineStoresAndAtomics = bool(self.request.get('vertexPipelineStoresAndAtomics'))




            mygpu.put()

            self.redirect('/')

        elif self.request.get('button') == 'Cancel':
            self.redirect('/')

