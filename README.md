# logs-analysis
Create a reporting tool that prints out reports (in plain text name results.txt) based on the data in the database. This reporting tool is a Python program using the psycopg2 module to connect to the database.
This program solve below problems:
1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.

2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

3. On which days did more than 1% of requests lead to errors?

## Install
Environment: python 2.7, psycopg2, postgresql 9.58.

To create the database,type "sudo su postgres createdb news" at terminal.
To upload data, type "psql -d news -f newsdata.sql" at terminal. (newsdata.sql file is not included at GitHub.)
To run the program, type "python logs-analysis.py" at terminal. This will create or append result at a file name results.txt.
