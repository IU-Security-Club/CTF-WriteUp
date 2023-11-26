a = ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '@', 'f', 'l', 'a', 'r', 'e', '-', 'o', 'n', '.', 'c', 'o', 'm']

a[0] = '0'
a[5] = 'R'
a[6] = '@' #chr(0x40)
a[12] = 'E' #chr(0x45)

def shellcode_1():
	v8 = "ten"
	arr = [0x16, 0x17, 0x3B, 0x17, 0x56]
	for i in range(5):
		arr[i] ^= ord(v8[i % 3])
	a[7:12] = [chr(i) for i in arr]

def stage_1():
	for i in range(32,127):
		for j in range(32,127):
			if 4*i + j == 295:
				a[1] = chr(i)
				a[2] = chr(j)
				print(''.join(a))

shellcode_1()
stage_1()

# 02_..R@brUc3E


  v3[0x8] = a1[1] = M
  v3[0x9] = a1[11] = Z
  v3[0x19] = a1[4] = E 
  v3[0x5C] = a1[2] = u
  v3[0x7A] = a1[3] = $
  v3[0x82] = a1[0] = a1[0xA] = A

  v8[0] = Source[12] = e
  v8[0x18] = Source[5] = `
  v8[0x1D] = Source[8] = . 
  v8[0x36] = Source[9] = *
  v8[0x50] = Source[7] = R
  v8[0x59] = Source[6] = 0

# v26 = [0x52, 0x7, 0x42, 0x1, 74, 29, 92, 25, 75, 31, 76, 5, 75, 12, 73, 7, 78, 11, 94, 12, 91, 30, 77, 8, 70]
# a = 0
# for i in range(len(v26)):
# 	tmp = v26[i] ^ a
# 	a = v26[i]
# 	v26[i] = tmp
# print(', '.join(hex(i) for i in v26))

aAz = 'AZBQCEDTEXFHGOHLIMJFKKLDMVNNOUPBQWRYSGTIUPVAWCXJYRZS'
# ABCDEFGHIJKLMNOPQRSTUVWXYZ
# ZQETXHOLMFKDVNUBWYGIPACJRS
aAzbqcedtexfhgo = [ 0x41, 0x5A, 0x42, 0x51, 0x43, 0x45, 0x44, 0x54, 0x45, 0x58, 
  0x46, 0x48, 0x47, 0x4F, 0x48, 0x4C, 0x49, 0x4D, 0x4A, 0x46, 
  0x4B, 0x4B, 0x4C, 0x44, 0x4D, 0x56, 0x4E, 0x4E, 0x4F, 0x55, 
  0x50, 0x42, 0x51, 0x57, 0x52, 0x59, 0x53, 0x47, 0x54, 0x49, 
  0x55, 0x50, 0x56, 0x41, 0x57, 0x43, 0x58, 0x4A, 0x59, 0x52, 
  0x5A, 0x53]

res = 'RUECKWAERTSINGENIEURWESEN'
result = [	0x52, 0x55, 0x45, 0x43, 0x4b, 0x57, 0x41, 0x45, 0x52, 0x54, 
			0x53, 0x49, 0x4E, 0x47, 0x45, 0x4E, 0x49, 0x45, 0x55, 0x52, 
			0x57, 0x45, 0x53, 0x45, 0x4E
		]

ori = [0] * 25
for i in range(25):
	t = 0
	while t < len(aAz):
		if result[i] == aAzbqcedtexfhgo[t]:
			ori[i] = aAzbqcedtexfhgo[t + 1]
			break
		else:
			t += 2
print(''.join([chr(i) for i in ori]))


a = '02_..R@brUc3E/1337pr.ost/0/.pizza/AMu$E`0R.*AZe/YPXEKCZXYIGMNOXNMXPYCXGXN/ob5cUr3/fin/'







