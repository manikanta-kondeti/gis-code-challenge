from models.geojson_utils import GeoJson


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
    def remove_outliers(self, features):
        '''
        :param features:
        :return:

        http://pcjericks.github.io/py-gdalogr-cookbook/geometry.html#buffer-a-geometry

        http://pcjericks.github.io/py-gdalogr-cookbook/geometry.html#create-geometry-from-geojson
        '''
        return
