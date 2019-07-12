'''
    Author:Monty
    Date:2019-05-26
    Version:1.0
    Func:Download images from tieba.baidu.com
'''

import requests
from lxml import etree
from urllib.request import urlretrieve

def get_HTML(url):
    '''获取网页内容'''
    # headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        # 把返回的HTML文本变为element类型，方便后续使用xpath提取数据
        html = etree.HTML(r.text)
        return html
    except:
        print('获取网页内容失败')

def get_tiezi_url(html):
    '''解析贴吧页面的HTML信息，获取帖子的URL'''
    # html = etree.HTML(html_text)
    uids = html.xpath('//*[@id="thread_list"]//li/@data-tid')
    return uids

def parse_tiezi(uid):
    '''解析帖子页面，获取帖子总页数并下载图片到本地'''
    tiezi_url = 'http://tieba.baidu.com/p/' + uid
    tiezi_html = get_HTML(tiezi_url)
    # 找出该帖子共有多少页
    pages = int(tiezi_html.xpath('//ul[@class="l_posts_num"][1]/li[2]/span[2]')[0].text)
    for page in range(pages+1):
        tiezi_url = 'http://tieba.baidu.com/p/' + uid + '?pn={}'.format(page)
        # 获取帖子页面内容
        tiezi_html = get_HTML(tiezi_url)
        print('正在解析:{}'.format(tiezi_url))
        get_img(tiezi_html)

def get_img(tiezi_html):
    '''获取图片url并下载'''
    img_urls = tiezi_html.xpath('//img[@class="BDE_Image"]/@src')
    for img_url in img_urls:
        # 用图片链接的最后一串字符命名图片
        img_name = 'd:/my_pic/' + img_url.split('/')[-1]
        print('正在下载:',img_url)
        urlretrieve(img_url, img_name)

def main():
    # 输入贴吧名称
    tieba_name = input('Enter tieba name:')
    for page in range(100):
        url = 'http://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}'.format(tieba_name, 50 * page)
        html = get_HTML(url)
        uid_list = get_tiezi_url(html)
        for uid in uid_list:
            parse_tiezi(uid)

if __name__ == '__main__':
    main()
