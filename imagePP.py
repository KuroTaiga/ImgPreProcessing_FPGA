# -*- coding: utf-8 -*-
"""
This is contains functions about image pre-processing

@author: dongj1
"""
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt


# ToDo: Change the parameters/add in auto changing parameters for the image
def process_Img(imgName,folderPath): 
    """
    This is function to call for processing raw images
    Input: imgName -- Name of the image
           folderPath -- The folder that contains the image
    Output: A set that contains the coordinates of the stars found: (rows,columns)
    """
    imgPath = os.path.join(folderPath,imgName+'.jpg')
    resultPath = os.path.join(folderPath,imgName+'_result.jpg')
    erodPath = os.path.join(folderPath,imgName+'_erod.jpg')
    f = []
    fgrey = []
    result = []
    f = cv2.imread(imgPath)
    fgrey = f
    fgrey = cv2.cvtColor(f,cv2.COLOR_RGB2GRAY)
    print('imput image')
    plt.imshow(fgrey,'gray')
    plt.show()
    rows = np.shape(fgrey)[0]
    columns = np.shape(fgrey)[1]
    size = 36 # size of the mask (# of pixels from each size)
    paddedgrey = np.zeros([rows+2*size,columns+2*size])
    paddedgrey[size:rows+size,size:columns+size] = fgrey
    print('Padded: ')
    plt.imshow(paddedgrey,'gray')
    plt.show()
    result = np.zeros(np.shape(fgrey))
    count = 0
    for i in range(size,rows+size):
        for j in range(size,columns+size):
            currImg = paddedgrey[i-size:i+size,j-size:j+size]
            currPixel = paddedgrey[i,j]
            imgAve = np.mean(currImg)
            imgVar = np.var(currImg)
            if (currPixel-imgAve)*(currPixel-imgAve) > 10*imgVar:
                result[i-size,j-size] = 0
                count+=1
            else:
                result[i-size,j-size] = 255
    cv2.imwrite(resultPath,result)
    print('Noisy Result')
    plt.imshow(result,'gray')
    plt.show()
    erod_img = erod(result,erodPath)
    print('Erod Img')
    plt.imshow(erod_img,'gray')
    plt.show()
    return getStarPoints(erod_img,np.shape(erod_img)[0],np.shape(erod_img)[1])

def erod(img,resultPath):
    fgrey = img
    result = fgrey
    kernel = np.ones((3,3), np.uint8)
    erodeKern = np.ones((4,4), np.uint8)
    erosion = cv2.dilate(result,kernel,iterations = 2)
    erosion = cv2.erode(erosion,erodeKern,iterations = 2)
    cv2.imwrite(resultPath,erosion)
    return erosion

def getStarPoints(f,rows,columns):
    result = set()
    temp = set()
    disgard = set()
    blob = set()
    currR = 0
    currC = 0
    count = 0
    for i in range(1,rows):
        for j in range (1,columns):
            currPixel = f[i,j]
            if currPixel==0:
                temp.add((i,j))
                
    while(len(temp)>0):
        count+=1
        blob.clear()
        disgard.clear()
        curr = temp.pop()
        blob.add(curr)
        currR = curr[0]
        currC = curr[1]
        for point in temp:
            if point not in disgard:
                if (np.abs(point[0]-currR)<=50 and np.abs(point[1]-currC)<=50):
                    blob.add(point)
                    disgard.add(point)
        for point in disgard:
            temp.discard(point)
        result.add(ave2d(blob))
    return result

def ave2d(pointSet):
    xSum = 0
    ySum = 0
    for p in pointSet:
        xSum += p[0]
        ySum += p[1]
    return (xSum/len(pointSet),ySum/len(pointSet))

"""    
Test Code
imageN = '3'
cwd = os.getcwd()
print(cwd)
print('Result points:')
print(process_Img(imageN,cwd))


#erodPath = os.path.join(cwd,imageN+'_erod.jpg')
#fe = []
#fe = cv2.imread(erodPath)
#plt.imshow(fe,'gray')
#plt.show()       
#getStarPoints(fe,np.shape(fe)[0],np.shape(fe)[1])
"""