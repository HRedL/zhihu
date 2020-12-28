import requests
import json
from bs4 import BeautifulSoup
from pymysql import connect


def getHTMLText(url):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'cookie': '_zap=2114f2e8-5c61-4463-8f4e-c6374401b8ea; d_c0="AFBijGAPkBCPTr4PYS_Nejzwwy650LEBvKo=|1577325614"; _ga=GA1.2.1687688185.1582948073; _xsrf=NxhXtjqKvZ1TqSXWuTjWSmnKrcoNfpz9; z_c0="2|1:0|10:1601476673|4:z_c0|92:Mi4xel9UOER3QUFBQUFBVUdLTVlBLVFFQ1lBQUFCZ0FsVk5RZVpoWUFBNy1TZVJCRjNVcHJpV3IxZk5FSTZHV0RGTG9n|ad5b82712d2bae78942652c23508401b0b8e166884a8beab52e10e51bcf9da7f"; __utma=51854390.1687688185.1582948073.1601476676.1601476676.1; __utmz=51854390.1601476676.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/signin; __utmv=51854390.100--|2=registration_date=20190531=1^3=entry_date=20190531=1; tst=r; q_c1=a741fdf5d5c54f1ca3204a0141f96879|1604219637000|1601476674000; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1605060538,1605061512,1605061572,1605090967; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1605090967; SESSIONID=YMm21yQDSVSEvjbK2gDYLpkJKLpgtNc5yf8eJfcoxOr; JOID=UFwdBUwiexMXJ9vnHia4BK8IfW8FfTpwJBOkulR0K0xcULSDWbDHt0wk0eUR9KNX-Ze3nH7-zKrg3Gs5wxwlocY=; osd=W1kdB08pfhMVJNDiHiS7D6oIf2wOeDpyJxihulZ3IElcUreIXLDFtEch0ecS_6ZX-5S8mX78z6Hl3Gk6yBklo8U=; KLBRSID=0a401b23e8a71b70de2f4b37f5b4e379|1605091004|1605090946'
        }
        response = requests.get(url, headers=headers)
        return response
    except:
        return "产生异常"


def connectDB():
    db = connect('127.0.0.1', 'root', '123456', 'zhihu2')
    return db


def getAnswerInfo(cursor):
    url = "https://www.zhihu.com/api/v4/infinity/new_responders?type=pu&limit=10&after_id=1488556867"
    count = 0
    while True:
        response = getHTMLText(url)
        jsonBody = json.loads(response.text.encode('utf-8'))
        print(count)
        count+=1
        if "paging" not in jsonBody.keys():
            break
        next_url = jsonBody['paging']['next']
        next_url = next_url.replace("http", "https")
        if next_url == url:
            break
        url = next_url
        sql = "INSERT INTO answerer(people_id,gender,fullname,question_price,avatar_url,description) VALUES(%s,%s,%s,%s,%s,%s)"
        for data in jsonBody['data']:
            cursor.execute(sql, [data['id'],data['gender'], data['fullname'], data['question_price'],
                                 data['avatar_url'], data['description']])


if __name__ == "__main__":
    db = connectDB()
    cursor = db.cursor()

    # sql = "SELECT id,answerer_count,column_id FROM answer_column"
    # cursor.execute(sql)
    # answer_columns = cursor.fetchall()
    # for answer_column in answer_columns:
    getAnswerInfo(cursor)
    db.commit()
    db.close()