import os
from PIL import Image

if os.path.isfile('list.txt'):
    os.remove('list.txt')

with open('list.txt','w') as f:
    for root, _, files in os.walk('./images/'):
        for name in files:
            f.write(name.replace('_ink_.png',''))
            f.write('\n')
f.close()
