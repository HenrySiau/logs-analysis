# logs-analysis
Create a reporting tool that prints out reports (in plain text name results.txt) based on the data in the database. This reporting tool is a Python program using the psycopg2 module to connect to the database.
This program solve below problems:
1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.

2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

3. On which days did more than 1% of requests lead to errors?

## Install
use python 2.7, psycopg2, postgresql 9.58, database name: news, sql file is not included at GitHub.
run logs-analysis.py will create or append result at results.txt
