import os

txt = ''
for x in os.listdir():
    txt += f'{x}\n'
print(txt)