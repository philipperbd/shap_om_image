import os
import pickle
import json

file = 'Data/V2/shap_v2_face'

f = open(file + '.json')
data = json.load(f)
f.close()

# get max and min
v_min = 10
v_max = -10
for i in data:
    for j in data[i]:
        if data[i][j] <= v_min:
            v_min = data[i][j]
        if data[i][j] >= v_max:
            v_max = data[i][j]

def min_max(min, max, value):
    return (value-min)/(max-min)

min = 1
max = -1
for i in data:
    for j in data[i]:
        data[i][j] = min_max(min=v_min, max=v_max, value=data[i][j])

json_object = json.dumps(data)
with open(file + '_scalled.json', 'wt') as f:
    f.write(json_object)