from hashlib import sha256
from sys import byteorder

print('--- SHA-256 Brute-Force Cracker -----------------------------------------\n')
target_hash = input('  Enter Hash:\n    > ')

i = 0
byte_len = 1
byte_range = 256
print('\n  * Now checking all 256 passwords of length 1...')
while True:
  pass_bytes = i.to_bytes(byte_len, byteorder='little')
  pass_hash = sha256(pass_bytes).hexdigest()

  if pass_hash == target_hash:
    print('\n--- SUCCESS! ------------------------------------------------------------\n')
    print('  %s  ->  %s' % (str(pass_bytes, 'utf-8'), pass_hash))
    break

  i += 1

  if i == byte_range:
    byte_len += 1
    byte_range *= 256
    print('  * Now checking all {} passwords of length {}...'.format(byte_range, byte_len))

input()
