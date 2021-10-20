import re

x = 'https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_82,h_82,c_pad,b_white,d_photoiscoming.png/LMCode/18868588.jpg'

y = re.sub('_\d+', '_400', x)
print(x)
print(y)