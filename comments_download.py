import time
from multiprocessing.dummy import Pool as ThreadPool
import json
import pymysql
import proxy
import logging



def divide(thread_i_di):
    """
    todo : 线程划分任务
    :param thread_i_di:
    :return:
    """
    db = pymysql.connect(user='biliu', password='123456',
                         host='centos.jh',
                         database='bili')
    for j in range(0, total//thread):
        #print("j:{}, i:{}. ".format(j, i+1))
        pageNumber = j*thread + (thread_i_di + 1)
        commitUrl = "https://api.bilibili.com/x/v2/reply?&pn=" + str(pageNumber) + "&type=1&oid=" + str(avId)
        run(commitUrl,db)
        print("sprider has run {}.".format(pageNumber))
    db.close()


def run(url,db):
    """
    todo : 评论爬虫入口
    :param url:
    :return:
    """
    try:
        resp = proxy.proxy_get(url)
        time.sleep(0.5)  # 延迟，避免太快 ip 被封
        #print(resp.status_code)

        if ( resp.status_code == 200 ):
            parserHtml(resp.text,db)
            print("run finsh:",url)
            return True
        else:
            print("none, try again.")
            run(url,db)
            return url
    except:
        print("error, try again.Retry URL:",url)
        run(url,db)
        return url


# 解析html内容
def parserHtml(textHtml,db):
    '''
    todo ：利用json解析html text 文本内容
    parameter value ：html 内容
    return ：
    '''

    try:
        commentDetailData = json.loads(textHtml)
        #print(s)
    except:
        #pageGetWrong.append(pageNumber)
        print('error')

    commentlist = []

    try:
        # 切片遍历 得到信息
        for i in range(20):
            comment = commentDetailData['data']['replies'][i]
            blist = []

            # personal details
            userName = comment['member']['uname']
            userSign = comment['member']['sign']
            userSex = comment['member']['sex']
            userMid = comment['member']['mid']
            userLeverl = comment['member']['level_info']['current_level']


            # Python time strftime() 函数接收以时间元组，并返回以可读字符串表示的当地时间，格式由参数format决定。
            # Python time localtime() 函数类似gmtime()，作用是格式化时间戳为本地的时间
            commentCtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(comment['ctime']))
            commentContent = comment['content']['message']
            commentPlat = comment['content']['plat']  # palt － 机型－  1 未知 2 安卓 3 ios
            commentLikes = comment['like']
            commentRcounts = comment['rcount']
            # print(userName, userSign, userSex, userMid, userLeverl, commentCtime, commentContent, commentPlat, commentLikes, commentRcounts)

            insertIntoDataBase(userName, userSign, userSex, userMid, userLeverl, commentCtime, commentContent, commentPlat, commentLikes, commentRcounts,db)


            blist.append(userName)
            blist.append(userSign)
            blist.append(userSex)
            blist.append(userMid)
            blist.append(userLeverl)

            blist.append(commentCtime)
            blist.append(commentContent)
            blist.append(commentPlat)
            blist.append(commentLikes)
            blist.append(commentRcounts)
            #print(userName, userSign, userSex, userMid, userLeverl, commentCtime, commentContent, commentPlat, commentLikes, commentRcounts)

            commentlist.append(blist)

        #print("切割内容：" + str(commentlist[:1]))


    except:
        pass







def insertIntoDataBase(s1, s2, s3, s4, s5, s6, s7, s8, s9, s10,db):
    """
    todo : 插入数据库， 并这个函数中调用用户信息爬虫
    :param s1:
    :param s2:
    :param s3:
    :param s4:  用户 mid
    :param s5:
    :param s6:
    :param s7:
    :param s8:
    :param s9:
    :param s10:
    :return:
    """

    # 打开数据库连接
    # db = pymysql.connect(host = "localhost", port = 3306, user = "biliu", password = "123456", database = comDataBaseName, charset='utf8mb4')
    # db = mysql.connector.connect(user='biliu', password='123456',
    #                               host='centos.jh',
    #                               database='bili',
    #                               use_pure=False)

    # print("open db conn")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 插入语句
    sql = "REPLACE INTO "+ comTableName +"(av,uname, sign, sex, mid, current_level, ctime, message, plat, likehah, rcount) VALUES " \
          "('%s','%s', '%s',  '%s',  %s,  %s, '%s', '%s',  %s,  '%s',  %s)" % (int(avId),str(s1), str(s2), str(s3), int(s4), int(s5), str(s6), str(s7), int(s8), str(s9), int(s10) )
    try:
        # 执行sql语句
        #print("prefer execute sql.  ")
        #print(sql)
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        print("worng in insert")
        # 如果发生错误则回滚
        db.rollback()

    # 因为评论人可能不知评论一次，所以需要去重
    # if(str(checkMid(s4,db)) != "存在" ):
    #     #print("bu cun zai ,zhengzaizhuaqv")
    #
    #     try:
    #         print("正在抓取用户信息， s4 / mid", s4)
    #         userinfo_download.getUsrInfoMainSpider(s4,db)
    #     except:
    #         print("用户信息爬虫有误，正在尝试再次获取，mid:", s4)
    #         userinfo_download.getUsrInfoMainSpider(s4,db)





def checkMid(mid,db):
    """
    todo : 检查用户信息表中，用户信息重复情况
    :param mid:
    :return:
    """
    # db = pymysql.connect(user='biliu', password='123456',
    #                      host='centos.jh',
    #                      database='bili')
    # db = pymysql.connect(host = "centos.jh", port = 3306, user = "biliu", password = "123456", database = comDataBaseName, charset='utf8mb4')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL query语句
    sql = "select * from bili_usrinfo where mid like '{}'".format(mid)

    #print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
        data_dict = [dict(zip([col[0] for col in desc], row)) for row in
                     cursor.fetchall()]  # 列表表达式把数据组装起来        # 提交到数据库执行

        if(str(data_dict) != "[]"):
            #print("存在",str(data_dict))
            return "存在"

        db.commit()
    except:
        print("worng in query mid. ")
        # 如果发生错误则回滚
        db.rollback()

def getTotal(avId,max=100):
    baseUrl="https://api.bilibili.com/x/v2/reply?&type=1&oid="+str(avId)
    res=proxy.proxy_get(baseUrl)
    jsonDict=json.loads(res.text)
    page=jsonDict['data']['page']
    count=int(page['count'])
    size=int(page['size'])
    result=count/size+1
    if result < max:
        return int(result)
    else:
        return max
# 获得合适的线程数，如果小于10，单线程
# 大于十，进程数为 num//10
# 上限为6
def getThreadCount(total,max=6):
    if total<10:
        return 1
    elif total>60:
        return max
    else:
        return total//10

# 抓取视频id
def SpiderComment(avId):
    time0 = time.time()

    # 评论爬虫 数据库名
    comDataBaseName = "bili"
    # 评论爬虫 表名
    comTableName = "bili_comment"
    # 抓取页面数量
    total = getTotal(avId)

    # 线程
    thread = getThreadCount(total)
    logging.info("视频id:" + str(avId) + ",页面数量:" + str(total) + "线程:" + str(thread))
    thread_i = [j
                for j in range(0, thread)
                ]

    pool = ThreadPool(thread)
    pool.map(divide, thread_i)

    pool.close()
    pool.join()

    time1 = time.time()
    logging.info("总花费时间:{}s".format(time1 - time0))




# https://github.com/Fyzjym/Spider-BiliComUsr