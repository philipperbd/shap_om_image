from matplotlib import pyplot as plt
import os
import cv2

class ShapOnImage:

    def __init__(self, suptitle="", title=""):
        """
        args:
            image: str, path to image
            dimensions: list, dimensions of output image (e.g. [0, 300, 0, 220])
            values: dict, positions on figure (verify dimensions) and shap values for every feature
            alpha: float, coefficient to multiply every shap values to better visualisation
            suptitle: str, main title of output figure
            title: str, title of output figure
        """          
        self.feature_cnt = 0
        self.suptitle = suptitle               
        self.title = title

    def get_image(self, image, dimensions):
        self.image = image                      
        self.dimensions = dimensions      
    
    def get_positions(self, features):
        if not hasattr(self, 'image'):
            print('No image loaded yet - use get_image() function')
        else:
            positions = {}
            def ask_feature(nb):
                print('Positions for', features[nb], end=" ")

            def click_event(event, x, y, flags, params):
                if event == cv2.EVENT_LBUTTONDOWN:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(img, str(x) + ',' +
                                str(y), (x,y), font,
                                1, (255, 0, 0), 2)
                    cv2.imshow('image', img)

                    positions[features[self.feature_cnt]] = {'x' : x, 'y': y}
                    
                    print(x, y)

                    self.feature_cnt += 1
                    if self.feature_cnt == len(features):
                            cv2.destroyAllWindows()
                    else: ask_feature(self.feature_cnt)
            
            img = cv2.imread(self.image, 1)
            cv2.imshow('image', img)
            ask_feature(0)
            cv2.setMouseCallback('image', click_event)
            cv2.waitKey(0)
            print('List of features-positions:', positions)
            self.values = positions

    def get_shap(self, shap_values):
        id = 0
        for key, _ in self.values.items():
            self.values[key]['shap'] = shap_values[id]
            id +=1
    
    def check_init(self):
        """
        Print results of few tests on class initialisation
        """
        print('---Initialisation Check---')
        if os.path.exists(self.image):
            print('Path to Image: OK')
        else:
            print('Path to Image: ERROR')
        dim_error = False
        for _, value in self.values.items():
            x = value['x']
            y = value['y']
            max_x = self.dimensions[1]
            max_y = self.dimensions[3]
            if x > max_x or y > max_y:
                dim_error = True
        if dim_error:
            print('Positions according to Image dimensions: ERROR')
        else:
            print('Positions according to Image dimensions: OK')
    
    def plot(self, alpha=1):
        """
        Plot the figure with image and shap values at specific positions
        """
        try:
            im = plt.imread(self.image)
        except: 
            print('Can\'t load image, verify path to image -> cf. Check_init()')
            return
        fig, ax = plt.subplots()
        im = ax.imshow(im, extent=self.dimensions)
        plt.axis('off')

        plt.suptitle(self.suptitle, weight="bold")
        plt.title(self.title)

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