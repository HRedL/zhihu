
import pymysql
from scrapyspider.items import PangTing
from scrapy import log


class ScrapyspiderPipeline(object):


    def process_item(self, item, spider):

       # 连接数据库
        my_sql = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', charset='utf8',
                                 db='zhihu2', use_unicode=True)
        # 获取游标
        cur = my_sql.cursor()
        try:
            if isinstance(item, PangTing):
                sql = "UPDATE pangting SET price=%s, pangting_count=%s, zan_count=%s,time=%s,content=%s,user=%s WHERE ID=%s"
                cur.execute(sql,
                            [item['price'],item['pangting_count'],item['zan_count'],item['time'],item['content'],item['user'],item['id']])
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
