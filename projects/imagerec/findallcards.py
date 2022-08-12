import cv2
import json
from PIL import Image
from pytesseract import pytesseract
from cydifflib import get_close_matches
import time
import datetime
import os
import fiximage

def get_name(img):
    global all_cards
    x,y = 775, 270
    w,h = 375, 540
    img = cv2.imread('test.jpg')
    #img = img[y:y+h, x:x+w]
    #img = cv2.resize(img, (2*w, 2*h))
    img = fiximage.grayscale(img)
    #img = fiximage.thresholding(img)

    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0,255,0), 3)

    # Passing the image object to image_to_string() function
    # This function will extract the text from the image
    text = pytesseract.image_to_string(img)
    print(text)
    exit()
    # Displaying the extracted text
    if text.strip() == '':
        return 'None'
    card_name = text.split('\n')[0]
    try:
        return get_close_matches(card_name, all_cards)[0]
    except IndexError:
        return 'None'

with open('all_cards.txt', 'r', encoding="utf-8") as f:
    all_cards = f.read().split('\n')

start = time.time()

filename = 'video.mp4'
print(filename)
vidcap = cv2.VideoCapture(filename)
ret,frame = vidcap.read()
name = get_name(frame)
if name != 'None':
    print(name)
while ret:
    ret,frame = vidcap.read()
    name = get_name(frame)
    if name != 'None':
        print(name)
        cv2.imwrite('output/'+name+'.png', frame)

end = time.time()
elapsed = end-start
print(str(datetime.timedelta(seconds=elapsed)))