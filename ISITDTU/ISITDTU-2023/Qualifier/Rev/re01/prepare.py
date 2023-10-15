out_enc = [0] * 25

prime = [2, 3, 5, 7, 0x0B, 0x0D, 0x11, 0x13, 0x17, 0x1D, 0x1F, 0x25, 0x29, 0x2B, 0x2F, 0x35, 0x3B, 0x3D, 0x43, 0x47, 0x49, 0x4F, 0x53, 0x59, 0x61]

inp = "0123456789012345678901234"

cnt_i, cnt_j, cnt_k = 0, 0, 0

def stage_one():
    global cnt_i, cnt_j, cnt_k
    if cnt_i < 5:
        if cnt_j < 5:
            if cnt_k < 5:
                
                fo.write(f'a{cnt_i * 5 + cnt_k} * {prime[cnt_k * 5 + cnt_j]} \n')
                #print('enc ', cnt_i * 5 + cnt_j, ' prime ', cnt_k * 5 + cnt_j, ' input ', cnt_i * 5 + cnt_k)
                #out_enc[cnt_i * 5 + cnt_j] += prime[cnt_k * 5 + cnt_j] * ord(inp[cnt_i * 5 + cnt_k])
                
                cnt_k += 1
                stage_one()
            cnt_k = 0
            cnt_j += 1
            stage_one()
        cnt_j = 0
        cnt_i += 1
        stage_one()

# fo = open("temp.txt","w")
# stage_one()
# fo.close()


flag = [0x43AD, 0x4CFC, 0x52A8, 0x5AA2, 0x651C, 0x4881, 0x5203, 0x57DF, 0x6043, 0x6B51, 
        0x49C6, 0x538F, 0x5975, 0x6231, 0x6D6B, 0x42DC, 0x4C10, 0x51AC, 0x59B8, 0x6448, 
        0x1F63, 0x2475, 0x27C9, 0x2C8D, 0x333F]
def second_stage():
    cnt = 0
    with open('temp.txt',"r") as f:
        for i in range(0,25):
            s = 's.add('
            s += f.readline().strip() + ' + '
            s += f.readline().strip() + ' + '
            s += f.readline().strip() + ' + '
            s += f.readline().strip() + ' + '
            s += f.readline().strip()        
            s += f" == {flag[cnt]})"
            print(s)
            cnt += 1
#stage_two()


"""
enc  0  prime  0  input  0
enc  0  prime  5  input  1
enc  0  prime  10  input  2
enc  0  prime  15  input  3
enc  0  prime  20  input  4
enc  1  prime  1  input  0
enc  1  prime  6  input  1
enc  1  prime  11  input  2
enc  1  prime  16  input  3
enc  1  prime  21  input  4
enc  2  prime  2  input  0
enc  2  prime  7  input  1
enc  2  prime  12  input  2
enc  2  prime  17  input  3
enc  2  prime  22  input  4
enc  3  prime  3  input  0
enc  3  prime  8  input  1
enc  3  prime  13  input  2
enc  3  prime  18  input  3
enc  3  prime  23  input  4
enc  4  prime  4  input  0
enc  4  prime  9  input  1
enc  4  prime  14  input  2
enc  4  prime  19  input  3
enc  4  prime  24  input  4
enc  5  prime  0  input  5
enc  5  prime  5  input  6
enc  5  prime  10  input  7
enc  5  prime  15  input  8
enc  5  prime  20  input  9
enc  6  prime  1  input  5
enc  6  prime  6  input  6
enc  6  prime  11  input  7
enc  6  prime  16  input  8
enc  6  prime  21  input  9
enc  7  prime  2  input  5
enc  7  prime  7  input  6
enc  7  prime  12  input  7
enc  7  prime  17  input  8
enc  7  prime  22  input  9
enc  8  prime  3  input  5
enc  8  prime  8  input  6
enc  8  prime  13  input  7
enc  8  prime  18  input  8
enc  8  prime  23  input  9
enc  9  prime  4  input  5
enc  9  prime  9  input  6
enc  9  prime  14  input  7
enc  9  prime  19  input  8
enc  9  prime  24  input  9
enc  10  prime  0  input  10
enc  10  prime  5  input  11
enc  10  prime  10  input  12
enc  10  prime  15  input  13
enc  10  prime  20  input  14
enc  11  prime  1  input  10
enc  11  prime  6  input  11
enc  11  prime  11  input  12
enc  11  prime  16  input  13
enc  11  prime  21  input  14
enc  12  prime  2  input  10
enc  12  prime  7  input  11
enc  12  prime  12  input  12
enc  12  prime  17  input  13
enc  12  prime  22  input  14
enc  13  prime  3  input  10
enc  13  prime  8  input  11
enc  13  prime  13  input  12
enc  13  prime  18  input  13
enc  13  prime  23  input  14
enc  14  prime  4  input  10
enc  14  prime  9  input  11
enc  14  prime  14  input  12
enc  14  prime  19  input  13
enc  14  prime  24  input  14
enc  15  prime  0  input  15
enc  15  prime  5  input  16
enc  15  prime  10  input  17
enc  15  prime  15  input  18
enc  15  prime  20  input  19
enc  16  prime  1  input  15
enc  16  prime  6  input  16
enc  16  prime  11  input  17
enc  16  prime  16  input  18
enc  16  prime  21  input  19
enc  17  prime  2  input  15
enc  17  prime  7  input  16
enc  17  prime  12  input  17
enc  17  prime  17  input  18
enc  17  prime  22  input  19
enc  18  prime  3  input  15
enc  18  prime  8  input  16
enc  18  prime  13  input  17
enc  18  prime  18  input  18
enc  18  prime  23  input  19
enc  19  prime  4  input  15
enc  19  prime  9  input  16
enc  19  prime  14  input  17
enc  19  prime  19  input  18
enc  19  prime  24  input  19
enc  20  prime  0  input  20
enc  20  prime  5  input  21
enc  20  prime  10  input  22
enc  20  prime  15  input  23
enc  20  prime  20  input  24
enc  21  prime  1  input  20
enc  21  prime  6  input  21
enc  21  prime  11  input  22
enc  21  prime  16  input  23
enc  21  prime  21  input  24
enc  22  prime  2  input  20
enc  22  prime  7  input  21
enc  22  prime  12  input  22
enc  22  prime  17  input  23
enc  22  prime  22  input  24
enc  23  prime  3  input  20
enc  23  prime  8  input  21
enc  23  prime  13  input  22
enc  23  prime  18  input  23
enc  23  prime  23  input  24
enc  24  prime  4  input  20
enc  24  prime  9  input  21
enc  24  prime  14  input  22
enc  24  prime  19  input  23
enc  24  prime  24  input  24
"""