def add_shap_to_values(self):
    """
    Add shap values in values variable containing features names, positions and shap values.
    """
    self.values = self.positions
    id = 0
    for key, _ in self.values.items():
        self.values[key]['shap'] = self.shap[id]
        id +=1

def ask_for_feature(self):
    print('Positions for', self.features[self.feature_cnt], end=" ")
    self.feature_cnt += 1
    

def click_event(event, x, y, flags, params):
    import cv2
    self, img = params[0], params[1]
    if event == cv2.EVENT_LBUTTONDOWN:
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
                    str(y), (x,y), font,
                    1, (255, 0, 0), 2)
        cv2.imshow('image', img)
        self.positions[self.features[self.feature_cnt-1]] = {'x' : x, 'y': y}
        print(x, y)
        if self.feature_cnt == len(self.features):
            cv2.destroyAllWindows()
        else: 
            ask_for_feature(self)
            