import ccircle
import connection
import random
import time

con = connection.create()

con.send('set_name', {'name': 'put_your_name_or_nickname_here'})

for i in range(10):
    con.send('set_velocity', {'vx': random.randint(30, 50), 'vy': random.randint(-50, 50)})
    time.sleep(1)