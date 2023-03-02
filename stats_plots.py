import matplotlib.pyplot as plt
import json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--path")

args = parser.parse_args()

def sym_plots(stats, datasets):

    for label in ["global", "normal", "anormal"]:
        for sym_type in ["T-B", "L-R"]:

            x = [stats[dataset]["sym_"+label][sym_type] for dataset in datasets]
            y = [stats[dataset]["mean"] for dataset in datasets]
            y_error = [stats[dataset]["std"] for dataset in datasets]

            combined = zip(x, y, y_error, datasets)
            sorted_combined = sorted(combined, key=lambda x: x[0])
            x_sorted, y_sorted, y_error_sorted, datasets_sorted = zip(*sorted_combined)

            fig, ax = plt.subplots()

            plt.errorbar(x_sorted, y_sorted, yerr=y_error_sorted, fmt='o', capsize=5)

            plt.xlabel(sym_type)
            plt.ylabel("Mean AUC")
            plt.title(label.upper() + " - AUC vs " + sym_type)

            plt.ylim(0, 1)

            plt.savefig(
                args.path + "Stats_outputs/" + label + "_AUC_vs_" + sym_type + ".png", 
                dpi=300, bbox_inches='tight')

def auc_plot(stats, datasets):
    fig, ax = plt.subplots()

    x = datasets # list of datasets
    y = [stats[dataset]["mean"] for dataset in datasets] # mean auc
    y_error = [stats[dataset]["std"] for dataset in datasets] # std auc

    #combined = zip(x, y, y_error)
    #sorted_combined = sorted(combined, key=lambda x: x[0])
    #x_sorted, y_sorted, y_error_sorted, datasets_sorted = zip(*sorted_combined)

    fig, ax = plt.subplots()

    plt.errorbar(x, y, yerr=y_error, fmt='o', capsize=5)

    plt.xlabel("Dataset")
    plt.ylabel("Mean AUC")
    plt.title("Mean AUC with std by dataset")

    plt.xticks(rotation=90)

    plt.ylim(0, 1)

    plt.savefig(
        args.path + "Stats_outputs/mean_auc.png", 
        dpi=300, bbox_inches='tight')

# ouvrir stats dict
f = open(args.path + "stats.json")
stats = json.load(f)
f.close()

datasets = [dataset for dataset in stats.keys()]

datasets.remove("amplitudes")

sym_plots(stats=stats, datasets=datasets)

auc_plot(stats=stats, datasets=datasets)

