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
        check_list_top = [
            'lshoulder-lelbow', 'rshoulder-relbow', 'lelbow-lwrist', 'relbow-rwrist',
            'lshoulder', 'rshoulder', 'lelbow', 'relbow', 'lwrist', 'rwrist',
            'top_right', 'top_left']
        check_list_right = [
            'rshoulder-relbow', 'relbow-rwrist', 'rshoulder', 'relbow', 'rwrist',
            'rhip-rknee', 'rknee-rankle', 'rhip', 'rknee', 'rankle',
            'top_right', 'bot_right']
        
        
        top, bot, right, left = [], [], [], []
        nb_top, nb_bot, nb_right, nb_left = 0, 0, 0, 0

        print(plot_name)
        
        for feature, shap_value in self.shap[plot_name].items():
            if feature == "Face":
                continue
            if plot_name[:11] == 'linear_data':
                feature = feature[:-2]
            if feature.lower() in check_list_top:
                #print("top", feature)
                top.append(shap_value)
                nb_top += 1
            else: 
                #print("bot", feature)
                bot.append(shap_value)
                nb_bot += 1
            if feature.lower() in check_list_right:
                #print("right", feature)
                right.append(shap_value)    
                nb_right += 1
            else: 
                #print("left", feature)
                left.append(shap_value)
                nb_left += 1

        top, bot, right, left = sum(top), sum(bot), sum(right), sum(left)

        if bot > top:
            sym_top_bot = round((bot / top), 2)
        else:
            sym_top_bot = round((top / bot), 2)
        if right > left:
            sym_left_right = round((right / left), 2) * -1
        else:
            sym_left_right = round((left / right), 2)

        print(top, bot, left, right)
        print(sym_top_bot, sym_left_right)

        print('--------------')

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

        dataset = plot_name[:plot_name.rfind('_')]

        mean = round(self.auc[dataset]['mean'], 2)
        std = round(self.auc[dataset]['std'], 2)
        sym_top_bot, sym_left_right = self.symmetry(plot_name=plot_name)

        plt.suptitle(plot_name.replace('_', ' ').upper(), weight="bold")
        plt.title(
            'AUC: ' + str(mean) + '('+ str(std) + ') ' + \
            'L/R: ' + str(sym_left_right) + ' ' + \
            'T/B: ' + str(-sym_top_bot))

        for feature, shap_value in self.shap[plot_name].items():
            shap = shap_value * alpha
            color = 'blue'
            
            if plot_name[:11] == 'linear_data' and feature != "Face":
                feature_type = feature[-2:]
                x = self.positions[feature[:-2]]['x']
                y = self.positions[feature[:-2]]['y']
                shap = shap / 7 

                if feature_type == '_x':
                    plt.plot([x - abs(shap)/2, x + abs(shap)/2], [y, y], color='blue')
                else:
                    plt.plot([x, x], [y - abs(shap)/2, y + abs(shap)/2], color='blue')
            else:
                x = self.positions[feature]['x']
                y = self.positions[feature]['y']
                plt.scatter(x, y, s=abs(shap), color=color)

        plt.arrow(202, 221, sym_left_right * 10, 0, head_width=5, color="crimson")
        plt.arrow(202, 221, 0, sym_top_bot * 10, head_width=5, color="crimson")

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
        
        