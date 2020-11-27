# This is a sample Python script.
import download_tool
import keyframes_extract
import rank_info
import  av_store
import os
import shutil
import time
import ctypes
import os
import platform
import sys

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
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

if __name__ == '__main__':
    av_set=av_store.load_av_set(data_path)
    print('already download av size:' + str(len(av_set)))
    av_new_list=rank_info.get_rank_videos()
    for av in av_new_list:
        while(get_free_space_gb(target_dir) < 1000):
            print("free space just:" + str(get_free_space_gb(target_dir)) + " gb,wait clean")
            time.sleep(4)

        if str(av) not in av_set:
            base_dir=download_tool.download_video(str(av),target_dir)
            video_path_list=get_video_path(base_dir)
            # 先只处理一个
            print(video_path_list[0])
            frames_dir_path=os.path.join(base_dir,str(av))
            #keyframes_extract.extract(video_path_list[0],frames_dir_path)
            #frames_ocr_process(frames_dir_path)
            av_set.add(av)
            av_store.append_av_set(str(av),data_path)
            # shutil.rmtree(base_dir)
            print(base_dir+ "has been delete")
            time.sleep(2)
        else:
            print("already download av "+str(av)+",jump it")
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
