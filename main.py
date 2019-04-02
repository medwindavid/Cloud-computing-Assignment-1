import os
import webapp2
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb

from datetime import datetime

from gpu import Gpu
from myuser import MyUser
from detail import Detail
from edit import Edit
from search import Find

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        if user == None:
            template_values = {
                'login_url': users.create_login_url(self.request.uri)
            }
            template = JINJA_ENVIRONMENT.get_template('mainpageguest.html')
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

        template = JINJA_ENVIRONMENT.get_template('mainpage.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        action = self.request.get('button')
        if action == 'Add GPU':
            name = self.request.get('name')
            manufacturer = self.request.get('manufacturer')
            dateIssued = datetime.strptime(self.request.get("dateIssued"), '%Y-%m-%d')
            geometryShader = self.request.get('geometryShader')== 'on'
            tesselationShader = self.request.get('tesselationShader')== 'on'
            shaderInt16 = self.request.get('shaderInt16') == 'on'
            sparseBinding = self.request.get('sparseBinding') == 'on'
            textureCompressionETC2 = self.request.get('textureCompressionETC2')== 'on'
            vertexPipelineStoresAndAtomics = self.request.get('vertexPipelineStoresAndAtomics')== 'on'

            options = Gpu.query()
            if geometryShader:
                options.filter(Gpu.geometryShader==True)

            if tesselationShader:
                options.filter(Gpu.tesselationShader==True)

            if shaderInt16:
                options.filter(Gpu.shaderInt16==True)

            if sparseBinding:
                options.filter(Gpu.sparseBinding==True)

            if textureCompressionETC2:
                options.filter(Gpu.textureCompressionETC2==True)

            if vertexPipelineStoresAndAtomics:
                options.filter(Gpu.vertexPipelineStoresAndAtomics==True)
            options = options.fetch()

            user = users.get_current_user()

            mygpu_key = ndb.Key('Gpu', name)
            mygpu = mygpu_key.get()

            mygpu.details.append(options)
            mygpu.put()
            template_values = {

                'options':options,
                'geometryShader':geometryShader,
                'tesselationShader' :tesselationShader,
                'shaderInt16':shaderInt16,
                'sparseBinding': sparseBinding,
                'textureCompressionETC2':textureCompressionETC2,
                'vertexPipelineStoresAndAtomics': vertexPipelineStoresAndAtomics
                 }

        template = JINJA_ENVIRONMENT.get_template('mainpage.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        action = self.request.get('button')
        if action == 'Add GPU':
            name = self.request.get('name')
            manufacturer = self.request.get('manufacturer')
            dateIssued = datetime.strptime(self.request.get("dateIssued"), '%Y-%m-%d')
            geometryShader = self.request.get('geometryShader') == 'on'
            tesselationShader = self.request.get('tesselationShader') == 'on'
            shaderInt16 = self.request.get('shaderInt16') == 'on'
            sparseBinding = self.request.get('sparseBinding') == 'on'
            textureCompressionETC2 = self.request.get('textureCompressionETC2') == 'on'
            vertexPipelineStoresAndAtomics = self.request.get('vertexPipelineStoresAndAtomics') == 'on'

            user = users.get_current_user()

            mygpu_key = ndb.Key('Gpu',name)
            mygpu = mygpu_key.get()

            if mygpu == None:

                new_details = Gpu(id=name, name=name, manufacturer=manufacturer, dateIssued=dateIssued, geometryShader=geometryShader,
                                tesselationShader=tesselationShader, shaderInt16=shaderInt16, sparseBinding=sparseBinding,
                                textureCompressionETC2=textureCompressionETC2,
                                vertexPipelineStoresAndAtomics=vertexPipelineStoresAndAtomics)

                new_details.put()

                self.redirect('/')

            else:
                template_values = {
                        'error':'Gpu already in datastore'

                 }
                template = JINJA_ENVIRONMENT.get_template('mainpage.html')
                self.response.write(template.render(template_values))

        elif action == 'Delete':
            index = int(self.request.get('index'))
            user = users.get_current_user()
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()
            del myuser.details[index]
            myuser.put()
            self.redirect('/')


app = webapp2.WSGIApplication([
            ('/', MainPage),
            ('/detail',Detail),
            ('/edit',Edit),
            ('/search', Find)
        ], debug=True)