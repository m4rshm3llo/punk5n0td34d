import os
path = 'bins'
fread = lambda x : open(x, 'rb').read()

offset1 = 0x10ba
offset2 = 0x10d4
size = 3

res = ''
for i in range(111):
  fname = 'binary{}'.format(i)
  bin = fread(path + os.sep + fname)
  p1 = bin[offset1:offset1+size]
  p2 = bin[offset2:offset2+size]

  if p2[:2] != '\x80\xfa':
    print(fname)
    raise RuntimeError('Cmp not found.')

  if p1[:2] == '\x80\xEA':
    res += chr((ord(p2[2]) + ord(p1[2]))&0xff)
  elif p1[:2] == '\x80\xF2':
    res += chr(ord(p2[2]) ^ ord(p1[2]))
  elif p1[:2] == '\x80\xC2':
    res += chr((ord(p2[2]) - ord(p1[2]))&0xff)
  else:
    print(fname, res)
    raise RuntimeError('Instruction not found.')
print(res)