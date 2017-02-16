import tool
from workflow import Work


@tool.state
def feature_join(*features_path):
    shop_feature = {}
    for feature_path in features_path[-1:]:
        feature_reader = tool.Reader(feature_path)
        for row in feature_reader:
            shop_feature.setdefault(row[0], [])
            shop_feature[row[0]] += row[1:]
    feature_writer = tool.Writer(features_path[-1])
    for shop, feature in sorted(shop_feature.items()):
        feature_writer.write_row([shop] + feature)


class FeatureJoin(Work):
    def function(self):
        return feature_join
