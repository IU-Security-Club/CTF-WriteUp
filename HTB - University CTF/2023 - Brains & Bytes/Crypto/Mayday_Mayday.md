# [__Mayday Mayday__](#maydaymayday)
Difficulty: medium
## Given
```source.py```
```py
from Crypto.Util.number import getPrime, GCD, bytes_to_long
from secret import FLAG
from random import randint

class Crypto:
    def __init__(self, bits):
        self.bits = bits
        self.alpha = 1/9
        self.delta = 1/4
        self.known = int(self.bits*self.delta) #512
    
    def keygen(self):
        while True:
            p, q = [getPrime(self.bits//2) for _ in '__']
            self.e = getPrime(int(self.bits*self.alpha))
            φ = (p-1)*(q-1)
            try:
                dp = pow(self.e, -1, p-1)
                dq = pow(self.e, -1, q-1)
                self.n = p*q
                break
            except:
                pass

        return (self.n, self.e), (dp, dq)

    def encrypt(self, m):
        return pow(m, self.e, self.n)

rsa = Crypto(2048)
_, (dp, dq) = rsa.keygen()

m = bytes_to_long(FLAG)
c = rsa.encrypt(m)

with open('output.txt', 'w') as f:
    f.write(f'N = 0x{rsa.n:x}\n')
    f.write(f'e = 0x{rsa.e:x}\n')
    f.write(f'c = 0x{c:x}\n')
    f.write(f'dp = 0x{(dp >> (rsa.bits//2 - rsa.known)):x}\n') #512
    f.write(f'dq = 0x{(dq >> (rsa.bits//2 - rsa.known)):x}\n') #512
```
```output.txt```
```
N = 0x78fb80151a498704541b888b9ca21b9f159a45069b99b04befcb0e0403178dc243a66492771f057b28262332caecc673a2c68fd63e7c850dc534a74c705f865841c0b5af1e0791b8b5cc55ad3b04e25f20dedc15c36db46c328a61f3a10872d47d9426584f410fde4c8c2ebfaccc8d6a6bd1c067e5e8d8f107b56bf86ac06cd8a20661af832019de6e00ae6be24a946fe229476541b04b9a808375739681efd1888e44d41196e396af66f91f992383955f5faef0fc1fc7b5175135ab3ed62867a84843c49bdf83d0497b255e35432b332705cd09f01670815ce167aa35f7a454f8b26b6d6fd9a0006194ad2f8f33160c13c08c81fe8f74e13e84e9cdf6566d2f
e = 0x4b3393c9fe2e50e0c76920e1f34e0c86417f9a9ef8b5a3fa41b381355
c = 0x17f2b5a46e4122ff819807a9d92b6225c483cf93c9804381098ecd6b81f4670e94d8930001b760f1d26bc7aa7dda48c9e12809d20b33fdb4c4dd9190b105b7dab42e932b99aaff54023873381e7387f1b2b18b355d4476b664d44c40413d82a10635fe6e7322543943aed2dcfbe49764b8da70edeb88d6f63ee47f025be5f2f38319611ab74cd5db6f90f60870ecbb57a884f821d873db06aadf0e61ff74cc7d4c8fc1e527dba9b205220c6707f750822c675c530f8ad6956e41ab80911da49c3d6a7d27e93c44ba5968f2f47a9c5a2694c9d6da245ceffe9cab66b6043774f446b1b08ee4739d3cc716b87c8225a84d3c4ea2fdf68143d09f062c880a870554
dp = 0x59a2219560ee56e7c35f310a4d101061aa61e0ae4eae7605eb63784209ad488b4ed161e780811edd61bf593e2d385beccfd255b459382d8a9029943781b540e7
dq = 0x39719131fbfd8afbc972ca005a430d080775bf1a5b3e8b789aba5c5110a31bd155ff13fba1019bb6cb7db887685e34ca7966a891bfad029b55b92c11201559e5
```
## Analyzing
Nhận thấy được đây là bài về hệ thống mật mã RSA với 2048 bit. Như thông thường ta sẽ có ```n, c, e```. Chúng ta biết được thêm 512 MSB của ```dp``` và ```dq```.
## Solution
So với bài ```grhkm’s babyRSA - Bauhinia CTF 2023```, bài mà đã cho LSB của ```dp, dq``` thì với MSB nó sẽ dễ hơn nhiều với [paper](https://eprint.iacr.org/2022/271.pdf) tôi kiếm được từ bài đó.<br>
Nên tôi sẽ demo lại cái phần này nhưng với code.<br>
Ta có: $$ed_p=1+k(p-1)$$
$$ed_q=1+k(q-1)$$
Phần 3.1 cho ta công thức: 
$$kl = \dfrac{2^{2 \cdot 512}e^2d_pd_q}{N}$$

Ta còn có:
$$k+l=1-kl(N-1)\mod e$$
Với ```k+l``` và ```kl``` ta dễ dàng tìm được ```kl``` với ``k`` và ``l`` là nghiệm của: 
$$(x-k)(x-l)=0$$
$$x^2-(k+l)+kl=0$$
$$x^2-(1-kl(N-1))+kl=0 \mod e$$
Khi kiếm được ```k, l```, thông qua Lemma 3 ở phần 3.3 của paper, từ ```k``` ta có thể kiếm được LSB còn lại của ```dp``` và phân tích N thành thừa số qua ```GCD```.
$$ed_pL+ed_pM \cdot 2^i +k-1=kp$$
$$f(x)=x+ed_pM \cdot 2^i +k-1 \mod k \cdot N $$
$$p=\gcd(f(d_pL,N))$$
## Solve script
```py
from Crypto.Util.number import long_to_bytes


n = 0x78fb80151a498704541b888b9ca21b9f159a45069b99b04befcb0e0403178dc243a66492771f057b28262332caecc673a2c68fd63e7c850dc534a74c705f865841c0b5af1e0791b8b5cc55ad3b04e25f20dedc15c36db46c328a61f3a10872d47d9426584f410fde4c8c2ebfaccc8d6a6bd1c067e5e8d8f107b56bf86ac06cd8a20661af832019de6e00ae6be24a946fe229476541b04b9a808375739681efd1888e44d41196e396af66f91f992383955f5faef0fc1fc7b5175135ab3ed62867a84843c49bdf83d0497b255e35432b332705cd09f01670815ce167aa35f7a454f8b26b6d6fd9a0006194ad2f8f33160c13c08c81fe8f74e13e84e9cdf6566d2f
e = 0x4b3393c9fe2e50e0c76920e1f34e0c86417f9a9ef8b5a3fa41b381355
c = 0x17f2b5a46e4122ff819807a9d92b6225c483cf93c9804381098ecd6b81f4670e94d8930001b760f1d26bc7aa7dda48c9e12809d20b33fdb4c4dd9190b105b7dab42e932b99aaff54023873381e7387f1b2b18b355d4476b664d44c40413d82a10635fe6e7322543943aed2dcfbe49764b8da70edeb88d6f63ee47f025be5f2f38319611ab74cd5db6f90f60870ecbb57a884f821d873db06aadf0e61ff74cc7d4c8fc1e527dba9b205220c6707f750822c675c530f8ad6956e41ab80911da49c3d6a7d27e93c44ba5968f2f47a9c5a2694c9d6da245ceffe9cab66b6043774f446b1b08ee4739d3cc716b87c8225a84d3c4ea2fdf68143d09f062c880a870554
dp_high = 0x59a2219560ee56e7c35f310a4d101061aa61e0ae4eae7605eb63784209ad488b4ed161e780811edd61bf593e2d385beccfd255b459382d8a9029943781b540e7
dq_high = 0x39719131fbfd8afbc972ca005a430d080775bf1a5b3e8b789aba5c5110a31bd155ff13fba1019bb6cb7db887685e34ca7966a891bfad029b55b92c11201559e5


kl=((e**2)*dp_high*dq_high*2**1024)//n+1


R.<x> = PolynomialRing(GF(e))

f=x^2-(1-kl*(n-1))*x+kl
k=int(f.roots()[0][0])

R.<x> = PolynomialRing(Zmod(k*n))
i=512
f=e*(dp_high*(2**i))+e*x+k-1

dp_low=f.monic().small_roots(X=2**i,beta=0.4)[0]

p = gcd(int(f(dp_low)), n)
q = n//p
d = pow(e, -1, (p-1)*(q-1))
flag = long_to_bytes(int(pow(c, d, n)))
print(flag.decode())
# HTB{f4ct0r1ng_w1th_just_4_f3w_b1ts_0f_th3_CRT_3xp0n3nts!https://eprint.iacr.org/2022/271.pdf}
```