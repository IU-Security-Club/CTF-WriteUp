# password Protector

# Packed Full Of Surprises

# Puzzle Room

# AI? PRNG
- Open ELF file first, looking for input (that is the most important thing and needs tracing to find the change, and the effect of it on the result - flag) and find out that the file receives maximum 32 chars, then processing in `init` function.
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
