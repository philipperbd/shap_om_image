from shap_on_image.ShapOnImageAuto import ShapOnImageAuto
import json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--path")

args = parser.parse_args()

image = 'baby.png'
features = [
    "RShoulder", "RElbow", "RWrist", "LShoulder", "LElbow", "LWrist",
    "RHip", "RKnee", "RAnkle", "LHip", "LKnee", "LAnkle",

    "LShoulder-LElbow", "RShoulder-RElbow", "LElbow-LWrist", "RElbow-RWrist",
    "LHip-LKnee", "RHip-RKnee", "LKnee-LAnkle", "RKnee-RAnkle",

    "up_right", "up_left", "down_right", "down_left",
    "Nose", "LEar", "REar", "LEye", "REye"]

r_path, version = args.path.rsplit('/', 1)

with open(r_path + '/values.json') as json_file:
    values = json.load(json_file)
with open(r_path + '/positions.json') as pos_file:
    positions = json.load(pos_file)

with open(args.path + '/shap_scalled.json') as shap_file:
    shap = json.load(shap_file)
with open(args.path + '/stats.json') as stats_file:
    stats = json.load(stats_file)


ShapImAuto = ShapOnImageAuto(image=image, features=features,
                             positions=positions, values=values, 
                             shap=shap, stats=stats)

ShapImAuto.create_plots(path=args.path + '/Visuals/', alpha=1000)
