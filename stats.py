import matplotlib.pyplot as plt

import json
f = open('Data/V2/stats_v2_face.json')
xai = json.load(f)
f.close()

def create_plot(xai, sym_type):
    x_values = [v[sym_type] for v in xai.values()]
    y_values = [v["mean"] for v in xai.values()]
    y_error = [v["std"] for v in xai.values()]

    plt.errorbar(x_values, y_values, yerr=y_error, fmt='o', capsize=5)

    plt.xlabel(sym_type)
    plt.ylabel("Mean AUC")
    plt.title("AUC vs " + sym_type)

    plt.savefig("Visuals/V2_face/stats_AUC_vs_" + sym_type + ".png")

for sym_type in ["T-B", "L-R"]:
    create_plot(xai, sym_type)