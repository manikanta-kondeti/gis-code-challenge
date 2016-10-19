from osgeo import ogr
from models.utils import WKT

class Algorithm:

    def __init__(self):
        return

    @classmethod
    def extract_points_based_on_props(self, features):

        '''
        # High probable points:
            previous_activity, current_activity = {in_vehicle, X} or {X, in_vehicle} --> X={on_foot, on_bicycle, still}
        '''
        # Filter operation
        new_features_set1 = filter(lambda feature: feature['properties']['previous_dominating_activity'] == 'in_vehicle'
                                    and feature['properties']['current_dominating_activity'] in ['still', 'on_foot', 'on_bicycle'],
                                    features)
        new_features_set2 = filter(lambda feature: feature['properties']['current_dominating_activity'] == 'in_vehicle'
                                    and feature['properties']['previous_dominating_activity'] in ['still', 'on_foot', 'on_bicycle'],
                                   features)

        filtered_features = new_features_set1 + new_features_set2
        return filtered_features

    @classmethod
    def remove_unintersected_points(self, point_objects, route_objects, buffer_distance=0.0005):
        '''
        :param features:
        :return:

        http://pcjericks.github.io/py-gdalogr-cookbook/geometry.html#buffer-a-geometry

        http://pcjericks.github.io/py-gdalogr-cookbook/geometry.html#create-geometry-from-geojson
        POINT object :
        {
            u'geometry': {u'type': u'Point', u'coordinates': [39.2815789, -6.7527988]},
            u'type': u'Feature',
            u'properties': {
            u'previous_dominating_activity': u'still', u'bearing': 0, u'route': None,
            u'previous_dominating_activity_confidence': 100, u'current_dominating_activity': u'in_vehicle',
            u'current_dominating_activity_confidence': 42, u'timestamp': u'2015-12-14T17:57:31+03:00', u'created_at': u'2015-12-14 14:57:38',
             u'feature': u'passive_tracking', u'id': 763, u'speed': 0, u'altitude': 0.0, u'accuracy': 24.0
            }
        }

        ROUTE object:
        {
        u'geometry': {u'type': u'LineString', u'coordinates': [[39.1708251, -6.8765432],
                [39.1712366, -6.8763936], [39.1714444, -6.876443], [39.1714371, -6.8771191], [39.1713169, -6.8779287],
                [39.1711023, -6.8795136], [39.170965, -6.8806299], [39.1707848, -6.8817973], [39.1707933, -6.8821808],
                [39.1707247, -6.8825557], [39.1706389, -6.8829733], [39.1705702, -6.8834164], [39.1704929, -6.8840981],
                [39.1705101, -6.8847627], [39.1704672, -6.8853762], [39.1703299, -6.8859301], [39.1700552, -6.8867055],
                [39.1696175, -6.8874043], [39.1692226, -6.8880093], [39.1680811, -6.8897646], [39.1671541, -6.8904207],
                [39.1666992, -6.890932], [39.1665361, -6.8911535], [39.1664675, -6.8914092], [39.166622, -6.8919716],
                [39.1668537, -6.8930537], [39.167034, -6.8935906], [39.1671627, -6.8939996], [39.1672915, -6.8943745],
                [39.1673172, -6.8950391], [39.167309, -6.8958411], [39.1673859, -6.8966922], [39.1674889, -6.8970927],
                [39.1675492, -6.8973072], [39.1676605, -6.897621], [39.1679352, -6.8982175], [39.1681841, -6.8986179],
                [39.1683729, -6.8990781], [39.1685532, -6.8995638], [39.168742, -6.9000665], [39.1688707, -6.9005778],
                [39.1693256, -6.9023671], [39.1694115, -6.9028443], [39.1695831, -6.9032363], [39.1696317, -6.9033876],
                [39.1693318, -6.904385], [39.1688973, -6.9063927], [39.1686988, -6.9073993], [39.1685003, -6.9080117],
                [39.1681623, -6.9100141]]},
        u'type': u'Feature',
        u'properties': {u'route_id': 5509682}
        }

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
