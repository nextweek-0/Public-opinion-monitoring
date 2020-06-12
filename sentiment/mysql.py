from mod import predict_sentiment
import pymysql
from apscheduler.schedulers.blocking import BlockingScheduler
from gensim.models import KeyedVectors
import jieba
import re

# 词向量
def wv():
    file = '100000-small.txt'
    wv_from_text = KeyedVectors.load_word2vec_format(file,binary=False)
    wv_from_text.init_sims(replace=True)
    return wv_from_text

# 只留下一句话的字和数字
def token(string):
    all_str = ''
    list_str = re.findall(r'[\d|\w]+',string)
    for i in list_str:
        all_str += i
    return all_str

# 停用词
def stopwords():
    stop_words = []
    with open('stopwords.txt','r',encoding='utf-8') as f:
        for i in f:
            stop_words.append(i.replace('\n',''))
    return stop_words

# 关键词分类
def classify(review):
    price, env, taste = 0, 0, 0
    wv_from_text = wv()
    stop_words = stopwords()
    comment = jieba.lcut(token(review))
    comment = [i for i in comment if i not in stop_words]
    for i in comment:
        try:
            if (wv_from_text.similarity('价格',i)) > 0.5:
                price = 1
                break
        except:
            continue

    for i in comment:
        try:
            if (wv_from_text.similarity('环境',i)) > 0.5:
                env = 1
                break
        except:
            continue

    for i in comment:
        try:
            if (wv_from_text.similarity('味道',i)) > 0.5:
                taste = 1
                break
        except:
            continue

    return env, price, taste


# 存入MySQL
def sql():
    connect = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='594546594546wsl', db='sentiment',
                              charset='utf8mb4')
    # print(conn)

    cursor = connect.cursor()

    # cursor.execute('set names utf8')

    path = '../dazhongdianping_datas/dianping.txt'

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                # 拿到评论
                review = line.strip('\n').replace(' ', '')
                # 拿到情感正负
                sentiment = predict_sentiment(review)
                #全部评论写入数据库
                sql = "insert into st (review, sentiment) VALUES ('%s','%d')"
                data = (review, sentiment)
                cursor.execute(sql % data)
                connect.commit()
                # 关键词
                env, price, taste = classify(review)
                # 按关键词存入数据库

                if env == 1:
                    sql = "insert into env (review, sentiment) VALUES ('%s','%d')"
                    cursor.execute(sql % data)
                    connect.commit()

                if price == 1:
                    sql = "insert into price (review, sentiment) VALUES ('%s','%d')"
                    cursor.execute(sql % data)
                    connect.commit()

                if taste == 1:
                    sql = "insert into taste (review, sentiment) VALUES ('%s','%d')"
                    cursor.execute(sql % data)
                    connect.commit()

            except:
                continue


    cursor.close()
    connect.close()


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(sql, 'interval', second=86400)
    print('**')

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    # sql()


