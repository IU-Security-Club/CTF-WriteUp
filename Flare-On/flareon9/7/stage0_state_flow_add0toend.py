with open("stage0_state_flow.js",'rb') as f:
	s = f.read()
	print(hex(len(s)), 0x4e8c8 - len(s))
with open("stage0_state_flow_rs.js",'wb') as f:
	s += b' ' * (0x4e8c8 - len(s))
	s += b'\x0A'
	f.write(s)