import os
import cv2

import numpy as np

from blurry_check import BlurryCheck

CLEAR_DIR = './clear_photos/'
BLURRY_DIR = './blurry_photos/'

blurry_checker = BlurryCheck()

def train_laplacian():
	clear_photos = [f for f in os.listdir(CLEAR_DIR) if not f.startswith(".")]
	blurry_photos = [f for f in os.listdir(BLURRY_DIR) if not f.startswith(".")]

	cur_perf = 0
	max_perf = -float("inf")
	best_threshold = 100

	for threshold in range (80, 210, 10):
		blurry_checker.set_threshold(threshold)
		for photo in clear_photos:
			file_name = CLEAR_DIR + photo
			cur_perf += judge_photo(file_name, True)

		for photo in blurry_photos:
			file_name = BLURRY_DIR + photo
			cur_perf += judge_photo(file_name, False)

		if cur_perf > max_perf:
			best_threshold = threshold
			max_perf = cur_perf

	return best_threshold

def judge_photo(file_name, expected):
	is_blurry = blurry_checker.is_blurry(cv2.imread(file_name, 0))
	return int(expected == is_blurry)

print(train_laplacian())