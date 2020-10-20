import scrapy
import pymysql
from bs4 import BeautifulSoup
from scrapyspider.items import Review
import time
import json

# 继承自scrapy.Spider
class TripadvisorSpider(scrapy.Spider):

    name = "zhihu"
    def start_requests(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'cookie': '_zap=2114f2e8-5c61-4463-8f4e-c6374401b8ea; d_c0="AFBijGAPkBCPTr4PYS_Nejzwwy650LEBvKo=|1577325614"; _ga=GA1.2.1687688185.1582948073; _xsrf=NxhXtjqKvZ1TqSXWuTjWSmnKrcoNfpz9; l_cap_id="YmE5M2UxNmZkZmE4NGZiMDljZTc1Yjg4OTcyNDJiOWE=|1601476278|fb34e2293348083ad3b5618625ad21fb5debf65f"; r_cap_id="NmMxZGVkOTQ3MGM3NGE3Nzk5ZDQ4ZDAzNTRiNTkzNGM=|1601476278|f0f85d61df8f46d6745ceea842cba9884bd4da9b"; cap_id="NDIyMDA4YTc5NThkNDg3ZGEyOWRmZDk1NjRjZmUyYTg=|1601476278|f674e53881aabb5d7f3617484d09874880112ec7"; capsion_ticket="2|1:0|10:1601476299|14:capsion_ticket|44:ZWMxZmU3NThlMDkwNDk1MzkzMDEzNjBlZTNjMDUwMzc=|7e3d96573692b746fe5b81792a84e36a671682cba03b0146e8f9a2c04acabd3e"; z_c0="2|1:0|10:1601476673|4:z_c0|92:Mi4xel9UOER3QUFBQUFBVUdLTVlBLVFFQ1lBQUFCZ0FsVk5RZVpoWUFBNy1TZVJCRjNVcHJpV3IxZk5FSTZHV0RGTG9n|ad5b82712d2bae78942652c23508401b0b8e166884a8beab52e10e51bcf9da7f"; q_c1=a741fdf5d5c54f1ca3204a0141f96879|1601476674000|1601476674000; __utma=51854390.1687688185.1582948073.1601476676.1601476676.1; __utmz=51854390.1601476676.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/signin; __utmv=51854390.100--|2=registration_date=20190531=1^3=entry_date=20190531=1; tst=r; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1603025658,1603025739,1603030270,1603120938; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1603120938; SESSIONID=SzRblaSpGMEB59Oq3HsSgTssoDGiGuITu8u74nFDgBl; JOID=V1oUBkJtolaQTdghTG1pTy1leqFZOdsA_i2-cTgm6BDWdO1pPkUK089G3CZEdn127RrilrNKxPn75SnvKt0cKKU=; osd=W10TCkxhpVGcQ9QmS2FnQypidq9VPtwM8CG5djQo5BfReONlOUIG3cNB2ypKenpx4RTukbRGyvX84iXhJtobJKs=; KLBRSID=4efa8d1879cb42f8c5b48fe9f8d37c16|1603121763|1603120935'
        }

        my_sql = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', charset='utf8',
                                 db='zhihu', use_unicode=True)
        cur = my_sql.cursor()
        cur.execute("SELECT id,people_id FROM answerer")

        datas = cur.fetchall()
        for data in datas :
            aid ,people_id = data
            url = f"https://www.zhihu.com/api/v4/infinity/{people_id}/reviews?limit=10&offset=0"
            yield scrapy.Request(url=url,headers=headers,callback=lambda response,foreign_key=aid,people_id=people_id: self.parse(response,foreign_key,people_id))


    def parse(self,response,foreign_key,people_id):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'cookie': '_zap=2114f2e8-5c61-4463-8f4e-c6374401b8ea; d_c0="AFBijGAPkBCPTr4PYS_Nejzwwy650LEBvKo=|1577325614"; _ga=GA1.2.1687688185.1582948073; _xsrf=NxhXtjqKvZ1TqSXWuTjWSmnKrcoNfpz9; l_cap_id="YmE5M2UxNmZkZmE4NGZiMDljZTc1Yjg4OTcyNDJiOWE=|1601476278|fb34e2293348083ad3b5618625ad21fb5debf65f"; r_cap_id="NmMxZGVkOTQ3MGM3NGE3Nzk5ZDQ4ZDAzNTRiNTkzNGM=|1601476278|f0f85d61df8f46d6745ceea842cba9884bd4da9b"; cap_id="NDIyMDA4YTc5NThkNDg3ZGEyOWRmZDk1NjRjZmUyYTg=|1601476278|f674e53881aabb5d7f3617484d09874880112ec7"; capsion_ticket="2|1:0|10:1601476299|14:capsion_ticket|44:ZWMxZmU3NThlMDkwNDk1MzkzMDEzNjBlZTNjMDUwMzc=|7e3d96573692b746fe5b81792a84e36a671682cba03b0146e8f9a2c04acabd3e"; z_c0="2|1:0|10:1601476673|4:z_c0|92:Mi4xel9UOER3QUFBQUFBVUdLTVlBLVFFQ1lBQUFCZ0FsVk5RZVpoWUFBNy1TZVJCRjNVcHJpV3IxZk5FSTZHV0RGTG9n|ad5b82712d2bae78942652c23508401b0b8e166884a8beab52e10e51bcf9da7f"; q_c1=a741fdf5d5c54f1ca3204a0141f96879|1601476674000|1601476674000; __utma=51854390.1687688185.1582948073.1601476676.1601476676.1; __utmz=51854390.1601476676.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/signin; __utmv=51854390.100--|2=registration_date=20190531=1^3=entry_date=20190531=1; tst=r; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1603025658,1603025739,1603030270,1603120938; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1603120938; SESSIONID=SzRblaSpGMEB59Oq3HsSgTssoDGiGuITu8u74nFDgBl; JOID=V1oUBkJtolaQTdghTG1pTy1leqFZOdsA_i2-cTgm6BDWdO1pPkUK089G3CZEdn127RrilrNKxPn75SnvKt0cKKU=; osd=W10TCkxhpVGcQ9QmS2FnQypidq9VPtwM8CG5djQo5BfReONlOUIG3cNB2ypKenpx4RTukbRGyvX84iXhJtobJKs=; KLBRSID=4efa8d1879cb42f8c5b48fe9f8d37c16|1603121763|1603120935'
        }

        jsonBody = json.loads(response.text.encode('utf-8'))
        total_count = int(jsonBody['count'])
        total_count = total_count//10 if total_count%10 == 0 else total_count//10 + 1
        for i in range(total_count):
            url = f'https://www.zhihu.com/api/v4/infinity/{people_id}/reviews?limit=10&offset={i * 10}'

            yield scrapy.Request(url=url, headers=headers,
                                 callback=lambda response, foreign_key=foreign_key: self.parse1(response, foreign_key))

    def parse1(self, response,foreign_key):

        jsonBody = json.loads(response.text.encode('utf-8'))
        datas = jsonBody['data']
        for data in datas:
            review = Review()
            review['is_anonymous'] = data['is_anonymous']
            review['questioner_id'] = data['questioner_id']
            review['content'] = data['review']
            review['score'] = data['score']
            review['fullname'] = data['fullname']
            review['is_automatic'] = data['is_automatic']
            review['update_time'] = data['updated_at']
            review['create_time'] = data['created_at']
            review['aid'] = foreign_key
            yield review


