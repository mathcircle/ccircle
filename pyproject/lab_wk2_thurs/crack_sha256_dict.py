from hashlib import sha256
from sys import byteorder

print('--- SHA-256 Dictionary Cracker -----------------------------------------\n')
print('  * Loading dictionary...')
entries = open('passwords.txt', 'rb').readlines()

target_hash = input('\n  Enter Hash:\n    > ')

print('\n  * Now checking %d dictionary entries...' % len(entries))
for password in entries:
  password = password[:-1]
  pass_hash = sha256(password).hexdigest()
  if pass_hash == target_hash:
    print('\n--- SUCCESS! ------------------------------------------------------------\n')
    print('  %s  ->  %s' % (str(password, 'utf-8'), pass_hash))
    break
else:
    print('\n--- FAILURE -------------------------------------------------------------\n')
    print('  No dictionary entries matched the target hash.')

input()
