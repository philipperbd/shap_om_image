from matplotlib import pyplot as plt
import os
import cv2
from shap_on_image.utils import *

# TODO: Adapter pour automatiser la créatio de multiples visuels
# TODO: Utiliser pour générer l'ensemble des visuels pour BabyGarches
# TODO: Pip nouvelle version du paquet

class ShapOnImage:

    def __init__(self, image, features, shap, positions={}):
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
            add_shap_to_values(self)
    
    def plot(self, suptitle="", title="", alpha=1):
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

        plt.suptitle(suptitle, weight="bold")
        plt.title(title)

        for _, value in self.positions.items():
            shap = value['shap'] * alpha
            x = value['x']
            y = value['y']
            color = ["cornflowerblue" if shap > 0 else "crimson"]
            plt.scatter(x, y, s=abs(shap), color=color)

        plt.show()

        self.fig = fig
    
    def save(self, save_path="saved_shap_ez_image.png"):
        """
        Save figure at specific path
        args:
            save_path: str, specific path (with filename) to save figure"""
        try:
            self.fig.savefig(save_path)
        except:
            print('Can\'t save figure, verify plot -> cf. Check_init()')