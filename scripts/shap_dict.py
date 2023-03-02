import pandas as pd
import shap
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--input")
parser.add_argument("--output")

args = parser.parse_args()

def get_values_labels(path, dataset):

    labels = pd.read_pickle(path + 'labels.pkl')
    shap_values = pd.read_pickle(path + 'shap_values.pkl')

    return shap_values, labels

def generate_dict(shap_values, labels, dataset):

    data = pd.DataFrame(shap_values.abs.values, columns=shap_values.feature_names)
    data['label'] = labels
    dataset_dict = {}
    labels = ['normal', 'anormal']

    for i in range(len(labels)):
        df = data[data['label'] == i].reset_index().drop(['index', 'label'], axis=1)
        df.loc['mean'] = df.mean()
        new_dict = df.loc['mean'].to_dict()
        dataset_dict[dataset + '_' + labels[i]] = new_dict

    return dataset_dict

def handle_face(dictionnary):

    for sub_dict in dictionnary.values():
        face_sum = 0
        keys_to_delete = []

        for key in sub_dict:
            if "Nose" in key or "Ear" in key or "Eye" in key:
                face_sum += sub_dict[key]
                keys_to_delete.append(key)

        for key in keys_to_delete:
            del sub_dict[key]

        if face_sum > 0:
            sub_dict["Face"] = face_sum

    return dictionnary

datasets = [
    'depth', 'segments_len', 
    'linear_data', 'linear_velocity', 'linear_acceleration', 'linear_jurk', 
    'angular_data', 'angular_velocity', 'angular_acceleration', 'angular_jurk']

output = {}

for dataset in datasets:

    path = args.input + '/' + dataset +'/'
    shap_values, labels = get_values_labels(path=path, dataset=dataset)
    dataset_dict = generate_dict(shap_values=shap_values, labels=labels, dataset=dataset)
    output.update(dataset_dict)

output = handle_face(output)

import json
json = json.dumps(output)
f = open(args.output, "w")
f.write(json)
f.close()