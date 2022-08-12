# import the necessary packages
from imutils import paths
import argparse
import time
import sys
import cv2
import os
import numpy as np
import urllib.request
import requests
import json
import distance
import imagehash
from matplotlib import cm
from PIL import Image

import fiximage

# grab the base subdirectories for the needle paths, initialize the
# dictionary that will map the image hash to corresponding image,
# hashes, then start the timer

start = time.time()
all_images = {}

# loop over the haystack paths
with open('all_cards.txt', 'r') as f:
    cards = f.read().split('\n')
try:
	with open('temp.json', 'r') as f:
		all_images = json.loads(f.read())
except:
	pass
start_card = 'Warteye Witch'
started = False
for card in cards:
	print(card)
	if start_card != None and not started:
		if card == start_card:
			started = True
		else:
			continue
	r = requests.get('https://api.scryfall.com/cards/named?exact='+card.replace(' ','+'))
	try:
		prints_uri = r.json()['prints_search_uri']
	except:
		continue
	r = requests.get(prints_uri)
	prints = r.json()['data']
	for i, p in enumerate(prints):
		try:
			if 'image_uris' not in p:
				for face in p['card_faces']:
					url = face['image_uris']['normal']
					print(url)
					urllib.request.urlretrieve(url, 'images/'+card+str(i)+'.png')
					continue
					with urllib.request.urlopen(url) as url:
						arr = np.asarray(bytearray(url.read()), dtype=np.uint8)
					image = cv2.imdecode(arr, -1)
					# if the image is None then we could not load it from disk (so
					# skip it)
					if image is None:
						continue
					# convert the image to grayscale and compute the hash
					image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
					image = cv2.resize(image, (253, 354))
					image = fiximage.remove_noise(image)
					image = fiximage.deskew(image)
					image = Image.fromarray(np.uint8(cm.gist_earth(image)*255))
					imageHash = imagehash.average_hash(image)
					all_images[str(imageHash)] = card
			else:
				url = p['image_uris']['normal']
				print(url)
				urllib.request.urlretrieve(url, 'images/'+card+str(i)+'.png')
				continue
				with urllib.request.urlopen(url) as url:
					arr = np.asarray(bytearray(url.read()), dtype=np.uint8)
				image = cv2.imdecode(arr, -1)
				# if the image is None then we could not load it from disk (so
				# skip it)
				if image is None:
					continue
				# convert the image to grayscale and compute the hash
				image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				image = cv2.resize(image, (253, 354))
				image = fiximage.remove_noise(image)
				image = fiximage.deskew(image)
				image = Image.fromarray(np.uint8(cm.gist_earth(image)*255))
				imageHash = imagehash.average_hash(image)
				all_images[str(imageHash)] = card
		except:
			pass
	with open('temp.json', 'w') as f:
		f.write(json.dumps(all_images, indent=4))
with open('allimagehashesfixed.json', 'w') as f:
	f.write(json.dumps(all_images, indent=4))

end = time.time()
print('elapsed: '+str(end-start)+' seconds')
exit()

def find_card(image, all_hashes, count, last_results):
	print(count)
	# convert the image to grayscale and compute the hash
	cvim = image
	image = Image.fromarray(image)
	image_hash = imagehash.average_hash(image)
	image_hash = str(image_hash)
	# grab all image paths that match the hash
	if image_hash in all_hashes:
		if last_results == [(all_hashes[image_hash], 0)]:
			return [(all_hashes[image_hash], 0)]
		with open('results.txt', 'a+') as f:
			f.write('\n'+str(count)+'\n')
			f.write(all_hashes[image_hash]+'\n')
		return [(all_hashes[image_hash], 0)]
	else:
		options = []
		for hash, name in all_hashes.items():
			dist = distance.hamming(hash, image_hash)
			if dist <= 2:
				options.append((name, dist))
		if len(options) > 0:
			if last_results == options:
				return options
			with open('results.txt', 'a+') as f:
				f.write('\n'+str(count)+'\n')
				for option in options:
					f.write(option[0]+' '+str(option[1])+'\n')
			cv2.imwrite('output/'+str(count)+'.jpg', cvim)
		return options

def prep_frame(frame):
	x,y = 515, 183
	w,h = 253, 354
	#frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	image = frame[y:y+h, x:x+w]
	image = cv2.resize(image, (w, h))
	#image = fiximage.remove_noise(image)
	#image = fiximage.deskew(image)
	return image

with open('allimagehashes.json', 'r') as f:
	all_hashes = json.loads(f.read())
count = 0
vidcap = cv2.VideoCapture('video.mp4')
ret,frame = vidcap.read()
image = prep_frame(frame)
results = []
results = find_card(image, all_hashes, count, results)
count += 1
last_hash = imagehash.average_hash(Image.fromarray(frame))
while ret:
	print(count)
	if count == 1207:
		cv2.imwrite('test.jpg', frame)
		exit()
	else:
		ret,frame = vidcap.read()
		count += 1
	"""
	ret,frame = vidcap.read()
	hash = imagehash.average_hash(Image.fromarray(frame))
	if hash != last_hash:
		image = prep_frame(frame)
		results = find_card(image, all_hashes, count, results)
		last_hash = hash
	else:
		print('skipped', count)
	count += 1
	"""