# This is a sample Python script.
import pika

import download_tool
import rank_info
import  av_store
import os
import shutil
import time
import ctypes
import os
import platform
import sys
import comments_download
import logging
import json

target_dir="/opt/video_download"
data_path=r"av_set.txt"
base_url="https://www.bilibili.com/video/av"
ocr_input_dir="/opt/ocr-files/images"

if not os.path.exists(target_dir):
    os.mkdir(target_dir)


def get_video_path(base_dir):
    result=[]
    videos_dir=os.path.join(base_dir,"Videos")
    for file in os.listdir(videos_dir):
        if file.endswith(".mp4"):
            result.append(os.path.join(videos_dir, file))
    return result
def get_chat_path(base_dir):
    result=[]
    videos_dir=os.path.join(base_dir,"Videos")
    for file in os.listdir(videos_dir):
        if file.endswith(".xml"):
            result.append(os.path.join(videos_dir, file))
    return result
# def frames_ocr_process(frames_dir_path):
#     shutil.copytree(frames_dir_path,os.path.join(ocr_input_dir,os.path.basename(frames_dir_path)))

def get_free_space_gb(folder):
    """ Return folder/drive free space (in bytes)
    """
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value/1024/1024/1024
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize/1024/1024/1024.

def create_message(av,path):
    return json.dumps({'av':av,'path':path})

if __name__ == '__main__':
    # mq 过程
    param=pika.URLParameters('amqp://biliu:123456@centos.jh:5672')
    param._heartbeat=0
    connection = pika.BlockingConnection(param)
    video_queue_name="videoPathQueue"
    chat_queue_name="chatPathQueue"
    video_channel = connection.channel()
    chat_channel = connection.channel()
    video_channel.queue_declare(queue=video_queue_name)
    chat_channel.queue_declare(queue=chat_queue_name)

    # mq 过程
    av_set=av_store.load_av_set(data_path)
    logging.info('already download av size:' + str(len(av_set)))
    av_new_list=rank_info.get_rank_videos()
    for av in av_new_list:
        while(get_free_space_gb(target_dir) < 5):
            print("free space just:" + str(get_free_space_gb(target_dir)) + " gb,wait clean")
            time.sleep(4)

        if str(av) not in av_set:
            #下载视频
            base_dir=download_tool.download_video(str(av),target_dir)
            video_path_list=get_video_path(base_dir)
            chat_path_list=get_chat_path(base_dir)
            logging.info("download av:" + str(av) +"video size:" + str((len(video_path_list))))
            # TODO
            for video_path in video_path_list:
                video_channel.basic_publish(exchange='',
                                            routing_key=video_queue_name,
                                            body=create_message(str(av),video_path))
            for chat_path in chat_path_list:
                chat_channel.basic_publish(exchange='',
                                            routing_key=chat_queue_name,
                                            body=create_message(str(av),chat_path))
            # 下载评论
            comments_download.SpiderComment(av)
            # 增加av号到已下载列表
            av_set.add(av)
            av_store.append_av_set(str(av),data_path)
            time.sleep(2)
        else:
            logging.info("already download av "+str(av)+",jump it")
    connection.close()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
