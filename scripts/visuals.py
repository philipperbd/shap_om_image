from shap_on_image.ShapOnImageAuto import ShapOnImageAuto
import json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--path")

args = parser.parse_args()

features = [
    "RShoulder", "RElbow", "RWrist", "LShoulder", "LElbow", "LWrist",
    "RHip", "RKnee", "RAnkle", "LHip", "LKnee", "LAnkle",

    "RShoulder-RElbow", "RElbow-RWrist", "LShoulder-LElbow", "LElbow-LWrist",
    "RHip-RKnee",  "RKnee-RAnkle", "LHip-LKnee", "LKnee-LAnkle",

    "top_right", "top_left", "bot_right", "bot_left",
    "Nose", "LEar", "REar", "LEye", "REye", "Face", "Arrow"]

r_path, version = args.path.rsplit('/', 1)

with open(r_path + '/mean_values.json') as json_file:
    values = json.load(json_file)

with open(r_path + '/positions.json') as pos_file:
    positions = json.load(pos_file)

with open(args.path + '/shap_scalled.json') as shap_file:
    shap = json.load(shap_file)
    
with open(args.path + '/stats.json') as stats_file:
    stats = json.load(stats_file)


ShapImAuto = ShapOnImageAuto(image='data/baby_without_shap.png', features=features,
                             positions=positions, values=values, 
                             shap=shap, stats=stats)
ShapImAuto.create_plots(path=args.path + '/baby_visuals/', full_plt=False, alpha=1000)


ShapImAuto = ShapOnImageAuto(image='data/baby_shap.png', features=features,
                             positions=positions, values=values, 
                             shap=shap, stats=stats)
ShapImAuto.create_plots(path=args.path + '/baby_visuals_shap/', full_plt=True, alpha=1000)
