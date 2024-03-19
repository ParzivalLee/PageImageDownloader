"""
@filename PageImageDownloader.py
@author 葛文星
@encoding utf-8
@date 2024-3-19
@lastModified 2024-3-19
@description 页面图片下载器
"""
import requests
from bs4 import BeautifulSoup
import time
import sys
import configparser
import os

# 网页图片下载器
class PageImageDownloader:
    def __init__(self, url, path) -> None:
        self.logs = []  # 日志输出列表
        self.urls = []  # 图片链接
        self.path = path  # 输出文件夹
        self.baseUrl = '/'.join(url.split("/")[:3])  # 构造基础URL
        print(self.baseUrl)

        response = requests.get(url)
        soup = BeautifulSoup(response.text)
        self.title = soup.title.string.strip().replace("/", "_")\
            .replace("\\", "_")\
            .replace("|", "_")\
            .replace("?", "_")\
            .replace(">", "_")\
            .replace("<", "_")\
            .replace("*", "_")\
            .replace("\"", "_")\
            .replace(":", "_")  # 获取网页标题
        
        imgs = soup.find_all('img')  # 解析图片标签
        for i in imgs:
            # 解析图片网页中的链接
            url = i.get('src')
            if not url:
                continue
            if url.startswith("//"):
                url = "http:" + url
            elif url.startswith("/"):
                url = self.baseUrl + url
            self.urls.append(url)

    def saveImage(self, url: str, filePath: str) -> None:
        """
        保存图片
        :param url: 图片链接
        :param filePath: 文件保存位置
        """
        path = os.path.join(filePath, self.title)
        if not os.path.exists(path):
            # 如果不存在该文件夹则创建
            os.makedirs(path)

        filename = url.strip("/").split("/")[-1]  # 解析文件名称

        try:
            response = requests.get(url)  # 获取响应
            if response.status_code == 200 or response.status_code == 301 or response.status_code == 302:
                with open (os.path.join(path, filename), 'wb') as fp:
                    fp.write(response.content)
            print(response.status_code)
        except:
            print("Failed")
            return
        
    def run(self):
        # 运行程序
        for i in self.urls:
            print(f"[{time.strftime('%H:%M:%S')}] 正在获取 {i} ", end=' ')
            self.saveImage(i, self.path)

if __name__ == "__main__":
    args = sys.argv[1:]  # 获取参数
    if not args:
        url = input("请输入url:")
    else:
        url = args[0]
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')
    path = cfg.get("image_downloader", "file_path")  # 解析输出文件夹
    pidl = PageImageDownloader(url=url, path=path)
    pidl.run()
