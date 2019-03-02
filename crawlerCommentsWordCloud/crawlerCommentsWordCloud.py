from requests_html import HTMLSession
import re
import jieba
import wordcloud
import imageio

# 要爬取评论的链接
url = "https://movie.douban.com/subject/1292052"
# 需要爬取评论的页数(目前只能最多爬25页，原因未知)
total = 25
# 登陆后的cookies填写
raw_cookies = ""

def crawler(url):
    session = HTMLSession()
    # 构造cookies
    cookies = {}
    for line in raw_cookies.split(";"):
        key,value = line.split("=", 1)
        cookies[key] = value
    # 获取电影名称
    home_page = session.get(url, cookies = cookies)
    name = home_page.html.find("#content > h1 > span:nth-child(1)",first = True).text
    name = name.split(" ")[0]
    print("影片名称: {}".format(name))
    # 爬取评论
    comments = []
    current = 0
    t = ""
    for i in range(total):
        comments_page = session.get(url + "/comments?start=" + str(current) + "&limit=20&sort=new_score&status=P", cookies = cookies)
        comments_element = "<span class=\"short\">(\S*)</span>"
        comments += re.findall(comments_element, comments_page.html.html)
        current += 20
        print("共需要爬取{}页评论，当前正在爬取第{}页".format(total, i + 1))
    for comment in comments:
        t += comment
    # 写入文本文件
    f = open(name + ".txt", "w", encoding='utf-8')
    f.write(t)
    f.close()
    return name

def wordCloud(name):
    # 读取评论文件
    f = open(name + ".txt", "r", encoding='utf-8')
    t = f.read()
    f.close()
    # 分词
    ls = jieba.lcut(t)
    txt = " ".join(ls)
    # 读取mask作为背景生成词云
    mask = imageio.imread("mask.png")
    w = wordcloud.WordCloud( font_path = "msyh.ttf", mask = mask,
                             width = 1000, height = 700, background_color = "white")
    w.generate(txt)
    w.to_file(name + ".png")

def main():
    name = crawler(url)
    wordCloud(name)
main()