from shap_on_image.ShapOnImageAuto import ShapOnImageAuto
import json

image = 'baby.png'
features = [
    "RShoulder", "RElbow", "RWrist", "LShoulder", "LElbow", "LWrist",
    "RHip", "RKnee", "RAnkle", "LHip", "LKnee", "LAnkle",

    "LShoulder-LElbow", "RShoulder-RElbow", "LElbow-LWrist", "RElbow-RWrist",
    "LHip-LKnee", "RHip-RKnee", "LKnee-LAnkle", "RKnee-RAnkle",

    "up_right", "up_left", "down_right", "down_left",
    "Nose", "LEar", "REar", "LEye", "REye"]

path = 'Data/'
version = "V2/"

with open(path + 'values.json') as json_file:
    values = json.load(json_file)
with open(path + 'positions.json') as pos_file:
    positions = json.load(pos_file)

with open(path + version + 'shap_v2_face_scalled.json') as shap_file:
    shap = json.load(shap_file)
with open(path + version + 'auc_v2_face.json') as auc_file:
    auc = json.load(auc_file)


ShapImAuto = ShapOnImageAuto(image=image, features=features,
                             positions=positions, values=values, 
                             shap=shap, auc=auc)

ShapImAuto.create_plots(path="Visuals/V2_face/", alpha=1000)
