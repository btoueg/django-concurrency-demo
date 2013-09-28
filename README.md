django-concurrency-demo
=======================

Minimal code to demonstrate a [concurrent requests issue](http://stackoverflow.com/questions/18958205/concurrent-requests-in-django).

Steps to reproduce:

 1. sync the database (assuming you have a PostgreSQL database named `concurrency`)
 2. create an product object in admin, with the stock field set to 1
 3. Run the server and then `test_script.py` several times
 4. Observe the stock field of product object obove has increased above 1
