from PIL import Image
import numpy as np

w, h = 512, 512
for i in range(512):
    data = 255*np.ones((h, w, 3), dtype=np.uint8)
    data[0:i, 0:256] = [255, 0, 255] # red patch in upper left
    img = Image.fromarray(data, 'RGB')
    img.save('images/img' + str(i) + '.jpeg')
    #img.show()