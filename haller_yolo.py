import torch
from torchvision.ops import nms
import cv2
import numpy as np
import datetime
import pandas as pd
import time
import typing


def draw_label(img, detection):
    confidence = detection[:, -2]
    detection = np.rint(detection).astype('int')
    for i in range(len(detection)):
        box = detection[i, :4]
        pt1 = tuple(box[:2])
        pt2 = tuple(box[2:])
        label_idx = detection[i, -1]
        label = names[label_idx] + f" {float(confidence[i]):.2f}"
        cv2.rectangle(img, pt1, pt2, (255, 0, 0), 1)
        cv2.putText(img, label, pt1, cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
    return img


class Detections:
    def __init__(self, use_nms=True):
        self.measurements: np.ndarray = np.empty((0, 6), dtype='float32')
        self.confidence_tr = 0.3
        self.use_nms = use_nms

    def add_measurement(self, detection):
        if self.use_nms:
            self.measurements = np.vstack((self.measurements, detection.values[:, :-1].astype('float32')))
            if len(self.measurements) > 30:
                self.measurements = self.measurements[-30:]
                return self.nms()
            else:
                return None
        else:
            return detection.values[:, :-1].astype('float32')

    def nms(self):
        d = self.measurements[:, :-2]
        c = self.measurements[:, -2]

        d_tensor = torch.tensor(d)
        c_tensor = torch.tensor(c)

        nms_result = nms(d_tensor, c_tensor, 0.1)
        rows = [n for n in nms_result if self.measurements[n, -2] > self.confidence_tr]
        return np.reshape(self.measurements[rows, :], (-1, 6))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    model = torch.hub.load('./', 'custom', path='haller/haller_net14/weights/best.pt', source='local', device='cuda:0')

    cap = cv2.VideoCapture(0)

    names = model.names
    detections1: Detections = Detections(use_nms=False)
    detections2: Detections = Detections(use_nms=False)

    while True:
        rval, img = cap.read()
        img_copy = np.copy(img)

        result = model(img)
        df = result.pandas().xyxy[0]
        if len(df) > 0:
            boxes1 = detections1.add_measurement(df)
            if boxes1 is not None:
                draw_label(img, boxes1)

            boxes2 = detections2.add_measurement(df)
            if boxes2 is not None:
                draw_label(img_copy, boxes2)

        cv2.imshow('with nms', img)
        cv2.imshow('no nms', img_copy)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

