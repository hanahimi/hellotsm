#-*-coding:UTF-8
'''
Created on 2018年8月28日
@author: mipapapa
'''
import numpy as np

class LocPose:
    def __init__(self):
        self.name = None
        # x,y,z,yawr
        self.data = np.zeros((4), np.float)
        """
        ax.arrow(pose.data[0], pose.data[1], 
                np.cos(pose.data[3])*0.2, np.sin(pose.data[3])*0.2,
                head_width=0.1, head_length=0.1)
        """
def load_pose(pose_path):
    pose_dataset = []
    with open(pose_path, "r") as fr:
        fr.readline()
        fr.readline()
        for log in fr:
            items = log.strip("\n").split(" ")
            pose_tmp = LocPose()
            pose_tmp.name = items[0]
            data = [float(item) for item in items[1:]]
            # 四元数转欧拉角
            w,x,y,z = data[3:]
            a1 = np.arctan2(2*(w*z+x*y), 1-2*(z*z+x*x)) # yawr
#             a2 = np.arctan(2*(w*x-y*z))
#             a3 = np.arctan2(2*(w*y+z*x), 1-2*(x*x+y*y))
            pose_tmp.data[:3] = data[:3]
            pose_tmp.data[3:] = [a1]
            
            pose_dataset.append(pose_tmp)
    return pose_dataset

def main():
    import matplotlib.pyplot as plt
    pose_path = r"F:\dataset\DeepLoc\semantic\ts_seq1\poses.txt"
    pose_dataset = load_pose(pose_path)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    pose_data_arr = []
    for i in range(len(pose_dataset)):
        pose = pose_dataset[i]
        pose_data_arr.append(pose.data)
        ax.arrow(pose.data[0], pose.data[1], np.cos(pose.data[3])*0.2, np.sin(pose.data[3])*0.2,
                 head_width=0.1, head_length=0.1)
    pose_data_arr = np.array(pose_data_arr)
    plt.plot(pose_data_arr[:,0], pose_data_arr[:,1], "r-")
    plt.show()
    
if __name__=="__main__":
    pass
    main()

