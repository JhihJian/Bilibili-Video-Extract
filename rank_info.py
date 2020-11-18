import requests
# return av list 数码，知识，影视 三个区
def get_rank_videos():
    knowledge_url='https://api.bilibili.com/x/web-interface/ranking/v2?rid=36&type=all'
    digital_url='https://api.bilibili.com/x/web-interface/ranking/v2?rid=188&type=all'
    movies_url='https://api.bilibili.com/x/web-interface/ranking/v2?rid=181&type=all'
    urls=[knowledge_url,digital_url,movies_url]
    video_aids = []
    for url in urls:
        r = requests.get(url, auth=('user', 'pass'))
        if r.status_code!=200:
            print("status code != 200 url:"+url)
        data=r.json()
        for video in data['data']['list']:
            video_aids.append(video['aid'])
            if 'others' in video:
                for other in video['others']:
                    video_aids.append(other['aid'])
    return video_aids
if __name__ == '__main__':
    print(get_rank_videos())

