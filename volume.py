import cv2
import time
import tracker as t
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]


wCam, hCam = 640, 480


previousTime = 0
currentTime = 0


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = t.handDetector(detection_confidence=0.8)

while True:
	success, img = cap.read()
	img = detector.detectHands(img, draw=True)

	landmarkList = detector.findPositions(img, draw=False)
	if len(landmarkList) != 0:
		# print(landmarkList[4], landmarkList[8])

		x1, y1 = landmarkList[4][1], landmarkList[4][2]
		x2, y2 = landmarkList[8][1], landmarkList[8][2]
		x3, y3 = landmarkList[12][1], landmarkList[12][2]
		cx, cy = (x1+x2)//2, (y1+y2)//2
		cv2.circle(img, (x1, y1), 10, (255,0,0), cv2.FILLED)
		cv2.circle(img, (x2, y2), 10, (255,0,0), cv2.FILLED)
		cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
		cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)
		cv2.line(img, (x1, y1), (x3, y3),(0,255,0), 2)
		length = math.hypot(x2-x1, y2-y1)
		print('Line length: ', int(length))

		vol = np.interp(length, [20, 160], [minVol, maxVol])
		print("volume: ", vol)

		if length<50:
			cv2.circle(img, (cx, cy), 5, (0,255,0), cv2.FILLED)

		volume.SetMasterVolumeLevel(vol, None)
		# time.sleep(0.1)

	img = cv2.flip(img, 1)
	cv2.imshow("Video", img)
	if cv2.waitKey(1) == ord('q'):
		break