import pyramid.httpexceptions as exc
import os.path
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.wsgi import wsgiapp

@wsgiapp
def indexPage(environment, beginResp):
    status = '200 OK'
    response_headers = [("Content-Type", "text/html")]
    result = []
    file = open('./index.html','rb')
    for x in file:
    	result.append(x)
    beginResp(status, response_headers)	
    return result
@wsgiapp
def aboutmePage(environment, beginResp):
    status = '200 OK'
    response_headers = [("Content-Type", "text/html")]
    result = []	
    file = open('./about/aboutme.html','rb')
    for x in file:
    	result.append(x)
    beginResp(status, response_headers)
    return result


mTop = "<div class='top'>Middleware TOP</div>"
mBottom =  "<div class='botton'>Middleware BOTTOM</div>"

class MiddleWare(object):
 	def __init__(self, application):
 		self.application = application

 	def __call__(self, environment, beginResp):
	 	openBody = -1
 		closeBody = -1
 		response = self.application(environment, beginResp)
 		for x in response:
 			if "<body>" in x.decode():
	 			openBody = response.index(x)
 			if "</body>" in x.decode():
 				closeBody = response.index(x)
 		result = response[:openBody] + [mTop.encode()] + response[openBody:closeBody+1] + [mBottom.encode()] + response[closeBody+1:]
 		return result

if __name__ == '__main__':
    configurator = Configurator()

    configurator.add_route('root', '/')
    configurator.add_view(indexPage, route_name='root')

    configurator.add_route('index_html', '/index.html')
    configurator.add_view(indexPage, route_name='index_html')

    configurator.add_route('aboutme_html', '/about/aboutme.html')
    configurator.add_view(aboutmePage, route_name='aboutme_html')

    application = configurator.make_wsgi_app()
    myApp = MiddleWare(application)
    server = make_server('localhost', 8000, myApp)
    server.serve_forever()
