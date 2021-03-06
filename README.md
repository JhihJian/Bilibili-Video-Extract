![](https://socialify.git.ci/JhihJian/Bilibili-Video-Extract/image?description=1&font=Raleway&language=1&owner=1&pattern=Circuit%20Board&stargazers=1&theme=Light)


### 部署方案
完整流程
```
# redis 的docekr 安装

docker pull redis:latest

docker run --name redis -d -p 6379:6379 redis redis-server --requirepass "password"

# 动态ip代理池

docker run --env DB_CONN=redis://:password@centos.jh:6379/0 -p 5010:5010 jhao104/proxy_pool:latest



mkdir -p /opt/ocr-docker/ocr-files

git clone https://github.com/JhihJian/Bilibili-Video-Extract.git

cd Bilibili-Video-Extract/Ocr-DockerFile

docker build -t paddleocr-jj:1.0.0 -f dockerFile .

docker run --name jjocr -v /opt/ocr-docker/ocr-files:/opt/PaddleOCR/ocr-files \
--network=host -it paddleocr-jj:1.0.0 /bin/bash

python3 /opt/PaddleOCR/ocr_main.py

ctrl+P+Q

cd ../DockerFile

docker build -t bili-extract:1.0.0 -f dockerFile .

docker run --name bili -v /home/jhihjian/video_download:/home/jhihjian/video_download \
--network=host -it bili-extract /bin/bash

python3 /opt/Bilibili-Video-Extract/main.py 

ctrl+P+Q



``` 

辅助手段
PaddleOCR的image 下载的慢，解决方法
```
docker install paddlepaddle 
https://paddleocr.bj.bcebos.com/docker/docker_pdocr_cuda9.tar.gz

tar zxf docker_pdocr_cuda9.tar.gz

docker load < docker_pdocr_cuda9.tar

docker images

# 执行docker images后如果有下面的输出，即可
hub.baidubce.com/paddlepaddle/paddle   latest-gpu-cuda9.0-cudnn7-dev    f56310dcc829
```
