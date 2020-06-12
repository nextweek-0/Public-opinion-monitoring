import requests
import re
from bs4 import BeautifulSoup
from lxml import html


# cookie格式化
class transCookie:
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict


# 获得有cookie的url
def getHTMLText_cookie(url, cookie_dict):
    try:
        r = requests.post(
                    url,
                    headers={
                    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
                        },
                    cookies=cookie_dict,
                    )
        r.raise_for_status()
#         r.encoding = r.apparent_encoding
        return r.text
    except:
        return


# 没有cookie的url
def getHTMLText(url):

    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return


# 获得点评网页，按时间排序的点评网页，css，svg
def get_html(url_1, url_2):
    demo_1 = getHTMLText_cookie(url_1, cookie_time_dict)
    demo_2 = getHTMLText_cookie(url_2, cookie_time_dict)
    demo_all = demo_1 + demo_2

    soup_all = BeautifulSoup(demo_all, 'html.parser')

    #     得到全部评论
    all_review_list = []
    for i in soup_all.find_all(class_='review-words'):
        try:
            review = str(i)
            comment = re.compile(r'\n(.*?)<div', re.S)
            review = comment.search(review).group().replace('\n', '').replace('<div', '')
            review = re.sub(r'<img(.*?)>', '', review, count=0)
            all_review_list.append(review)
        except:
            continue
    #     css_url
    #     css_url = 'http:' + soup.find_all('link',attrs={'rel':"stylesheet"},limit=2)[1].attrs['href']
    css_url = 'http:' + soup_all.find_all('link', attrs={'rel': "stylesheet"}, limit=2)[1].attrs['href']
    css = getHTMLText(css_url)

    svg_url = 'http://' + re.findall(r'//(.*?)\.svg', css)[2] + '.svg'
    svg = getHTMLText(svg_url)
    soup_svg = BeautifulSoup(svg, 'html.parser')
    svg = soup_svg.find

    #     建立坐标字典
    zuobiao_dict = {}

    for i in soup_svg.find_all(x='0'):
        zuobiao_dict[int(i.attrs['y'])] = i.text

    return all_review_list, css_url, zuobiao_dict



# 得到需要转换的坐标

def get_css_position(css_name,css_url):

    css_positon_html = requests.get(css_url).text

    str_css = (r'%s{background:-(\d+).0px -(\d+).0px' % css_name)
    css_re = re.compile(str_css)
    info_css = css_re.findall(css_positon_html)

    return info_css


def reviews(all_reviews, css_url, svg):
    true_all_reviews = []
    for review in all_reviews:
        # 获取坐标 得到真正的字并加入列表
        true_word_list = []
        try:
            for i in re.findall(r'"(.*?)"', review):
                y = int(int(get_css_position(i, css_url)[0][0]) / 14)
                num = int(get_css_position(i, css_url)[0][1]) + 23
                true_word_list.append(svg[num][y])

            # 替换
            for true_word in true_word_list:
                review = re.sub(r'<(.*?)i>', true_word, review, count=1)
        except:
            continue

        true_all_reviews.append(review)
    return true_all_reviews

if __name__ == '__main__':
    Cookie_time = 'fspop=test; cye=beijing; _lxsdk_cuid=171966bc877c8-03a58ae48936b7-39624006-100200-171966bc878c8; _lxsdk=171966bc877c8-03a58ae48936b7-39624006-100200-171966bc878c8; _hc.v=4ec9bfb8-eadf-ba33-fc88-5e9a4e3a39bb.1587366579; t_lxid=171966bca16c8-046be06627f984-39624006-100200-171966bca17c8-tid; s_ViewType=10; ua=dpuser_01284058991; ctu=846e795424b54fb05f10518f1b29646db446a185dcaca07f5fb080ad12c7aa49; cy=2; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; dper=546a9b7d7b25c2d6bc70d325603c24f4848f196516ef9c6de7e3f35b7a2d924231dcf722271f93707abc04e2a6e83f172c39b5f0f244de6edb4b3fd77e1b2780d701c2c9628da6d1db169107e0fe8df9fd65fdd3f1ba4ef2c4372a970a02f095; ll=7fd06e815b796be3df069dec7836c3df; uamo=15122115256; dplet=a2042990f9583551124a22627866f65f; _lxsdk_s=171a620b382-80f-f53-093%7C%7C979'
    cookie = Cookie_time
    trans = transCookie(cookie)
    cookie_time_dict = trans.stringToDict()

    # 按时间排序的点评
    url_1 = 'http://www.dianping.com/shop/513329/review_all?queryType=sortType&&queryVal=latest'
    url_2 = 'http://www.dianping.com/shop/513329/review_all/p2?queryType=sortType&queryVal=latest'

    all_reviews, css_url, svg = get_html(url_1, url_2)

    true_all_reviews = reviews(all_reviews, css_url, svg)

    with open('dianping.txt', 'w',encoding='utf-8') as f:
        for review in true_all_reviews:
            f.write(review)
            f.write('\n')

    print('1')



