import cherrypy
import os

plugStatus123 = False
plugStatus456 = False

class server(object):
    

    @cherrypy.expose
    def index(self):
        return open("index.html")

    @cherrypy.expose
    def changestatus(self, plugId, status):
        global plugStatus123
        global plugStatus456

        if plugId == "123":
            if status == "on":
                plugStatus123 = True
            else:
                plugStatus123 = False
        elif plugId == "456":
            if status == "on":
                plugStatus456 = True
            else:
                plugStatus456 = False

        return str(plugStatus123, plugStatus456)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getstatus(self, plugId):
        global plugStatus123
        global plugStatus456
        if plugId == "123":
            if plugStatus123:
                data = {
                    "plugId" : "123",
                    "plugStatus" : "on"
                }
            else:
                data = {
                    "plugId" : "123",
                    "plugStatus" : "off"
                }
        elif plugId == "456":
            if plugStatus456:
                data = {
                    "plugId" : "456",
                    "plugStatus" : "on"
                }
            else:
                data = {
                    "plugId" : "456",
                    "plugStatus" : "off"
                }
        else:
            data = {
                "plugId" : "ERROR",
                "plugStatus" : "ERROR"
            }
        return data

config = {'/':
{
    'tools.staticdir.on': True,
    'tools.staticdir.dir': os.path.abspath(".")}
}
cherrypy.tree.mount(server(), '/', config=config)
cherrypy.config.update({'server.socket_host': '0.0.0.0'}) 
cherrypy.engine.start()