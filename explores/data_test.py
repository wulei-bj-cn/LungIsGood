#coding=utf-8
import SimpleITK as sitk
import numpy as np
import PIL.Image as Image
import cv2
import math
import pickle

mhd_path="1.3.6.1.4.1.14519.5.2.1.6279.6001.100225287222365663678666836860/1.3.6.1.4.1.14519.5.2.1.6279.6001.100225287222365663678666836860.mhd"
raw_path="1.3.6.1.4.1.14519.5.2.1.6279.6001.100225287222365663678666836860/1.3.6.1.4.1.14519.5.2.1.6279.6001.100225287222365663678666836860.raw"
center = (-128.6994211,-175.3192718,-298.3875064)
diameter = 5.651470635


class ImageDesc(object):
    def __init__(self,
                 image_obj,
                 image_label,
                 layer_num,
                 layer_diameter,
                 layer_center):
        self.image_obj = image_obj #图像的物理尺寸
        self.image_label = image_label #图像中是否有结节，1有0没有
        self.layer_num = layer_num #图像是raw的第几层
        self.layer_diameter = layer_diameter #该层图像中结节的直径大小
        self.layer_center = layer_center #该层图像中结节的中心点坐标


def get_mhd(mhd_path):
    image = sitk.ReadImage(mhd_path)#从mhd文件读取图像信息
    #z是分层，image_array中是z个(y,x)的图片
    image_array = sitk.GetArrayFromImage(image) # z, y, x
    #spacing的x,y用于计算每个像素点的物理尺寸，z是该层的厚度
    spacing = image.GetSpacing()#x, y, z
    origin = image.GetOrigin()# x, y, z
    #可以把每层的图像单独保存下来
    outpath="image"
    index = 0
    center_layer,end_layer,start_layer = get_z(origin,spacing,center,diameter)
    image_list = []
    for img_item in image_array:
        index = index + 1
        image_obj = img_item*spacing[0] #图像的物理尺寸
        if index >= start_layer and index <= end_layer:
            image_label = 1 #该张图像中是否有结节，1：有，0：没有
            #计算该张图像中结节的半径
            layer_diameter = get_layer_diameter(index,center_layer,diameter,spacing)    
            layer_center = (center[0],center[1])
        else:
            image_label = 0
            layer_diameter = 0
            layer_center = ()
        image_res = ImageDesc(image_obj,image_label,index,layer_diameter,layer_center)    
        image_list.append(image_res)
    with open('image_obj.pk', 'wb') as f:
        pickle.dump(image_list,f)

#读取保存的数据,考虑到image_obj比较大，也可以直接从mhd文件再读一次，不需要存储也行
def load_image_obj(fn):
    with open(fn, 'rb') as f:
        data = pickle.load(f)
    print(len(data))
    for item in data:
        print(item.image_obj)
        print(item.image_label)
        print(item.layer_num)
        print(item.layer_diameter)
        print(item.layer_center)
 
    

#获取有结节的层的结节的直径大小
def get_layer_diameter(index,center_layer,diameter,spacing):
    layer_diameter = diameter
    if not index == center_layer:
        layer_diameter = ((diameter**2/4-abs(index-center_layer)*spacing[2])**0.5)*2
    return layer_diameter


#获取哪几层有结节存在
def get_z(origin,spacing,center,diameter):
    #结节中心点所在的层数，所得结果向下取整
    center_layer = math.floor((center[2] - origin[2])/spacing[2])
    #根据半径计算结节存在于中心层上下多少层
    end_layer = math.floor((center[2]+diameter/2-origin[2])/spacing[2])
    start_layer = math.floor((center[2]-diameter/2-origin[2])/spacing[2])
    return center_layer,end_layer,start_layer


if __name__ == "__main__":
    get_mhd(mhd_path)
    load_image_obj("image_obj.pk")
