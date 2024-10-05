import base64

def flipFlops(char):
    return chr(ord(char) - 1)

def reverse_promptGen():
    # Extract the base64-encoded strings
    bittysEnc = 'Zfo5ibyl6t7WYtr2voUEZ0nSAJeWMcN3Qe3/+MLXoKL/p59K3jgV'
    fourth = 'Ocmu{9gtufMmQg8G0eCXWi3MY9QfZ0NjCrXhzJEj50fumttU0ymp'

    # Reverse the flipFlops operation
    third = ""
    for each in fourth:
        third += flipFlops(each)

    # Decode the base64-encoded strings
    second = base64.b64decode(third+'=')
    bittys = base64.b64decode(bittysEnc)

    # Reverse the XOR operation
    onePointFive = int.from_bytes(second, 'little')
    first = (onePointFive ^ int.from_bytes(bittys, 'little')).to_bytes(len(second), 'little')

    return first

print(reverse_promptGen())
