import cv2
import sys

class BlurryCheck:
	def __init__(self, threshold=100):
		self.set_threshold(threshold)

	def set_threshold(self, threshold):
		self._LAPLACIAN_THRESHOLD = threshold

	def is_blurry(self, img):
		if cv2.Laplacian(img, cv2.CV_64F).var() < self._LAPLACIAN_THRESHOLD:
			return True
		else:
			return False

def simple_blurry():
	print(sys.argv[1])
	blurry_checker = BlurryCheck()
	print('Blurry') if blurry_checker.is_blurry(cv2.imread(sys.argv[1], 0)) else print('Good')


if __name__ == "__main__":
	simple_blurry()