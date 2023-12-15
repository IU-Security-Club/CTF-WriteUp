from z3 import *

n = 38
s = Solver()

for i in range(n):
    globals()['a%d' % i] = BitVec('a%d' % i, 8)

s.add(32 <= a0, a0 <= 126, 32 <= a1, a1 <= 126, 32 <= a2, a2 <= 126, 32 <= a3, a3 <= 126, 32 <= a4, a4 <= 126, 32 <= a5, a5 <= 126, 32 <= a6, a6 <= 126, 32 <= a7, a7 <= 126, 32 <= a8, a8 <= 126, 32 <= a9, a9 <= 126, 32 <= a10, a10 <= 126, 32 <= a11, a11 <= 126, 32 <= a12, a12 <= 126, 32 <= a13, a13 <= 126, 32 <= a14, a14 <= 126, 32 <= a15, a15 <= 126, 32 <= a16, a16 <= 126, 32 <= a17, a17 <= 126, 32 <= a18, a18 <= 126, 32 <= a19, a19 <= 126, 32 <= a20, a20 <= 126, 32 <= a21, a21 <= 126, 32 <= a22, a22 <= 126, 32 <= a23, a23 <= 126, 32 <= a24, a24 <= 126, 32 <= a25, a25 <= 126, 32 <= a26, a26 <= 126, 32 <= a27, a27 <= 126, 32 <= a28, a28 <= 126, 32 <= a29, a29 <= 126, 32 <= a30, a30 <= 126, 32 <= a31, a31 <= 126, 32 <= a32, a32 <= 126, 32 <= a33, a33 <= 126, 32 <= a34, a34 <= 126, 32 <= a35, a35 <= 126, 32 <= a36, a36 <= 126, 32 <= a37, a37 <= 126)

s.add(a0 + a1 == 156)
s.add(a1 + a2 == 150)
s.add(a2 + a3 == 189)
s.add(a3 + a4 == 175)
s.add(a4 + a5 == 147)
s.add(a5 + a6 == 195)
s.add(a6 + a7 == 148)
s.add(a7 + a8 == 96)
s.add(a8 + a9 == 162)
s.add(a9 + a10 == 209)
s.add(a10 + a11 == 194)
s.add(a11 + a12 == 207)
s.add(a12 + a13 == 156)
s.add(a13 + a14 == 163)
s.add(a14 + a15 == 166)
s.add(a15 + a16 == 104)
s.add(a16 + a17 == 148)
s.add(a17 + a18 == 193)
s.add(a18 + a19 == 215)
s.add(a19 + a20 == 172)
s.add(a20 + a21 == 150)
s.add(a21 + a22 == 147)
s.add(a22 + a23 == 147)
s.add(a23 + a24 == 214)
s.add(a24 + a25 == 168)
s.add(a25 + a26 == 159)
s.add(a26 + a27 == 210)
s.add(a27 + a28 == 148)
s.add(a28 + a29 == 167)
s.add(a29 + a30 == 214)
s.add(a30 + a31 == 143)
s.add(a31 + a32 == 160)
s.add(a32 + a33 == 163)
s.add(a33 + a34 == 161)
s.add(a34 + a35 == 163)
s.add(a35 + a36 == 86)
s.add(a36 + a37 == 158)

print(s.model)

while s.check() == sat:
    model = s.model()
    block = []
    flag = ''

    for i in range(n):
        c = globals()['a%d' % i]
        flag += chr(model[c].as_long())

        block.append(c != model[c])
    s.add(Or(block))

    print(flag)
