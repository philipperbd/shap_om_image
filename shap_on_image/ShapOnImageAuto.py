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

    def symmetry(self, plot_name):
        """
        return value of symmetry for top/bot and left/right
        """
        check_list_top = ['shoulder', 'elbow', 'wrist', 'top']
        check_list_right = ['rshoulder', 'relbow', 'rwrist', 'rhip', 'rknee', 'rankle', 'right']
        
        top, bot, right, left = [], [], [], []
        
        for feature, shap_value in self.shap[plot_name].items():
            for word in check_list_top:
                if word in feature.lower(): top.append(shap_value)
                else: bot.append(shap_value)
            for word in check_list_right:
                if word in feature.lower(): right.append(shap_value)
                else: left.append(shap_value)

        top, bot, right, left = sum(top), sum(bot), sum(right), sum(left)

        print(plot_name, "top ", top, "bot", bot, "left", left, "right", right)
        
        if top > bot:
            sym_top_bot = round(top / bot)
        else:
            sym_top_bot = round(bot / top) * -1
        
        if left > right:
            sym_left_right = round(left / right)
        else:
            sym_left_right = round(right / left) * -1

        return sym_top_bot, sym_left_right

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
        print_lines = False

        #plt.suptitle(plot_name.replace('_', ' ').upper(), weight="bold")
        #plt.title('XGBoost mean AUC : ' + str(mean) + ' ('+ str(std) + ')')

        for feature, shap_value in self.shap[plot_name].items():
            shap = shap_value * alpha
            color = 'blue'
            
            if plot_name[:11] == 'linear_data':
                feature_type = feature[-2:]
                x = self.positions[feature[:-2]]['x']
                y = self.positions[feature[:-2]]['y']
                shap = shap / 7 

                if feature_type == '_x':
                    plt.plot([x - abs(shap), x + abs(shap)], [y, y], color='blue')
                else:
                    plt.plot([x, x], [y - abs(shap), y + abs(shap)], color='blue')
            else:
                x = self.positions[feature]['x']
                y = self.positions[feature]['y']
                plt.scatter(x, y, s=abs(shap), color=color)

        sym_top_bot, sym_left_right = self.symmetry(plot_name=plot_name)

        plt.text(0, 1, "Left / Right: " + str(sym_left_right))
        plt.text(0, 20, "Top / Bot: " + str(sym_top_bot))

        plt.arrow(202, 221, sym_left_right * 3, 0, head_width=5, color="crimson")
        plt.arrow(202, 221, 0, -sym_top_bot * 3, head_width=5, color="crimson")

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
        
        