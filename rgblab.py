# ported by CHEN S.Y.
# code based on https://gist.github.com/manojpandey/f5ece715132c572c80421febebaf66ae

# RGB to Lab conversion

# Step 1: RGB to XYZ
#         http://www.easyrgb.com/index.php?X=MATH&H=02#text2
# Step 2: XYZ to Lab
#         http://www.easyrgb.com/index.php?X=MATH&H=07#text7
import numpy as np

RGB2XYZ = np.array([
[ 0.4124 , 0.3576 , 0.1805 ],
[ 0.2126 , 0.7152 , 0.0722 ],
[ 0.0193 , 0.1192 , 0.9504 ],  # according to https://gist.github.com/manojpandey/f5ece715132c572c80421febebaf66ae#gistcomment-2987733
]).T

XYZ_ref = np.array([95.047,100.0,108.883])

XYZ2LAB = np.array([
[0  ,  116,    0],
[500, -500,    0],
[0  ,  200, -200],
]).T

XYZ2LAB_OFFSET = np.array([-16,0,0])

def rgb2lab(nhwc_rgb):
    '''input image value domain: [0,255]'''
    rgb = np.array(nhwc_rgb).astype(np.float32)
    RGB = rgb/255.0

    gt_04045_mask = RGB>0.04045
    leq_04045_mask = (gt_04045_mask == False)

    RGB[gt_04045_mask] = ((RGB[gt_04045_mask]+0.055)/1.055)**2.4
    RGB[leq_04045_mask] = RGB[leq_04045_mask] / 12.92

    RGB = RGB*100

    XYZ = np.matmul(RGB,RGB2XYZ)

    XYZ = XYZ.round(4)

    XYZ = XYZ / XYZ_ref

    gt_008856_mask = XYZ > 0.008856
    leq_008856_mask = (gt_008856_mask == False)

    XYZ[gt_008856_mask] = XYZ[gt_008856_mask] ** (0.3333333333333333)
    XYZ[leq_008856_mask] = 7.787 * XYZ[leq_008856_mask] + (16.0 / 116.0)

    LAB = np.matmul(XYZ,XYZ2LAB) + XYZ2LAB_OFFSET

    LAB = LAB.round(4)

    return LAB

def rgb2lab_legacy(inputColor):
    '''accept only single RGB pixel input'''
    num=0
    RGB=[0,0,0]
    for value in inputColor:
        value = float(value) / 255

        if value > 0.04045:
            value = ((value + 0.055) / 1.055) ** 2.4
        else:
            value = value / 12.92

        RGB[num] = value * 100
        num = num + 1

    XYZ = [0, 0, 0, ]

    X = RGB[0] * 0.4124 + RGB[1] * 0.3576 + RGB[2] * 0.1805
    Y = RGB[0] * 0.2126 + RGB[1] * 0.7152 + RGB[2] * 0.0722
    Z = RGB[0] * 0.0193 + RGB[1] * 0.1192 + RGB[2] * 0.9504 # according to https://gist.github.com/manojpandey/f5ece715132c572c80421febebaf66ae#gistcomment-2987733
    XYZ[0] = round(X, 4)
    XYZ[1] = round(Y, 4)
    XYZ[2] = round(Z, 4)

    # Observer= 2°, Illuminant= D65
    XYZ[0] = float(XYZ[0]) / 95.047         # ref_X =  95.047
    XYZ[1] = float(XYZ[1]) / 100.0          # ref_Y = 100.000
    XYZ[2] = float(XYZ[2]) / 108.883        # ref_Z = 108.883

    num = 0
    for value in XYZ:

        if value > 0.008856:
            value = value ** (0.3333333333333333)
        else:
            value = (7.787 * value) + (16.0 / 116.0)

        XYZ[num] = value
        num = num + 1

    Lab = [0, 0, 0]

    L = (116 * XYZ[1]) - 16
    a = 500 * (XYZ[0] - XYZ[1])
    b = 200 * (XYZ[1] - XYZ[2])

    Lab[0] = round(L, 4)
    Lab[1] = round(a, 4)
    Lab[2] = round(b, 4)

    return Lab
