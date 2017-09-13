#!/usr/bin/python
import io
import psycopg2


DBNAME = "news"
# 1. What are the most popular three articles of all time?
query_1 = """
 SELECT articles.slug, COUNT(*) AS views
 FROM log JOIN articles on
 log.path LIKE CONCAT('%', articles.slug)
 GROUP BY articles.slug, log.path
 ORDER BY views DESC limit 3
 """

db = psycopg2.connect(dbname=DBNAME)
c = db.cursor()
c.execute(query_1)
raw_result = c.fetchall()
f = open('results.txt', 'ab')
f.write("The most popular three articles of all time.\n")
print("The most popular three articles of all time.")
for item in raw_result:
    title = str(
        item[0].replace("-", " ")).title()
    views = int(item[1])
    f.write(title + " --" + str(views) + " Views\n")
    print(title + " --" + str(views) + " Views")
f.write("\n")
print("")
c.close()
f.close()

# 2. Who are the most popular article authors
# of all time? Present this as a sorted list
# with the most popular author at the top.

query_2 = """
 SELECT
 authors.name, sum(sub.views) AS sum_views
 FROM
 (SELECT articles.slug, articles.author,
 COUNT(*)AS views
 FROM log JOIN articles
 on log.path LIKE CONCAT('%', articles.slug)
 GROUP BY articles.slug, log.path, articles.author
 ) sub
 JOIN authors ON sub.author = authors.id
 GROUP BY authors.id, sub.author
 ORDER BY sum_views DESC
"""
db = psycopg2.connect(dbname=DBNAME)
c = db.cursor()
c.execute(query_2)
raw_result = c.fetchall()
f = open('results.txt', 'ab')
f.write("The most popular article authors of all time.\n")
print("The most popular article authors of all time.")
for item in raw_result:
    f.write(str(item[0]) + " --" + str(item[1]) + " Views\n")
    print(str(item[0]) + " --" + str(item[1]) + " Views")
f.write("\n")
print("")
c.close()
f.close()

# 3.  On which days did more than 1%
# of requests lead to errors?

query_3 = """
SELECT sub_0.date,
(sub_0.errors::decimal / sub_1.views) AS err_rate FROM
(SELECT
time::DATE AS date, COUNT(*) AS errors FROM log
where status = '404 NOT FOUND'
GROUP BY time::DATE) AS sub_0
JOIN
(SELECT time::DATE AS date,
COUNT(*) AS views FROM log GROUP BY time::DATE) AS sub_1
on sub_0.date = sub_1.date
WHERE
sub_0.errors  > (0.01 * sub_1.views)
"""

db = psycopg2.connect(dbname=DBNAME)
c = db.cursor()
c.execute(query_3)
raw_result = c.fetchall()
f = open('results.txt', 'ab')
f.write("These days did more than 1% of requests lead to errors.\n")
print("These days did more than 1% of requests lead to errors.")
for item in raw_result:
    f.write(str(item[0].strftime("%B %d, %Y")) +
            " --" "{0:.2f}". format(float(item[1]) * 100) +
            "% errors\n")
    print(str(item[0].strftime("%B %d, %Y")) +
          " --" "{0:.2f}". format(float(item[1]) * 100) +
          "% errors")

f.write("\n")
print("")
c.close()
f.close()
