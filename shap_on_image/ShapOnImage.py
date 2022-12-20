from matplotlib import pyplot as plt
import os
import cv2

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
            os.path.exists(self.image)
            self.image = image
            self.features = features
            self.shap = shap 
            self.positions = positions
            self.feature_cnt = 0
        except:
            print('Error during init - verify path to image')
    
    def put_shap_in_values(self):
        """
        Add shap values in values variable containing features names, positions and shap values.
        """
        id = 0
        for key, _ in self.values.items():
            self.values[key]['shap'] = self.shap[id]
            id +=1
    
    def set_positions(self):
        """
        Tool to select positions of every feature on the image.
        """
        if not hasattr(self, 'image'):
            print('No image loaded yet - use get_image() function')
        else:
            positions = {}
            def ask_feature(nb):
                print('Positions for', self.features[nb], end=" ")

            def click_event(event, x, y, flags, params):
                if event == cv2.EVENT_LBUTTONDOWN:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(img, str(x) + ',' +
                                str(y), (x,y), font,
                                1, (255, 0, 0), 2)
                    cv2.imshow('image', img)

                    positions[self.features[self.feature_cnt]] = {'x' : x, 'y': y}
                    
                    print(x, y)

                    self.feature_cnt += 1
                    if self.feature_cnt == len(self.features):
                            cv2.destroyAllWindows()
                    else: ask_feature(self.feature_cnt)
            
            img = cv2.imread(self.image, 1)
            cv2.imshow('image', img)
            ask_feature(0)
            cv2.setMouseCallback('image', click_event)
            cv2.waitKey(0)
            self.values = positions
            self.put_shap_in_values()
    
    def plot(self, suptitle="", title="", alpha=1):
        """
        Plot the figure with image and shap values at specific positions
        args:
            suptitle: str, suptitle to display on image
            title: str, title to display on image
            alpha: float, coefficient to multiply every shap values by.
        """
        try:
            im = plt.imread(self.image)
        except: 
            print('Can\'t load image, verify path to image -> cf. Check_init()')
            return
        fig, ax = plt.subplots()
        im = ax.imshow(im)
        plt.axis('off')

        plt.suptitle(suptitle, weight="bold")
        plt.title(title)

        for _, value in self.values.items():
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