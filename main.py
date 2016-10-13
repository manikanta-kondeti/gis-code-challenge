import webapp2
from paste import httpserver

class HelloWebapp2(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello, webapp2!')

app = webapp2.WSGIApplication([
    ('/', HelloWebapp2),
], debug=True)

def main():

    httpserver.serve(app, host='127.0.0.1', port='8080')

if __name__ == '__main__':
    main()
