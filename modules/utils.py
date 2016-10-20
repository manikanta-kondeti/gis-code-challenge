import json


class GeoJson:

    def __init__(self):
        self.features = []
        self.crs = ''
        self.type = None

    def read_contents(self, file_path):
        contents = {}
        with open(file_path) as f:
            contents = json.loads(f.read())
        for key in contents:
            if key == "crs":
                self.crs = contents[key] or 'WGS:84'
            elif key == "type":
                self.type = contents[key]
            elif key == "features":
                self.features = contents[key]
        return

    def to_geojson(self):
        # Generate geojson with current attributes
        new_geojson =  {}
        new_geojson["crs"] = self.crs
        new_geojson["type"] = self.type
        new_geojson["features"] = self.features

        return json.dumps(new_geojson)

class WKT:

    def __init__(self):
        return

    @classmethod
    def linestring_to_WKT(cls, linestring_coods):
        wkt = "LINESTRING ("
        coordinates_string = ""
        for coods in linestring_coods:
            coordinates_string = coordinates_string + " " + str(coods[0]) + " " + str(coods[1]) + ","

        return "LINESTRING (" + coordinates_string[:-1] + ")"