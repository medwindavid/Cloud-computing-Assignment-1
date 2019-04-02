import os

import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb


from gpu import Gpu

from myuser import MyUser

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Find(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()

        if user == None:
            template_values = {
                'login_url': users.create_login_url(self.request.uri)
            }
            template = JINJA_ENVIRONMENT.get_template('mainpage.html')
            self.response.write(template.render(template_values))
            return

        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        if myuser == None:
            myuser = MyUser(id=user.user_id())
            myuser.put()

        gpu_query = Gpu().query().fetch()

        template_values = {
            'logout_url': users.create_logout_url(self.request.uri),
            'details': gpu_query
        }
        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        action = self.request.get('button')
        if action == 'Search':
            geometryShader = bool(self.request.get('geometryShader'))
            tesselationShader = bool(self.request.get('tesselationShader'))
            shaderInt16 = bool(self.request.get('shaderInt16'))
            sparseBinding = bool(self.request.get('sparseBinding'))
            textureCompressionETC2 = bool(self.request.get('textureCompressionETC2'))
            vertexPipelineStoresAndAtomics = bool(self.request.get('vertexPipelineStoresAndAtomics'))

            gpu_list = Gpu.query()

            if geometryShader:
                gpu_list = gpu_list.filter(Gpu.geometryShader == True)

            if tesselationShader:
                gpu_list = gpu_list.filter(Gpu.tesselationShader == True)

            if shaderInt16:
                gpu_list = gpu_list.filter(Gpu.shaderInt16 == True)

            if sparseBinding:
                gpu_list = gpu_list.filter(Gpu.sparseBinding == True)

            if textureCompressionETC2:
                gpu_list = gpu_list.filter(Gpu.textureCompressionETC2 == True)

            if vertexPipelineStoresAndAtomics:
                gpu_list = gpu_list.filter(Gpu.vertexPipelineStoresAndAtomics == True)

            for i in gpu_list:
                self.response.write(i.name + '<br/>')
