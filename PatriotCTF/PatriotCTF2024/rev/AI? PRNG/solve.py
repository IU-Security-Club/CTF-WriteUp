import subprocess
import string
import itertools

command = 'echo "{}" | ./ai_rnd'
input_encode = b'a5 39 24 90 a8 a5 88 77 26 e4 3c 14 03 1e ba 3c 7d bb dc d6 aa 90 50 c9 0f aa dd 57 33 e1 a4 c7'.split(b' ')

out = open('output','wb')

def recur(idx, flag):
    print('Index:', idx, "\tPrevious string:", flag)
    if idx == 19:
        print(flag)
        input()
        return

    for c in string.printable:
        
        attempt_str = list(flag)
        attempt_str[idx] = c
    
        process = subprocess.Popen(command.format(''.join(attempt_str)), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        print("===>\t", ''.join(attempt_str))
        print("\t\t", output)

        try:
            if output.split(b' ')[idx] == input_encode[idx]:
                recur(idx + 1, ''.join(attempt_str))
        except:
            pass

recur(10, 'pctf{d33p_000000000')
