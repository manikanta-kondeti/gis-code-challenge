import json
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


class WMSWebPage(webapp2.RequestHandler):
    """
        To handle post request, when the entity is approved or rejected
    """
    def get(self, term=None):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'text/html'

        # Routes
        routes = GeoJson()
        routes.read_contents("./data/routes.geojson")
        routes_json = routes.to_geojson()
        print "Request being served...Please check this page http://localhost:8080/busstops"
        activity_points = GeoJson()
        activity_points.read_contents("./data/activity_points.geojson")
        activity_points.features = Algorithm.extract_points_based_on_props(activity_points.features)
        activity_points.features = Algorithm.remove_unintersected_points(activity_points.features, routes.features)


        busstops_json = activity_points.to_geojson()

        google_busstops = GeoJson()
        google_busstops.read_contents("./data/bus_stops_from_google_maps")
        google_busstops_json = google_busstops.to_geojson()
        print "*** Successful ***", "\n"
        template = JINJA_ENVIRONMENT.get_template('./views/wms.html')
        self.response.write(template.render({
                                            "routes_json" : json.dumps(routes_json),
                                            "busstops_json" : json.dumps(busstops_json),
                                            "google_busstops_json" : json.dumps(google_busstops_json),
                                            "length_of_extracted_busstops" : json.dumps(len(activity_points.features))
                        }))

        return


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
    ('/busstops', WMSWebPage),
], debug=True)


def main():

    httpserver.serve(app, host='127.0.0.1', port='8080')

if __name__ == '__main__':
    main()
