# 存储从知乎爬取的相关数据

建议直接使用mysql转储sql文件，其中csv文件和excel文件都是从mysql中导出，方便阅读的。



# 爬虫执行顺序



1. answer_column.py

2. answer.py

3. answer_detail.py

4. answerer_detail.py

5. scrapy scrawl zhihu

# 表的含义

answer_column：类别信息：共10个类别：职场、教育。。。。。

answerer：答主信息

review：咨询的评论信息