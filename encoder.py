def step_rotor(rotor):
    """Rotate rotor by one position."""
    return rotor[1:] + rotor[:1]


def enigma_encode(inputstr: str, left_rotor_pos, middle_rotor_pos, right_rotor_pos):
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    plugboard = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                 " ", " ", " ", " ", " "]
    rota1 = list("EKMFLGDQVZNTOWYHXUSPAIBRCJ")
    rota2 = list("AJDKSIRUXBLHWTMCQGZNPYFVOE")
    rota3 = list("BDFHJLCPRTXVZNYEIWGAKMUSQO")
    reflector = list("EJMZALYXVBWFCRQUONTSPIKHGD")
    rota1notch = "Q"
    rota2notch = "E"

    while rota1[0] != right_rotor_pos:
        rota1 = rota1[1:] + rota1[:1]
    while rota2[0] != middle_rotor_pos:
        rota2 = rota2[1:] + rota2[:1]
    while rota3[0] != left_rotor_pos:
        rota3 = rota3[1:] + rota3[:1]

    inputstr = inputstr.strip().upper()
    inputstrlist = list(inputstr)
    encoded_str = []

    def encode_letter(lettertoencode: str):
        nonlocal rota1, rota2, rota3

        rightrotaprestep = rota1[0]
        middlerotaprestep = rota2[0]

        rota1.append(rota1[0])
        rota1.pop(0)

        if rightrotaprestep == rota1notch or middlerotaprestep == rota2notch:
            rota2.append(rota2[0])
            rota2.pop(0)

        if middlerotaprestep == rota2notch:
            rota3.append(rota3[0])
            rota3.pop(0)

        RRota = dict(zip(alphabet, rota1))
        MRota = dict(zip(alphabet, rota2))
        LRota = dict(zip(alphabet, rota3))

        reFlector = dict(zip(alphabet, reflector))

        LRota_inv = {v: k for k, v in LRota.items()}
        MRota_inv = {v: k for k, v in MRota.items()}
        RRota_inv = {v: k for k, v in RRota.items()}

        plugBoard = {a: a for a in alphabet}
        for a, p in zip(alphabet, plugboard):
            if p != " ":
                plugBoard[a] = p
                plugBoard[p] = a

        return plugBoard[RRota_inv[MRota_inv[LRota_inv[reFlector[LRota[MRota[RRota[plugBoard[lettertoencode]]]]]]]]]

    for eachletter in inputstrlist:
        encoded_letter = encode_letter(eachletter)
        encoded_str.append(encoded_letter)
    return "".join(encoded_str)

def enigma_single_letter(letter, left_rotor_pos, middle_rotor_pos, right_rotor_pos) -> str:
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    rota1 = list("EKMFLGDQVZNTOWYHXUSPAIBRCJ")
    rota2 = list("AJDKSIRUXBLHWTMCQGZNPYFVOE")
    rota3 = list("BDFHJLCPRTXVZNYEIWGAKMUSQO")
    reflector = list("EJMZALYXVBWFCRQUONTSPIKHGD")

    # Set rotors to starting positions
    while rota1[0] != right_rotor_pos:
        rota1 = rota1[1:] + rota1[:1]
    while rota2[0] != middle_rotor_pos:
        rota2 = rota2[1:] + rota2[:1]
    while rota3[0] != left_rotor_pos:
        rota3 = rota3[1:] + rota3[:1]

    # No stepping at all
    RRota = dict(zip(alphabet, rota1))
    MRota = dict(zip(alphabet, rota2))
    LRota = dict(zip(alphabet, rota3))
    reFlector = dict(zip(alphabet, reflector))
    LRota_inv = {v: k for k, v in LRota.items()}
    MRota_inv = {v: k for k, v in MRota.items()}
    RRota_inv = {v: k for k, v in RRota.items()}

    return RRota_inv[MRota_inv[LRota_inv[reFlector[LRota[MRota[RRota[letter]]]]]]]


def enigma_run():
    print("enter plain text: ")
    plaintext = input()
    plaintext = plaintext.strip().upper()

    print("enter right rota position letter: ")
    rPos = input()
    rPos = rPos.strip().upper()

    print("enter middle rota position letter: ")
    mPos = input()
    mPos = mPos.strip().upper()

    print("enter left rota position letter: ")
    lPos = input()
    lPos = lPos.strip().upper()

    encoded = enigma_encode(plaintext, lPos, mPos, rPos)
    print(encoded)
    return encoded

if __name__ == "__main__":
    enigma_run()
