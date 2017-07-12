import ccircle
import connection

ADM_KEY='???'

con = connection.create()
con.send('set_name', {'name': '____________'})
con.send('adm_enable_ai', {'enabled': False})

def move_toward(vx, vy):
  con.send('adm_enable_ai', {'key':ADM_KEY,'enabled': False})
  con.send('adm_set_boss_velocity', {'key':ADM_KEY,'vx': vx, 'vy': vy})

move_toward(0, -10)

# Write code to make money and kill the evil cat!
# See readme.txt !
