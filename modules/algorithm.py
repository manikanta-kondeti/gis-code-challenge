from osgeo import ogr
from modules.utils import WKT


class Algorithm:

    def __init__(self):
        return

    @classmethod
    def extract_points_based_on_props(self, features):
        '''
        :param features:
        :return: features
        # High probable points based on intuition and detailed checking of attributes:
            previous_activity, current_activity = {in_vehicle, X} or {X, in_vehicle} --> X={on_foot, on_bicycle, still} adn speed < 70
        '''

        new_features_set1 = filter(lambda feature: feature['properties']['previous_dominating_activity'] == 'in_vehicle'
                                    and feature['properties']['current_dominating_activity'] in ['still', 'on_foot', 'on_bicyle', 'NULL']
                                    and feature['properties']['speed'] < 70,
                                    features)
        new_features_set2 = filter(lambda feature: feature['properties']['current_dominating_activity'] == 'in_vehicle'
                                    and feature['properties']['previous_dominating_activity'] in ['still', 'on_foot', 'on_bicycle', 'NULL']
                                    and feature['properties']['speed'] < 70,
                                   features)

        filtered_features = new_features_set1 + new_features_set2
        return filtered_features

    @classmethod
    def remove_unintersected_points(self, point_objects, route_objects, buffer_distance=0.005):
        '''
        :param features:
        :return: features

        Useful resources:
        http://pcjericks.github.io/py-gdalogr-cookbook/geometry.html#buffer-a-geometry
        http://pcjericks.github.io/py-gdalogr-cookbook/geometry.html#create-geometry-from-geojson
        '''

        route_wkt_objects = map(lambda route: WKT.linestring_to_WKT(route['geometry']['coordinates']), route_objects)
        bufferDistance = buffer_distance
        polygon_buffered_from_point = []
        for point in point_objects:
            wkt = "POINT  ("+ str(point['geometry']['coordinates'][0]) + " " + str(point['geometry']['coordinates'][1]) + ")"
            pt = ogr.CreateGeometryFromWkt(wkt)
            point_object = {'buffered_point': pt.Buffer(bufferDistance), 'id': point['properties']['id']}
            polygon_buffered_from_point.append(point_object)

        # Check intersections with all the routes
        point_route_intersections = []
        for point_buffered in polygon_buffered_from_point:
            point_poly = ogr.CreateGeometryFromWkt(str(point_buffered['buffered_point']))
            route_geoms = map(lambda route: ogr.CreateGeometryFromWkt(str(route)), route_wkt_objects)
            intersections = map(lambda route_geom: route_geom.Intersection(point_poly), route_geoms)
            point_intersection_object = {'intersections' : map(lambda intersection: intersection.ExportToWkt(), intersections), 'id' : point_buffered['id']}
            point_route_intersections.append(point_intersection_object)

        filtered_point_ids = []
        for intersection in point_route_intersections:
            is_bus_stop = False
            for j in intersection['intersections']:
                if j != "GEOMETRYCOLLECTION EMPTY" and is_bus_stop == False:
                    is_bus_stop = True
                    filtered_point_ids.append(intersection['id'])

        # extract point features from id's
        filtered_point_features = []
        for id in filtered_point_ids:
            for point_object in point_objects:
                if id == point_object['properties']['id']:
                    filtered_point_features.append(point_object)

        return filtered_point_features
