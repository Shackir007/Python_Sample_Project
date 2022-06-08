##https://medium.com/@sdoshi579/to-read-emails-and-download-attachments-in-python-6d7d6b60269
import re

s = 'GeeksforGeeks: A computer science portal for geeks'

match = re.search(r'portal', s)

print('Start Index:', match.start())
print('End Index:', match.end())


#if c in '[@!#$%^&*()<>?/\|}{~:]'
#for c in 'Shackir' for c in '@Shackir'):
for i in ['Shackir','Ruhaila', 'Ir!s']:
    if any(c in '[@!#$%^&*()<>?/\|}{~:]' for c in i):
        print("Found")
    else:
        print('Not Found')
