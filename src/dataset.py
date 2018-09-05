#coding:UTF-8
'''
Created on 2018年9月2日-下午12:00:16
author: Gary-W
载入一组数据(分割图像，pose文件)，转换为语义特征
'''
import os
from util.dataio import get_filelist
from pose import load_pose
from feature import load_label_img, Feature
import numpy as np
from tqdm import tqdm

def load_feat_dataset(data_dir):
    
    labels = os.path.join(data_dir, "labels")
    label_imgs = get_filelist(labels,".png")
    poses = load_pose(os.path.join(data_dir, "poses.txt"))
    
    img_name_dict = {}
    for i in range(len(label_imgs)):
        img_name = os.path.split(label_imgs[i])[-1][:-4]
        img_name_dict[img_name] = label_imgs[i]
    
    seg_feature_dataset = []
    cnt, step = 0, 1
    for i in tqdm(range(len(poses))):
        pose = poses[i]
        if i == 0:
            x_last, y_last = pose.data[0], pose.data[1]
        acc_veh_odm = np.sqrt((pose.data[0] - x_last)**2 + (pose.data[1] - y_last)**2)
        x_last, y_last = pose.data[0], pose.data[1]
        if pose.name in img_name_dict:
            if cnt % step == 0:
                _img_path = img_name_dict[pose.name]
                _hist_l, _hist_c, _hist_r = load_label_img(_img_path)
                _feature = Feature()
                _feature.parse(pose, _hist_l, _hist_c, _hist_r, acc_veh_odm)
                seg_feature_dataset.append(_feature)
            cnt += 1

    return seg_feature_dataset

def load_feature_npy(npy_file):
    # 只要数据结构不变即可，feature的方法修改不影响npy的恢复
    seg_feature_dataset = np.load(npy_file)
    return seg_feature_dataset

def main():
    data_dir = r"D:\Dataset\public_data\DeepLoc\tsm_demo\ts_seq1"
    seg_feature_dataset = load_feat_dataset(data_dir)
    print(len(seg_feature_dataset))
    npy_file = os.path.join(data_dir, "feature.npy")
    np.save(npy_file, seg_feature_dataset)
    seg_feature_dataset = load_feature_npy(npy_file)
    print(len(seg_feature_dataset))


if __name__=="__main__":
    main()
    
    
    
    

