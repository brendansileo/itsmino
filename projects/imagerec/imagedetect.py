import cv2
import numpy as np
import imagehash
import datetime
import time
from PIL import Image
from threading import Thread
import os

locks = 0
max_locks = 50
found = False

def is_similar(image1, image2):
    image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
    image1 = Image.fromarray(image1)
    hash1 = imagehash.average_hash(image1) 
    image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
    image2 = Image.fromarray(image2)
    hash2 = imagehash.average_hash(image2)
    cutoff = 10  # maximum bits that could be different between the hashes. 
    return hash1 - hash2 < cutoff

def is_card_there(target, frame, id):
    global locks
    global found
    global video_name
    # Initiate SIFT detector
    sift = cv2.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(target,None)
    kp2, des2 = sift.detectAndCompute(frame,None)
    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params,search_params)
    matches = flann.knnMatch(des1,des2,k=2)
    count = 0
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.7*n.distance:
            count += 1
    if count > 500:
        print('matches: '+str(count))
        cv2.imwrite(video_name+".jpg", frame)
        found = True
        time.sleep(10)
    locks -= 1

def runner(id):
    global found
    global pool
    global locks
    count = -1
    while not found:
        try:
            frame = pool.pop()
        except:
            continue
        count += 1
        if count == 0 or not is_similar(last_frame, frame):
            last_frame = frame
            t = Thread(target=is_card_there,args=(target, frame, count))
            while locks > max_locks:
                pass
            locks += 1
            t.daemon = True
            t.start()

start = time.time()

pool = []
#videos = os.listdir('videos')
video_name = None
for filename in ['video.mp4']:#videos:
    print(filename)
    video_name = filename
    vidcap = cv2.VideoCapture(filename)
    target = cv2.imread('targets/crypt.jpg')

    t1 = Thread(target=runner,args=(1,))
    t2 = Thread(target=runner,args=(2,))
    t3= Thread(target=runner,args=(3,))

    t1.daemon = True
    t2.daemon = True
    t3.daemon = True

    t1.start()
    t2.start()
    t3.start()

    ret,frame = vidcap.read()
    pool.append(frame)
    count = 0
    while ret and not found:
        if len(pool) < 15:
            ret,frame = vidcap.read()
            pool.append((frame))
            count += 1
            print(count)
    if not found:
        x = 'not found'
    else:
        x = 'found'
    end = time.time()
    elapsed = end-start
    with open('output.txt', 'a+') as f:
        f.write(filename+'\n')
        f.write(x+'\n')
        f.write(str(datetime.timedelta(seconds=elapsed))+'\n\n')
