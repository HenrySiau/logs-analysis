import io
import psycopg2


DBNAME = "news"
# 1. What are the most popular three articles of all time?
query_1 = """
 select articles.slug, count(*)as views
 from log join articles on
 log.path like concat('%', articles.slug)
 group by articles.slug, log.path
 order by views desc limit 3
 """

db = psycopg2.connect(dbname=DBNAME)
c = db.cursor()
c.execute(query_1)
raw_result = c.fetchall()
f = open('results.txt', 'ab')
f.write("The most popular three articles of all time.\n")
for item in raw_result:
    title = str(
        item[0].replace("-", " ")).title()
    views = int(item[1])
    f.write(
        title + " --" + str(views) + " Views\n")
f.write("\n")
c.close()
f.close()

# 2. Who are the most popular article authors
# of all time? Present this as a sorted list
# with the most popular author at the top.

query_2 = """
 select
 authors.name, sum(sub.views) as sum_views
 from
 (select articles.slug, articles.author,
 count(*)as views
 from log join articles
 on log.path like concat('%', articles.slug)
 group by articles.slug, log.path, articles.author
 order by views desc) sub
 join authors on sub.author = authors.id
 group by authors.id, sub.author
 order by sum_views desc
"""
db = psycopg2.connect(dbname=DBNAME)
c = db.cursor()
c.execute(query_2)
raw_result = c.fetchall()
f = open('results.txt', 'ab')
f.write("The most popular article authors of all time.\n")
for item in raw_result:
    f.write(str(item[0]))
    f.write(" --")
    f.write(str(item[1]) + " Views\n")
f.write("\n")
c.close()
f.close()

# 3.  On which days did more than 1%
# of requests lead to errors?

query_3 = """
select sub_0.date,
(sub_0.errors::decimal / sub_1.views) as err_rate from
(select
time::DATE as date, count(*) as errors from log
where status = '404 NOT FOUND'
group by time::DATE) as sub_0
join
(select time::DATE as date,
count(*) as views from log group by time::DATE) as sub_1
on sub_0.date = sub_1.date
where
sub_0.errors  > (0.01 * sub_1.views)
"""

db = psycopg2.connect(dbname=DBNAME)
c = db.cursor()
c.execute(query_3)
raw_result = c.fetchall()
f = open('results.txt', 'ab')
f.write("These days did more than 1% of requests lead to errors.\n")
for item in raw_result:
    f.write(str(item[0].strftime("%B %d, %Y")) + " --")
    f.write(
        "{0:.2f}". format(float(item[1]) * 100) +
        "% errors\n")

f.write("\n")
c.close()
f.close()
