import pickle
import magic_card_detector as mcg


card_detector = mcg.MagicCardDetector('outputs')
card_detector.read_and_adjust_reference_images('images/')

hlist = []
for image in card_detector.reference_images:
    image.original = None
    image.clahe = None
    image.adjusted = None
    hlist.append(image)

with open('allhashes.dat', 'wb') as f:
    pickle.dump(hlist, f)