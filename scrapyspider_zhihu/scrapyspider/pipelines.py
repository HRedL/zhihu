
import pymysql
from scrapyspider.items import Review
from scrapy import log


class ScrapyspiderPipeline(object):


    def process_item(self, item, spider):

       # 连接数据库
        my_sql = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', charset='utf8',
                                 db='zhihu', use_unicode=True)
        # 获取游标
        cur = my_sql.cursor()
        try:
            if isinstance(item, Review):
                sql = "INSERT INTO review(is_anonymous,questioner_id,content,score,fullname,is_automatic,update_time,create_time,aid) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cur.execute(sql,
                            [item['is_anonymous'],item['questioner_id'],item['content'],item['score'],item['fullname'],item['is_automatic'],item['update_time'],item['create_time'],item['aid']])
                # 提交
                my_sql.commit()
                # 关闭游标
                cur.close()
                # 关闭数据库连接
                my_sql.close()
        except Exception as e:
            log.msg("写入数据库出现异常", level=log.WARING)
            my_sql.commit()
            cur.close()
            my_sql.close()
        finally:
            return item
