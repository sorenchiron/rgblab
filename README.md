# rgblab
RGB and CIE-Lab color space conversion, based on existing code


Usage:
```python
from rgblab import rgb2lab

img = imageio.imread('xxxrgb.png')

lab = rgb2lab(img)

L = lab[...,0] 
a = lab[...,1] 
b = lab[...,2] 

```
