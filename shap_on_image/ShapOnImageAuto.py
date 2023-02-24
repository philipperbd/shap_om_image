from matplotlib import pyplot as plt
import os
import cv2
from shap_on_image.utils import *

class ShapOnImageAuto:

    def __init__(self, image, features, shap, auc, positions={}):
        """
        args:
            image: str, path to image
            features: list, features names as strings
            shap: list, shap values extracted from shap packages
            positions: dict, features with 'x' and 'y' values, can be set with set_positions()
        """       
        try: 
            os.path.exists(image)
            self.image = image
            self.features = features
            self.shap = shap 
            self.auc = auc
            self.positions = positions
            self.feature_cnt = 0
        except:
            print('Error during init - verify path to image')
    
    def set_positions(self):
        """
        Tool to select positions of every feature on the image.
        """
        if not hasattr(self, 'image'):
            print('No image loaded yet - use get_image() function')
        else:
            img = cv2.imread(self.image, 1)
            cv2.imshow('image', img)
            ask_for_feature(self)
            cv2.setMouseCallback('image', click_event, [self, img])
            cv2.waitKey(0)

    def get_positions(self):
        """
        Return list of positions
        """
        return self.positions

    def create_plot(self, path, plot_name, suptitle="", title="", alpha=1):
        """
        Plot the figure with image and shap values at specific positions
        args:
            suptitle: str, suptitle to display on image
            title: str, title to display on image
            alpha: float, coefficient to multiply every shap values by.
        """
        im = plt.imread(self.image)
        fig, ax = plt.subplots()
        im = ax.imshow(im)
        plt.axis('off')
        try:
            dataset = plot_name.rsplit('_', 1)[0]
            auc = self.auc[dataset]['auc']
            std = self.auc[dataset]['std']
        except:
            auc = 00
            std = 00


        plt.suptitle(plot_name.replace('_', ' ').upper(), weight="bold")
        plt.title('XGBoost mean AUC : ' + str(auc) + ' ('+ str(std) + ')')

        for feature, shap_value in self.shap[plot_name].items():
            try:
                shap = shap_value * alpha
                x = self.positions[feature]['x']
                y = self.positions[feature]['y']
                color = ["cornflowerblue" if shap > 0 else "crimson"]
                plt.scatter(x, y, s=abs(shap), color=color)
            except:
                print(plot_name, feature)
                

        plt.close(fig)
        fig.savefig(path + plot_name + '.png')

    def create_plots(self, path = "", alpha=1):
        """Create several plots and save them in path.

        Args:
            path (str, optional): Path to output plots. Defaults to "".
            alpha (int, optional): Coefficient to multiply shap values by. Defaults to 1.
        """
        for plot_name, _ in self.shap.items():
            #print(plot_name)
            self.create_plot(path, plot_name, alpha=alpha)
        
        