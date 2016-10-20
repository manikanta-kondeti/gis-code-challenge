import json
import webapp2
from paste import httpserver
import jinja2
import os
from modules.utils import GeoJson
from modules.algorithm import Algorithm

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class WebPageHandler(webapp2.RequestHandler):
    """
        Web page to compute the bus stops based on the algorithm, and also to send html as response
    """
    def get(self, term=None):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'text/html'

        print "Request being served...Please check this page http://localhost:8080/extract_bus_stops"
        # Read Routes
        routes = GeoJson()
        routes.read_contents("./data/routes.geojson")
        routes_json = routes.to_geojson()

        # Read Activity points
        activity_points = GeoJson()
        activity_points.read_contents("./data/activity_points.geojson")
        activity_points.features = Algorithm.extract_points_based_on_props(activity_points.features)
        activity_points.features = Algorithm.remove_unintersected_points(activity_points.features, routes.features)
        busstops_json = activity_points.to_geojson()

        google_bus_stops = GeoJson()
        google_bus_stops.read_contents("./data/bus_stops_from_google_maps")
        google_bus_stops_json = google_bus_stops.to_geojson()

        print "*** Successful ***", "\n"
        template = JINJA_ENVIRONMENT.get_template('./views/wms.html')
        self.response.write(template.render({
                                            "routes_json" : json.dumps(routes_json),
                                            "busstops_json" : json.dumps(busstops_json),
                                            "google_busstops_json" : json.dumps(google_bus_stops_json),
                                            "length_of_extracted_busstops" : json.dumps(len(activity_points.features))
                        }))

        return


app = webapp2.WSGIApplication([
    ('/extract_bus_stops', WebPageHandler),
], debug=True)


def main():

    httpserver.serve(app, host='127.0.0.1', port='8080')

if __name__ == '__main__':
    main()
