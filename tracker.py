import cv2
import mediapipe as mp
import time

class handDetector:
	def __init__(self, mode=False, max_hands=2, detection_confidence=0.5, tracking_confidence=0.5):
		self.mode = mode
		self.max_hands = max_hands
		self.detection_confidence = detection_confidence
		self.tracking_confidence = tracking_confidence
		
		self.mpHands = mp.solutions.hands
		self.hands = self.mpHands.Hands(self.mode, self.max_hands, self.detection_confidence, self.tracking_confidence)
		self.mpDraw = mp.solutions.drawing_utils

	def detectHands(self, img, draw=True):
		imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		self.results = self.hands.process(imgRGB)

		if self.results.multi_hand_landmarks:
			for handLms in self.results.multi_hand_landmarks:
				if draw:
					self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
		return img

	def findPositions(self, img, handNumber=0, draw=True):

		lmList = [] 

		if self.results.multi_hand_landmarks:
			hand = self.results.multi_hand_landmarks[handNumber]

			for handLms in self.results.multi_hand_landmarks:
				for id, lm in enumerate(hand.landmark):
					h, w, c = img.shape
					cx, cy = int(lm.x*w), int(lm.y*h)
					lmList.append([id, cx, cy])
					

		return lmList
	def drawOnLandmark(self, img, landmarkNumber, landmarkList, handNumber=0):
		cv2.circle(img, (landmarkList[landmarkNumber][1], landmarkList[landmarkNumber][2]), 15, (255,0, 255), cv2.FILLED)
def main():
	previousTime = 0
	currentTime = 0
	cap = cv2.VideoCapture(0)
	detector = handDetector()
	
	while True:
		success, img = cap.read()
		img = detector.detectHands(img)

		landMarkList = detector.findPositions(img)
		if len(landMarkList) != 0:
			print(landMarkList[4])
			detector.drawOnLandmark(img, 4, landMarkList)

		currentTime = time.time()
		fps = 1/(currentTime-previousTime)
		previousTime = currentTime
		# print(fps)

		img = cv2.flip(img, 1)
		# cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (0, 255, 0), 3)		
		cv2.imshow("Video", img)
		if cv2.waitKey(1) == ord('q'):
			break

if __name__ == '__main__':
	main()