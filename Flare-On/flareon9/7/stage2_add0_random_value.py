import re

with open("stage2_dump_get_random_value.js",'r') as f:
	inp = f.read()
	inp = inp.split('\n')

for i,s in enumerate(inp):
	if i<2: continue
	m = re.search(r'(?P<head>{b.*?)(?P<body>Math\.floor\(Math\.random\(\))(?P<end>.*?}else)', s)
	if m != None:
		#print('\n---',s)
		s = s[ : m.span(1)[0]] + '{t=Math.random();console.log(t);' + s[m.span(1)[0] + 1 : m.span(1)[1]] + 'Math.floor(t' + s[m.span(3)[0]:]
		#print('___',s)
		#input()
	m = re.search(r'(?P<head>e{.*?)(?P<body>Math\.floor\(Math\.random\(\))(?P<end>.*?}s)', s)
	if m != None:
		#print('\n---',s)
		s = s[ : m.span(1)[0]] + 'e{t=Math.random();console.log(t);' + s[m.span(1)[0] + 2 : m.span(1)[1]] + 'Math.floor(t' + s[m.span(3)[0]:]
		#print('___',s)
		#input()

	inp[i] = s

s = '\x0A'.join(inp)
s = s.encode()

print(hex(len(s)), 0x4e8c8 - len(s))

with open("stage2_result.js",'wb') as f:
	s += b' ' * (0x4e8c8 - len(s))
	s += b'\x0A'
	f.write(s)