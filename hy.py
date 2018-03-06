import requests
from bs4 import BeautifulSoup
import json
import re


def get_html(url):
    #  模拟网页请求
    headers = {
	'User-Agent': 'Mozilla/5.0(Windows NT 6.1; WOW64)',
	'Referer': 'http://music.163.com/',
	'Host': 'music.163.com'
    }
    try:
        response = requests.get(url, headers=headers)
        html = response.text
        return html
    except:
        print('request error')
        pass


def get_singer_info(html):
    # 获取html源码
    soup = BeautifulSoup(html, 'lxml')
    # 网页标签为ul class为f-hide
    links = soup.find('ul', class_='f-hide').find_all('a')
    song_IDs = []
    song_names = []
    # 循环歌曲
    for link in links:
        song_ID = link.get('href').split('=')[-1]
        song_name = link.get_text()
        song_IDs.append(song_ID)
        song_names.append(song_name)
    # zip元组方式保存
    return zip(song_names, song_IDs)


def get_lyric(song_id):
    # 获取歌词，链接为网易云音乐API
    url = 'http://music.163.com/api/song/lyric?' + 'id=' + str(song_id) + '&lv=1&kv=1&tv=1'
    html = get_html(url)
    # 载入json数据
    json_obj = json.loads(html)
    # 匹配Json字段
    initial_lyric = json_obj['lrc']['lyric']
    # 正则匹配时间字符串
    regex = re.compile(r'\[.*\]')
    # 正则替换时间字符串
    final_lyric = re.sub(regex, '', initial_lyric).strip()
    return final_lyric


def write_text(song_name, lyric):
    print('正在写入歌曲：{}'.format(song_name))
    # 歌词写入文件
    with open('music/{}.txt'.format(song_name), 'a', encoding='utf-8') as fp:
        fp.write(lyric)


if __name__ == '__main__':
    # 唱歌人ID
    singer_id = '6452'
    # 唱歌人网页
    start_url = 'http://music.163.com/artist?id={}'.format(singer_id)
    html = get_html(start_url)
    # 获取歌曲名，歌曲ID
    singer_infos = get_singer_info(html)
    # 循环输出歌词写入歌曲文件中
    for singer_info in singer_infos:
        lyric = get_lyric(singer_info[1])
        write_text(singer_info[0], lyric)
