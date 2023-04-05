import cv2
import matplotlib.pyplot as plt
from skimage.transform import resize
import pickle
import numpy as np

EMPTY = True
NOT_EMPTY = False

MODEL = pickle.load(open("E:\MAJOR_PROJECT\SPACECOUNTER\model\model.p", "rb"))

L1,L2=[],[]
t1,t2=None,None

def empty_or_not(spot_bgr):

    flat_data = []

    img_resized = resize(spot_bgr, (15, 15, 3))
    flat_data.append(img_resized.flatten())
    flat_data = np.array(flat_data)

    y_output = MODEL.predict(flat_data)

    if y_output == 0:
        return EMPTY
    else:
        return NOT_EMPTY


def get_parking_spots_bboxes(connected_components):
    (totalLabels, label_ids, values, centroid) = connected_components

    slots = []
    coef = 1
    for i in range(1, totalLabels):

        # Now extract the coordinate points
        x1 = int(values[i, cv2.CC_STAT_LEFT] * coef)
        y1 = int(values[i, cv2.CC_STAT_TOP] * coef)
        w = int(values[i, cv2.CC_STAT_WIDTH] * coef)
        h = int(values[i, cv2.CC_STAT_HEIGHT] * coef)

        slots.append([x1, y1, w, h])

    return slots


def calc_diff(im1, im2):
    return np.abs(np.mean(im1) - np.mean(im2))


def SPACE_COUNTER():
    mask = 'E:\MAJOR_PROJECT\SPACECOUNTER\SAMPLES\mask_1920_1080.png'

    video_path = 'E:\MAJOR_PROJECT\SPACECOUNTER\data\parking_1920_1080_loop.mp4'
    
    mask = cv2.imread(mask, 0)

    cap = cv2.VideoCapture(video_path)

    connected_components = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)

    spots = get_parking_spots_bboxes(connected_components)

    spots_status = [None for j in spots]

    diffs = [None for j in spots]

    previous_frame = None

    frame_nmr = 0
    ret = True
    step = 30

    while ret:
        ret, frame = cap.read()

        if frame_nmr % step == 0 and previous_frame is not None:
            for spot_indx, spot in enumerate(spots):
                x1, y1, w, h = spot

                spot_crop = frame[y1:y1 + h, x1:x1 + w, :]

                diffs[spot_indx] = calc_diff(spot_crop, previous_frame[y1:y1 + h, x1:x1 + w, :])

            #print([diffs[j] for j in np.argsort(diffs)][::-1])

        if frame_nmr % step == 0:
            if previous_frame is None:
                arr_ = range(len(spots))
            else:
                arr_ = [j for j in np.argsort(diffs) if diffs[j] / np.amax(diffs) > 0.4]
            for spot_indx in arr_:
                spot = spots[spot_indx]
                x1, y1, w, h = spot

                spot_crop = frame[y1:y1 + h, x1:x1 + w, :]

                spot_status = empty_or_not(spot_crop)

                spots_status[spot_indx] = spot_status

        if frame_nmr % step == 0:
            previous_frame = frame.copy()

        for spot_indx, spot in enumerate(spots):
            spot_status = spots_status[spot_indx]
            x1, y1, w, h = spots[spot_indx]

            if spot_status:

                cv2.putText(frame, 's{}'.format(str(spot_indx)), (x1+10, y1+17), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2,cv2.LINE_AA)

                frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)
                
                L1.append(spot_indx) #returns all filled slots indexes

            
            else:

                cv2.putText(frame, 's{}'.format(str(spot_indx)), (x1+10, y1+17), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2,cv2.LINE_AA)

                frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 0, 255), 2)

                L2.append(spot_indx) #returns all empty slots indexes
                

        cv2.rectangle(frame, (80, 20), (550, 80), (0, 0, 0), -1)
        cv2.putText(frame, 'Available spots: {} / {}'.format(str(sum(spots_status)), str(len(spots_status))), (100, 60),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.imshow('frame', frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

        frame_nmr += 1

        #print("Current Available Slot => ",L1[0])
        return L1[0] 
        
        ret=False

    cap.release()
    cv2.destroyAllWindows()

#SPACE_COUNTER()