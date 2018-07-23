#coding=utf-8
import SimpleITK as sitk
import numpy as np
import PIL.Image as Image
import cv2
mhd_path="1.3.6.1.4.1.14519.5.2.1.6279.6001.100225287222365663678666836860/1.3.6.1.4.1.14519.5.2.1.6279.6001.100225287222365663678666836860.mhd"
raw_path="1.3.6.1.4.1.14519.5.2.1.6279.6001.100225287222365663678666836860/1.3.6.1.4.1.14519.5.2.1.6279.6001.100225287222365663678666836860.raw"


def get_mhd(mhd_path):
    image = sitk.ReadImage(mhd_path)#从mhd文件读取图像信息
    #z是分层，image_array中是z个(y,x)的图片
    image_array = sitk.GetArrayFromImage(image) # z, y, x
    print(image_array.shape)
    """
    #查看每层图像的像素值
    for item in image_array:
        print(item)
        break
    """
    
    #可以把每层的图像单独保存下来
    outpath="image"
    index = -1
    for img_item in image_array:
        index = index + 1
        cv2.imwrite("%s/%d.png"%(outpath,index),img_item)
    
    origin = image.GetOrigin()# x, y, z
    print(origin)
    #spacing的x,y用于计算每个像素点的物理尺寸，z是该层的厚度
    spacing = image.GetSpacing() #x, y, z
    print(spacing)




if __name__ == "__main__":
    get_mhd(mhd_path)
