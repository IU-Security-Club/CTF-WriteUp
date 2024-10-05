# [__password Protector__](#passwordProtector)
- This chall gives me the .pyc file. As usual, I will check it and decompile it with `uncompyle6` immediately.
- However, this is a compiled python file with version 3.11 and it cannot be decompiled yet.

![image](https://github.com/user-attachments/assets/af5e03fa-0fed-48ce-a87b-589c11449841)

- Therefore, I have to use difference tool, [pycdc](https://github.com/zrax/pycdc) in order to get python bytecode disassembler and decompiler.
- Unfortunately, `pycdc` didnot support python 3.11 at all.

![image](https://github.com/user-attachments/assets/9f85c4ab-15bc-4de3-991c-e73532c58521)

- Hence, I have to read bytecode disassembler and decompile by myself.

![image](https://github.com/user-attachments/assets/fda82c3d-ad0b-4a83-b7ef-21016f0782c6)
![image](https://github.com/user-attachments/assets/1e6b4c3e-acd6-43d8-a3dc-c5aaf4b80fd8)

- But wait, we have ChatGPT, so just make them decompile these for me. And it does too well, of course.

![image](https://github.com/user-attachments/assets/d26ad371-e8cc-492d-be6b-613f57dd1d81)

- And reverse it for me too :P

![image](https://github.com/user-attachments/assets/5385d912-8369-4d7d-801b-63337f157b40)

[solve.py](./passwordProtected/solve.py)

# [__Puzzle Room__](#PuzzleRoom)
- This is a funny chall. Your mission to get to Shrine cell, and you will get a flag based on the content of your path.

![image](https://github.com/user-attachments/assets/61713312-ee70-46d9-8d3f-00632f9f8446)

- However, you have to follow some rules:
  * Do not get out of the box.
  * Do not step on the corner.
  * Do not step on the door.
  * Do not come back.
  * Do not step on cells, which have contents that you stepped before.

- We understood the rules, so just applied graph algorithms (DFS) and set rules as a condition to not follow this path and choose another. Just directly custom the code, delete some trash code and add DFS recursive function.

![image](https://github.com/user-attachments/assets/9a1e5088-f4e2-40d2-8219-ec9da15cb784)
![image](https://github.com/user-attachments/assets/1c9251c6-93d2-4e90-9a90-1959674a8ba8)

- That's it, all done and get the flag

![image](https://github.com/user-attachments/assets/32a4243e-acd8-4434-a6a1-de5919c1fa6f)

[solve.py](./Puzzle%20Room/solve.py)

# [__Packed Full Of Surprises__](#PackedFullOfSurprises)
- This is the simple chall with rev + crypto type. You just need to find `key` và `iv` for AES256-CFB128, then we can do decryption.

![image](https://github.com/user-attachments/assets/2ff5b8c5-e053-4686-b96f-7b4943002e53)

- Just one thing we have to do before analyzing is to check the attribute of ELF, and know that this ELF is being packed. The signature is in the strings of the file. Download UPX and unpack it directly. Hence, we can get the original file.

![image](https://github.com/user-attachments/assets/30fc6f7a-162d-4b1f-97c7-36bca6f5bdeb)

[decrypt.cpp](./Packed%20Full%20Of%20Surprises/decrypt.cpp)

# [__AI? PRNG__](#AIPRNG)
- Open ELF file first, looking for input (that is the most important thing and needs tracing to find the change, and the effect of it on the result - flag) and find out that the file receives a maximum of 32 chars, then processing on `init` function.

![image](https://github.com/user-attachments/assets/4b1f8777-704e-41d7-91f7-10501941f7c7)

- And the input will be double if it does not have 32 chars for the length then put it all for processing on `scramble`.

![image](https://github.com/user-attachments/assets/8e509a11-edbd-49fe-88ac-9b8cde99368a)

- On `scramble`, it goes through the string, calculates based on each of them, and returns hex char.

![image](https://github.com/user-attachments/assets/43832c4a-f980-4627-ab51-37a98e59ee04)
![image](https://github.com/user-attachments/assets/ca3ba09e-8aef-4952-bc16-2215226329af)

- For this type of context, you can use a trick in order to quickly analyze. That is input the prefix of `flag` and see if the output is permanent or not.

![image](https://github.com/user-attachments/assets/31b84a2a-fac9-4997-af1f-918bb416849e)

- In this case, we can say that output hex strings are processed char by char, permanent and unchangeable => Bruteforce able.

- Now we can write a brute for the flag. And do some guessing to make it faster by stopping earlier (identify the loop, and the meaning of the string...).
- But Remember to go through all printable characters, because the hex output could be the same.

![image](https://github.com/user-attachments/assets/5d647f49-9c2f-4c10-b3f7-7b4ae42bb721)
![image](https://github.com/user-attachments/assets/bac07669-f5c9-4c1f-afef-4c1c8729c3e0)
![image](https://github.com/user-attachments/assets/32396817-909d-4514-b26b-65df70d97204)

[solve.py](./AI%3F%20PRNG/solve.py)
