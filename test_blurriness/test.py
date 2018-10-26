import cv2
import sys

LAPLACIAN_THRESHOLD = 100

def isBlurry(img):
	if cv2.Laplacian(img, cv2.CV_64F).var() < LAPLACIAN_THRESHOLD:
		return True
	else:
		return False

print('Blurry') if isBlurry(cv2.imread(sys.argv[1], 0)) else print('Good')

