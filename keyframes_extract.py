import cv2
from scipy.stats.stats import  pearsonr
import time
import os
from tqdm import tqdm,trange

# 相关性阈值
THREADHOLD = 0.99
# 裁剪高度
height=600
# 灰度 + 二值化
# 小于阈值的像素点灰度值不变，大于阈值的像素点置为0,其中参数3任取
def binarization(frame):
    ret,thresh = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY),127,255,cv2.THRESH_TOZERO)
    return thresh
def just_white(frame):
    hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV);
    mask1 = cv2.inRange(frame, (0, 0,200), (255, 255, 255))
    cv2.imwrite("target.png", mask1)

def is_diffent_frame(curr_frame,prev_frame):
    if curr_frame is not None and prev_frame is not None:
        # curr_frame=cv2.cvtColor(cur_frame, cv2.COLOR_BGR2LUV)
        # prev_frame=cv2.cvtColor(pre_frame, cv2.COLOR_BGR2LUV)
        # 将矩阵转换成向量。按行转换成向量，第一个参数就是矩阵元素的个数
        img0 = curr_frame.reshape(curr_frame.size, order='C')
        img1 = prev_frame.reshape(prev_frame.size, order='C')
        # corr = np.corrcoef(img0, img0)[0, 1]
        # 皮尔逊相关系数0.99为阈值
        corr = pearsonr(img0, img1)[0]
        return corr <= THREADHOLD
    return True
def extract(video_path,output_dir):

    #视频路径（相对路径)
    videopath = video_path
    #存帧的路径
    dir =output_dir
    print(dir)
    if not os.path.exists(dir):
        os.mkdir(dir)

    cap = cv2.VideoCapture(str(videopath))
    # 帧率
    fps = cap.get(cv2.CAP_PROP_FPS)
    #总帧数
    frames_num=cap.get(7)
    curr_frame = None
    prev_frame = None
    frame_coor = []
    frames = []
    #开始计时
    start_time = time.time()

    #计数读取的帧数
    i = 0
    #计数要保存的帧数
    num = 0
    # 间隔数
    interval_count = 0
    success, frame = cap.read()
    #不用while(success):换用tqdm可以展示进度条
    for i in trange(int(frames_num)-1):
        interval_count+=1
        if interval_count>=fps:
            interval_count=0
            frame_time = frame[height:,:,:]
            curr_frame = cv2.cvtColor(frame_time, cv2.COLOR_BGR2LUV)
            if is_diffent_frame(curr_frame,prev_frame):
                num += 1
                timestamps = [cap.get(cv2.CAP_PROP_POS_MSEC)]
                name = str(int(timestamps[0])) + ".jpg"
                cv2.imwrite(os.path.join(dir, name) ,frame_time)
                # 获得当前帧的时间戳
            prev_frame = curr_frame
        i = i + 1
        success, frame = cap.read()
    cap.release()
    end_time = time.time()
    print("耗时：",end_time - start_time,'s')
    print("读取帧数:",i)
    print("输出帧数:",num)



