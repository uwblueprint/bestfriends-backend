import cv2

class CatDetector:
	_CLASSIFIER_XML = "haarcascade_frontalcatface.xml"

	def __init__(self):
		self._detector = cv2.CascadeClassifier(self._CLASSIFIER_XML)

	def get_num_cats(self, file_name):
		image = cv2.imread(file_name, 0)
		cv2.imshow('image', image)
		cv2.waitKey(0)

		rects = self._detector.detectMultiScale(image, scaleFactor=1.3,
			minNeighbors=13, minSize=(10, 10))
		
		return len(rects)

cat_detector = CatDetector()
print(cat_detector.get_num_cats("cat3.jpg"))
