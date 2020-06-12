from flask import Flask,render_template,request
import os
import pymysql


app = Flask(__name__)


# 差评与好评数
@app.route("/")
def ps():

    connent = pymysql.connect(host='127.0.0.1', port=3306,
                              user='root', password='594546594546wsl',
                              db='sentiment', charset='utf8mb4')
    cursor = connent.cursor()

    # 全部评论数
    try:
        sql = 'select  sentiment from st where QUARTER(createtime)=QUARTER(now()) and sentiment = 1'
        all_hp = cursor.execute(sql)
        sql = 'select  sentiment from st where QUARTER(createtime)=QUARTER(now()) and sentiment = 0'
        all_cp = cursor.execute(sql)
    except:
        pass

    # 环境评论数
    try:
        sql = 'select  sentiment from env where QUARTER(createtime)=QUARTER(now()) and sentiment = 1'
        env_hp = cursor.execute(sql)
        sql = 'select  sentiment from env where QUARTER(createtime)=QUARTER(now()) and sentiment = 0'
        env_cp = cursor.execute(sql)
    except:
        pass

    # 价格
    try:
        sql = 'select  sentiment from price where QUARTER(createtime)=QUARTER(now()) and sentiment = 1'
        price_hp = cursor.execute(sql)
        sql = 'select  sentiment from price where QUARTER(createtime)=QUARTER(now()) and sentiment = 0'
        price_cp = cursor.execute(sql)
    except:
        pass

    # 味道
    try:
        sql = 'select  sentiment from taste where QUARTER(createtime)=QUARTER(now()) and sentiment = 1'
        taste_hp = cursor.execute(sql)
        sql = 'select  sentiment from taste where QUARTER(createtime)=QUARTER(now()) and sentiment = 0'
        taste_cp = cursor.execute(sql)
    except:
        pass
    # reviews =cursor.fetchall()
    # for review in reviews:
    #     print(review[0])

    cursor.close()

    connent.close()

    return render_template('ps.html', all_hp=all_hp, all_cp=all_cp,
                           env_hp=env_hp, env_cp=env_cp,
                           price_hp=price_hp, price_cp=price_cp,
                           taste_hp=taste_hp, taste_cp=taste_cp
                           )

# 全部评论
@app.route("/all")
def all_review():

    connent = pymysql.connect(host='127.0.0.1', port=3306,
                              user='root', password='594546594546wsl',
                              db='sentiment', charset='utf8mb4')
    cursor = connent.cursor()

    sql = 'select  review from st where QUARTER(createtime)=QUARTER(now()) and sentiment = 1'
    cursor.execute(sql)
    hp = cursor.fetchall()
    # hp = list(hp[-20:])
    # for i,review in enumerate(hp):
    #     hp[i] = hp[i][0]
    hp = hp[-20:]
    sql = 'select  review from st where QUARTER(createtime)=QUARTER(now()) and sentiment = 0'
    cursor.execute(sql)
    cp = cursor.fetchall()
    cp = cp[-20:]


    cursor.close()

    connent.close()
    return render_template('all.html', hp=hp, cp=cp)

# 环境评论

@app.route("/env")
def env_review():
    connent = pymysql.connect(host='127.0.0.1', port=3306,
                              user='root', password='594546594546wsl',
                              db='sentiment', charset='utf8mb4')
    cursor = connent.cursor()

    sql = 'select review from env where QUARTER(createtime)=QUARTER(now()) and sentiment = 1'
    cursor.execute(sql)
    hp = cursor.fetchall()[:20]

    sql = 'select review from env where QUARTER(createtime)=QUARTER(now()) and sentiment = 1'
    cursor.execute(sql)
    cp = cursor.fetchall()[:20]

    cursor.close()

    connent.close()
    return render_template('env.html', hp=hp, cp=cp)

# 价格评论
@app.route("/price")
def price_review():
    connent = pymysql.connect(host='127.0.0.1', port=3306,
                              user='root', password='594546594546wsl',
                              db='sentiment', charset='utf8mb4')
    cursor = connent.cursor()

    sql = 'select review from price where QUARTER(createtime)=QUARTER(now()) and sentiment = 1'
    cursor.execute(sql)
    hp = cursor.fetchall()[:20]

    sql = 'select review from price where QUARTER(createtime)=QUARTER(now()) and sentiment = 1'
    cursor.execute(sql)
    cp = cursor.fetchall()[:20]

    cursor.close()

    connent.close()
    return render_template('price.html', hp=hp, cp=cp)

# 味道评论
@app.route("/taste")
def taste_review():
    connent = pymysql.connect(host='127.0.0.1', port=3306,
                              user='root', password='594546594546wsl',
                              db='sentiment', charset='utf8mb4')
    cursor = connent.cursor()

    sql = 'select review from taste where QUARTER(createtime)=QUARTER(now()) and sentiment = 1'
    cursor.execute(sql)
    hp = cursor.fetchall()[:20]

    sql = 'select review from taste where QUARTER(createtime)=QUARTER(now()) and sentiment = 1'
    cursor.execute(sql)
    cp = cursor.fetchall()[:20]

    cursor.close()

    connent.close()
    return render_template('taste.html', hp=hp, cp=cp)


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)


# def all_review():
#
#     connent = pymysql.connect(host='127.0.0.1', port=3306,
#                               user='root', password='594546594546wsl',
#                               db='sentiment', charset='utf8mb4')
#     cursor = connent.cursor()
#
#     sql = 'select  review from st where QUARTER(createtime)=QUARTER(now()) and sentiment = 1'
#     cursor.execute(sql)
#     hp = cursor.fetchall()
#     hp = list(hp[-20:])
#     for i,review in enumerate(hp):
#         hp[i] = hp[i][0]
#     sql = 'select  review from st where QUARTER(createtime)=QUARTER(now()) and sentiment = 0'
#     cursor.execute(sql)
#     cp = cursor.fetchall()
#     cp = cp[-20:]
#     print(hp)
#
#
# all_review()