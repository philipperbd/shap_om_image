def add_shap_to_values(self):
    """
    Add shap values in values variable containing features names, positions and shap values.
    """
    self.values = self.positions
    id = 0
    for key, _ in self.values.items():
        self.values[key]['shap'] = self.shap[id]
        id += 1


def ask_for_feature(self):
    """
    Print feature we are looking for positions x/y on image.
    """
    print('Positions for', self.features[self.feature_cnt], end=" ")
    self.feature_cnt += 1


def click_event(event, x, y, flags, params):
    """
    Click event handler for left mouse click to select positions of features on image.

    Args:
        params (list): [ShapOnImage instance, OpenCV img]
    """
    import cv2
    self, img = params[0], params[1]
    if event == cv2.EVENT_LBUTTONDOWN:
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +str(y), (x, y), font, 1, (255, 0, 0), 2)
        cv2.imshow('image', img)
        self.positions[self.features[self.feature_cnt-1]] = {'x': x, 'y': y}
        print(x, y)
        if self.feature_cnt == len(self.features):
            cv2.destroyAllWindows()
        else:
            ask_for_feature(self)


def informations(self, plot_name, stats):
    """ Return useful information for plots
    """
    dataset, sym_type = plot_name.rsplit('_', 1)

    mean_auc = round(stats[dataset]['mean'], 2)
    std_auc = round(stats[dataset]['std'], 2)
    sym = stats[dataset]['sym_' + sym_type]
    sym = [sym["T-B"], sym["L-R"]]

    suptitle = plot_name.replace('_', ' ').upper()

    title = (
        'AUC: ' + str(mean_auc) + '(' + str(std_auc) + ') ' +
        'T/B: ' + str(sym[0]) + ' ' +
        'L/R: ' + str(sym[1]))

    return suptitle, title, sym

def feature_color(plot_name, feature, values):
    """Return int value corresponding to color in colormap
    """
    dataset, label = plot_name.rsplit('_', 1)
    if feature == "Face":
        face = []
        for elem in ['Nose', 'REar', 'LEar', 'REye', 'LEye']:
            face.append(values[dataset][label][elem]["mean_value"])
        color = 1 - (sum(face) / len(face))
    else: 
        color = 1 - values[dataset][label][feature]["mean_value"]
    return color
