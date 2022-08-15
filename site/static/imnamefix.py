from os import listdir

for file in listdir('color_images2'):
    name = list(file.split('.')[0])
    name.sort()
    name = ''.join(name)
    with open('color_images2/'+file, 'rb') as f:
        with open('color_images/'+name+'.png', 'wb') as f2:
            f2.write(f.read())
