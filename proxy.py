import requests
import fakerHeaders

def get_proxy():
    return requests.get("http://centos.jh:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://centos.jh:5010/delete/?proxy={}".format(proxy))

def proxy_post(url,head,data):
    retry_count = 5
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            response = requests.session().post(url, headers=head, data=data, timeout=9, proxies={"http": "http://{}".format(proxy)})
            return response
        except Exception:
            retry_count -= 1
    delete_proxy(proxy)
    return None

def proxy_get(url):
    # ....
    retry_count = 5
    proxy = get_proxy().get("proxy")
    hideHeader = fakerHeaders.getFakerHeaders()
    head = {'User-Agent': hideHeader}
    while retry_count > 0:
        try:
            html = requests.get(url,headers=head, proxies={"http": "http://{}".format(proxy)})
            # 使用代理访问
            return html
        except Exception:
            retry_count -= 1
    # 删除代理池中代理
    delete_proxy(proxy)
    print("get fail")
    return None
if __name__ == '__main__':
    url="https://api.bilibili.com/x/v2/reply?&pn=6&type=1&oid=669797737"
    import fakerHeaders

    hideHeader = fakerHeaders.getFakerHeaders()
    head = {'User-Agent': hideHeader}
    proxy = get_proxy().get("proxy")
    html = requests.get(url,headers=head, proxies={"http": "http://{}".format(proxy)})
    print(html.text)