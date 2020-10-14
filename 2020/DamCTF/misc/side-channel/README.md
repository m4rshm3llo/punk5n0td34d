# What do we have on the task?

A python script that is a guessing game. We have to guess the password by game design. How do we do it?</br>
Now let's see the script:</br>
```python
def init_password():
  global password
  global sample_password
  # seems super secure, right?
  password = "%08x" % secrets.randbits(32)
  sample_password = "%08x" % secrets.randbits(32)
```
In the code above, we see the generation of password. The password is 8 byte hex number.</br>
Okey, next intresting code is a guessing function:</br>
```python
def guess_password(s):
  print("Password guessing %s" % s)
  typed_password = ''
  correct_password = True
  for i in range(len(password)):
    user_guess = input("Guess character at position password[%d] = %s?\n" % (i, typed_password))
    typed_password += user_guess
    if user_guess != password[i]:
      # we will punish the users for supplying wrong char..
      time.sleep(0.3 * charactor_position_in_hex(password[i]))
      correct_password = False

  # to get the flag, please supply all 8 correct characters for the password..
  if correct_password:
    cat_flag()

  return correct_password
```
When we sent the wrong password character, the server will delay befor checking the next character of the password. Based on the delays, we can calculate the password character and this function call twice in main() function.</br>
The first call is used to calculate the password and the second call send the correct password</br>
# Solver
```python
from pwn  import remote
from time import time

p = remote('chals.damctf.xyz', 30318)
p.recvuntil('Password guessing Trial 1\n')

t0 = time()

ppp = ''

for i in range(16):
  p.recvuntil('?')

  t1 = time()
  total = t1-t0
  if i > 0 and len(ppp) != 8:
    ppp += '{:x}'.format(int(total // 0.3))

  if len(ppp) != 8: 
    p.sendline('0')
  else:
    p.sendline(ppp[i-8])
  t0 = time()

print(p.recvline())
print(p.recvline())
```
# Flag
dam{d0nT_d3l4y_th3_pRoC3sSiNg}
