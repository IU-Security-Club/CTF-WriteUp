"""
flag_cipher = Šúceœ^öž¹ÃÜè²1:ãm”†4!F+oè­0*yèê{f	ØÐX=—kòª`…HM—qê‚5ºKüQä­i+æ%[
m_constant = 0x9f18776bd3e78835b5ea24259706d89cbe7b5a79010afb524609efada04d0d71170a83c853525888c942e0dd1988251dfdb3cd85e95ce22a5712fb5e235dc5b6ffa3316b54166c55dd842101b1d77a41fdcc08a43019c218a8f8274e8164be2e857680c2b11554b8d593c2f13af2704e85847f80a1fc01b9906e22baba2f82a1
N = 0xdc425c720400e05a92eeb68d0313c84a978cbcf47474cbd9635eb353af864ea46221546a0f4d09aaa0885113e31db53b565c169c3606a241b569912a9bf95c91afbc04528431fdcee6044781fbc8629b06f99a11b99c05836e47638bbd07a232c658129aeb094ddaf4c3ad34563ee926a87123bc669f71eb6097e77c188b9bc9
cipherMess_m_constant = 0x8e678f043c0d8b8d3dff39b28ce9974ff7d4162473080b54eefaa6decb8827717c6b24edfff7063375b6588acf8eca35c2033ef8ebe721436de6f2f66569b03df8c5861a68e57118c9f854b2e62ca9871f7207fafa96aceba11ffd37b6c4dbf95b256184983bad407c7973e84b23cd22579dd25bf4c1a03734d1a7b0dfdcfd44
cipher_key_ChaCha = 0x5a04e95cd0e9bf0c8cdda2cbb0f50e7db8c89af791b4e88fd657237c1be4e6599bc4c80fd81bdb007e43743020a245d5f87df1c23c4d129b659f90ece2a5c22df1b60273741bf3694dd809d2c485030afdc6268431b2287c597239a8e922eb31174efcae47ea47104bc901cea0abb2cc9ef974d974f135ab1f4899946428184c
"""
import binascii

cipher_key_chacha = 0x5a04e95cd0e9bf0c8cdda2cbb0f50e7db8c89af791b4e88fd657237c1be4e6599bc4c80fd81bdb007e43743020a245d5f87df1c23c4d129b659f90ece2a5c22df1b60273741bf3694dd809d2c485030afdc6268431b2287c597239a8e922eb31174efcae47ea47104bc901cea0abb2cc9ef974d974f135ab1f4899946428184c

N = 0xdc425c720400e05a92eeb68d0313c84a978cbcf47474cbd9635eb353af864ea46221546a0f4d09aaa0885113e31db53b565c169c3606a241b569912a9bf95c91afbc04528431fdcee6044781fbc8629b06f99a11b99c05836e47638bbd07a232c658129aeb094ddaf4c3ad34563ee926a87123bc669f71eb6097e77c188b9bc9
e = 65537

#cipher_key_chacha = (key_chacha ^ d) mod N
key_chacha = pow(cipher_key_chacha, e, N)

"""
# bignum
key = key_chacha & (2**256 - 1)					# 256-bit
counter = (key_chacha >> 256) & 0xFFFFFFFF		# 32-bit
nonce = key_chacha >> 288 						# 96-bit
"""
""" 
# bytes array
key(256bits) + counter(32bits) + nonce(96bits)
key_chacha = [ 				
							01 b0 97 a1 2a 39 fc 42 
	05 24 a2 e7 75 a7 43 c9 28 d5 a5 50 b1 87 9a a8 
	b4 15 57 1e 38 32 9b 98 00 00 00 00 02 49 fc 0f 
	c8 33 40 fe 4d 92 8f 95 						
]
"""


key_chacha = '{:02x}'.format(key_chacha)

l = len(key_chacha)
key = binascii.unhexlify(''.join([key_chacha[i-1:i+1] for i in range(l-1, l-(32*2)-1, -2)]))
nonce = binascii.unhexlify(''.join([key_chacha[i-1:i+1] for i in range(l-(36*2)-1, -1, -2)]))

with open('SuspiciousFile.txt.Encrypted', 'rb') as f:
	flag_cipher = f.read().split(b'0x0A')[0][:73]

from Cryptodome.Cipher import ChaCha20

cipher = ChaCha20.new(key=key, nonce=nonce)
flag = cipher.encrypt(flag_cipher)

print(flag)

