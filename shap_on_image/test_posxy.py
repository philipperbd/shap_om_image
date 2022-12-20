import cv2

POSITIONS = {}

counter = 0

def ask_feature(nb):
    print('-- Choosing positions for', features[nb], '--')

def click_event(event, x, y, flags, params):

    global counter

    if event == cv2.EVENT_LBUTTONDOWN:

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
                    str(y), (x,y), font,
                    1, (255, 0, 0), 2)
        cv2.imshow('image', img)

        POSITIONS[features[counter]] = (x,y)
        
        print(features[counter], x, y)

        counter += 1
        if counter == len(features):
                cv2.destroyAllWindows()
        else:
            ask_feature(counter)

        
        
if __name__=="__main__":
 
    img = cv2.imread('shap_on_image\image_test.jpg', 1)
 
    cv2.imshow('image', img)

    features = ['RShoulder', 'LShoulder', 'RHip']

    ask_feature(0)
    
    cv2.setMouseCallback('image', click_event)

    cv2.waitKey(0)

    print(POSITIONS)