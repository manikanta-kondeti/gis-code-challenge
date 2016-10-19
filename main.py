import webapp2
from paste import httpserver
import jinja2
import os
from models.utils import GeoJson
from models.algorithm import Algorithm

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class ExtractBusStops(webapp2.RequestHandler):
    def get(self):
        # Read and load activity points
        activity_points = GeoJson()
        activity_points.read_contents("./data/activity_points.geojson")

        # Read and load routes
        routes = GeoJson()
        routes.read_contents("./data/routes.geojson")


        activity_points.features = Algorithm.extract_points_based_on_props(activity_points.features)
        activity_points.features = Algorithm.remove_unintersected_points(activity_points.features, routes.features)

        new_json = activity_points.to_geojson()

        self.response.write(new_json)



class HomePage(webapp2.RequestHandler):
    """
        To handle post request, when the entity is approved or rejected
    """
    def get(self, term=None):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'text/html'

        template = JINJA_ENVIRONMENT.get_template('./views/index.html')
        self.response.write(template.render({}))
        return


app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/extract', ExtractBusStops)
], debug=True)


def main():

    httpserver.serve(app, host='127.0.0.1', port='8080')

if __name__ == '__main__':
    main()
