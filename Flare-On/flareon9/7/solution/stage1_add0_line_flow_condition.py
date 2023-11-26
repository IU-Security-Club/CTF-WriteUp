with open("stage1_line_flow_condition.js",'r') as f:
	s = f.read()
	s = s.split('\n')

j = 0
for i in range(len(s)):
	if 'case' in s[i]:
		s[i] = s[i].replace("console.log('1')",f"console.log('1_{j}')")
		s[i] = s[i].replace("console.log('2')",f"console.log('2_{j}')")
		j += 1
s = '\x0A'.join(s)
s = s.encode()
print(hex(len(s)), 0x4e8c8 - len(s))

with open("stage1_result.js",'wb') as f:
	s += b' ' * (0x4e8c8 - len(s))
	s += b'\x0A'
	f.write(s)