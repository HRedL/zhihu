import requests
import json
from bs4 import BeautifulSoup
from pymysql import connect


def getHTMLText(url):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'cookie': '_zap=2114f2e8-5c61-4463-8f4e-c6374401b8ea; d_c0="AFBijGAPkBCPTr4PYS_Nejzwwy650LEBvKo=|1577325614"; _ga=GA1.2.1687688185.1582948073; _xsrf=NxhXtjqKvZ1TqSXWuTjWSmnKrcoNfpz9; l_cap_id="YmE5M2UxNmZkZmE4NGZiMDljZTc1Yjg4OTcyNDJiOWE=|1601476278|fb34e2293348083ad3b5618625ad21fb5debf65f"; r_cap_id="NmMxZGVkOTQ3MGM3NGE3Nzk5ZDQ4ZDAzNTRiNTkzNGM=|1601476278|f0f85d61df8f46d6745ceea842cba9884bd4da9b"; cap_id="NDIyMDA4YTc5NThkNDg3ZGEyOWRmZDk1NjRjZmUyYTg=|1601476278|f674e53881aabb5d7f3617484d09874880112ec7"; capsion_ticket="2|1:0|10:1601476299|14:capsion_ticket|44:ZWMxZmU3NThlMDkwNDk1MzkzMDEzNjBlZTNjMDUwMzc=|7e3d96573692b746fe5b81792a84e36a671682cba03b0146e8f9a2c04acabd3e"; z_c0="2|1:0|10:1601476673|4:z_c0|92:Mi4xel9UOER3QUFBQUFBVUdLTVlBLVFFQ1lBQUFCZ0FsVk5RZVpoWUFBNy1TZVJCRjNVcHJpV3IxZk5FSTZHV0RGTG9n|ad5b82712d2bae78942652c23508401b0b8e166884a8beab52e10e51bcf9da7f"; q_c1=a741fdf5d5c54f1ca3204a0141f96879|1601476674000|1601476674000; __utma=51854390.1687688185.1582948073.1601476676.1601476676.1; __utmz=51854390.1601476676.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/signin; __utmv=51854390.100--|2=registration_date=20190531=1^3=entry_date=20190531=1; tst=r; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1603025658,1603025739,1603030270,1603120938; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1603120938; SESSIONID=SzRblaSpGMEB59Oq3HsSgTssoDGiGuITu8u74nFDgBl; JOID=V1oUBkJtolaQTdghTG1pTy1leqFZOdsA_i2-cTgm6BDWdO1pPkUK089G3CZEdn127RrilrNKxPn75SnvKt0cKKU=; osd=W10TCkxhpVGcQ9QmS2FnQypidq9VPtwM8CG5djQo5BfReONlOUIG3cNB2ypKenpx4RTukbRGyvX84iXhJtobJKs=; KLBRSID=4efa8d1879cb42f8c5b48fe9f8d37c16|1603121763|1603120935'
        }
        response = requests.get(url, headers=headers)
        return response
    except:
        return "产生异常"


def connectDB():
    db = connect('127.0.0.1', 'root', '123456', 'zhihu')
    return db




def getAnswerInfo(cursor,answer_column):
    ac_id,answer_count,column_id = answer_column

    total_count = int(answer_count)//10 if int(answer_count)%10==0 else int(answer_count)//10 +1
    for i in range(total_count):

        url = f'https://www.zhihu.com/api/v4/infinity/topics/{column_id}/responders?limit=10&offset={i*10}'
        response = getHTMLText(url)
        jsonBody = json.loads(response.text.encode('utf-8'))
        datas = jsonBody['data']
        sql = "INSERT INTO answerer(people_id,fullname,score,question_price,conversation_count,avatar_url,description,acid) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        for data in datas:
            cursor.execute(sql,[data['id'],data['fullname'],data['score'],data['question_price'],data['conversation_count'],data['avatar_url'],data['description'],ac_id])
            
if __name__ =="__main__":
    db = connectDB()
    cursor = db.cursor()

    sql = "SELECT id,answerer_count,column_id FROM answer_column"
    cursor.execute(sql)
    answer_columns = cursor.fetchall()
    for answer_column in answer_columns:
        getAnswerInfo(cursor,answer_column)
    db.commit()
    db.close()