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
        cv2.putText(img, str(x) + ',' +
                    str(y), (x, y), font,
                    1, (255, 0, 0), 2)
        cv2.imshow('image', img)
        self.positions[self.features[self.feature_cnt-1]] = {'x': x, 'y': y}
        print(x, y)
        if self.feature_cnt == len(self.features):
            cv2.destroyAllWindows()
        else:
            ask_for_feature(self)

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

    for feature, shap_value in self.shap[plot_name].items():
        if feature == "Face":
            continue
        if plot_name[:11] == 'linear_data':
            feature = feature[:-2]
        if feature.lower() in check_list_top:
            top.append(shap_value)
            nb_top += 1
        else:
            bot.append(shap_value)
            nb_bot += 1
        if feature.lower() in check_list_right:
            right.append(shap_value)
            nb_right += 1
        else:
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

    return [sym_top_bot, sym_left_right]


def informations(self, plot_name, auc):
    """ Return useful information for plots
    """
    dataset = plot_name[:plot_name.rfind('_')]

    mean_auc = round(auc[dataset]['mean'], 2)
    std_auc = round(auc[dataset]['std'], 2)

    sym = symmetry(self, plot_name=plot_name)

    suptitle = plot_name.replace('_', ' ').upper()

    title = (
        'AUC: ' + str(mean_auc) + '(' + str(std_auc) + ') ' +
        'L/R: ' + str(sym[0]) + ' ' +
        'T/B: ' + str(-sym[1]))

    return suptitle, title, sym
