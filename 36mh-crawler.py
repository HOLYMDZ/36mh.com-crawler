#coding=utf-8
import requests
import re
import os
import time

#已经下载完毕的最后一张图，初始置0，若中断则按照编号重置
pos_c = 67
pos_i = 1
manga_name = 'dagongbamowangdaren'

chapters = requests.get('https://www.36mh.com/manhua/' + manga_name + '/')
url_head = 'https://www.36mh.com'
pic_head = 'https://img001.pkqiyi.com/'
chapters.encoding = 'utf-8'
chapters_html = chapters.text
chapters_html = chapters_html.replace('\n','')
chapters_html = chapters_html.replace(' ','')
chapters_pattern = re.compile(r"""<ahref="/manhua/""" + manga_name + r"""/[0-9]+.html"class=""><span>.+?话""")

doc_head = os.getcwd()

chapters_list = chapters_pattern.findall(chapters_html)

chapters_dic = {}

for i in chapters_list:
    chapter_link = re.findall(r'/manhua/' + manga_name + r'/[0-9]+.html',i)
    chapter_name = re.findall(r'<span>(.+)',i)
    chapters_dic[chapter_name[0]] = chapter_link[0]

error = 1

for name in chapters_dic:
    if error < pos_c:
        error += 1
        continue
    dir = os.getcwd()
    if error > pos_c:
        os.makedirs(dir + "\\" + name)
    chapter = requests.get(url_head + chapters_dic[name])
    chapter.encoding = 'utf-8'
    chapter_html = chapter.text
    chapter_pattern = re.compile(r"""chapterImages = \["(.+?)"\]""")
    images = chapter_pattern.findall(chapter_html)
    images_list = images[0].split('''","''')
    mid_pattern = re.compile(r'''chapterPath = "(.+?)"''')
    mid_url = mid_pattern.findall(chapter_html)
    num = 1
    for pic_name in images_list:
        if error == pos_c:
            if num <= pos_i:
                num += 1
                continue
        pic_url = pic_head + mid_url[0] + pic_name
        f_name = ".\\" + name +"\\" + str(num) + ".jpg"
        pic_out = open(f_name, "wb+")
        img = requests.get(pic_url)
        pic_out.write(img.content)
        pic_out.close()
        print(num)
        print('\n')
        num += 1
        time.sleep(3)
    print(name)
    print('\n')
    error += 1