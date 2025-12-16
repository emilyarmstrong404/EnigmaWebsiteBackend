from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import encoder
import os
import uvicorn
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #"https://enigmawebsiteappvercel.vercel.app"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    text: str
    keys: list[str]  # [left, middle, right]

def step_rotor(rotor):
    """Rotate rotor by one position."""
    return rotor[1:] + rotor[:1]

##############
# def enigma_encode(inputstr: str, left_rotor_pos, middle_rotor_pos, right_rotor_pos):
#     alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    
#     plugboard = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
#                  " ", " ", " ", " ", " "]
#     plugBoard = {a: a for a in alphabet}
#     for a, p in zip(alphabet, plugboard):
#         if p != " ":
#             plugBoard[a] = p
#             plugBoard[p] = a
            
#     rota1 = list("EKMFLGDQVZNTOWYHXUSPAIBRCJ")
#     rota2 = list("AJDKSIRUXBLHWTMCQGZNPYFVOE")
#     rota3 = list("BDFHJLCPRTXVZNYEIWGAKMUSQO")
#     reflector = list("EJMZALYXVBWFCRQUONTSPIKHGD")
#     rota1notch = "Q"
#     rota2notch = "E"
    
#     reFlector = dict(zip(alphabet, reflector))

#     while rota1[0] != right_rotor_pos:
#         rota1 = rota1[1:] + rota1[:1]
#     while rota2[0] != middle_rotor_pos:
#         rota2 = rota2[1:] + rota2[:1]
#     while rota3[0] != left_rotor_pos:
#         rota3 = rota3[1:] + rota3[:1]

#     inputstr = inputstr.strip().upper()
#     inputstrlist = list(inputstr)
#     encoded_str = []

#     def encode_letter(lettertoencode: str):
#         nonlocal rota1, rota2, rota3

#         rightrotaprestep = rota1[0]
#         middlerotaprestep = rota2[0]

#         rota1.append(rota1[0])
#         rota1.pop(0)

#         if rightrotaprestep == rota1notch or middlerotaprestep == rota2notch:
#             rota2.append(rota2[0])
#             rota2.pop(0)

#         if middlerotaprestep == rota2notch:
#             rota3.append(rota3[0])
#             rota3.pop(0)

#         RRota = dict(zip(alphabet, rota1))
#         MRota = dict(zip(alphabet, rota2))
#         LRota = dict(zip(alphabet, rota3))

        

#         LRota_inv = {v: k for k, v in LRota.items()}
#         MRota_inv = {v: k for k, v in MRota.items()}
#         RRota_inv = {v: k for k, v in RRota.items()}

#         return plugBoard[RRota_inv[MRota_inv[LRota_inv[reFlector[LRota[MRota[RRota[plugBoard[lettertoencode]]]]]]]]]

#     for eachletter in inputstrlist:
#         encoded_letter = encode_letter(eachletter)
#         encoded_str.append(encoded_letter)
#     return "".join(encoded_str)
#############

def enigma_encode(inputstr, left_rotor_pos, middle_rotor_pos, right_rotor_pos):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    char_to_i = {c: i for i, c in enumerate(alphabet)}

    # rotors
    r1 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
    r2 = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
    r3 = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
    reflector = "EJMZALYXVBWFCRQUONTSPIKHGD"

    r1_map = [char_to_i[c] for c in r1]
    r2_map = [char_to_i[c] for c in r2]
    r3_map = [char_to_i[c] for c in r3]
    ref_map = [char_to_i[c] for c in reflector]

    r1_inv = [r1_map.index(i) for i in range(26)]
    r2_inv = [r2_map.index(i) for i in range(26)]
    r3_inv = [r3_map.index(i) for i in range(26)]

    r1_pos = char_to_i[right_rotor_pos]
    r2_pos = char_to_i[middle_rotor_pos]
    r3_pos = char_to_i[left_rotor_pos]

    r1_notch = char_to_i["Q"]
    r2_notch = char_to_i["E"]

    result = []

    for ch in inputstr.upper():
        # stepping (double-step)
        if r2_pos == r2_notch:
            r3_pos = (r3_pos + 1) % 26
            r2_pos = (r2_pos + 1) % 26
        elif r1_pos == r1_notch:
            r2_pos = (r2_pos + 1) % 26

        r1_pos = (r1_pos + 1) % 26

        i = char_to_i[ch]

        # forward
        i = r1_map[(i + r1_pos) % 26]
        i = r2_map[(i + r2_pos) % 26]
        i = r3_map[(i + r3_pos) % 26]

        # reflector
        i = ref_map[i]

        # backward
        i = (r3_inv[i] - r3_pos) % 26
        i = (r2_inv[i] - r2_pos) % 26
        i = (r1_inv[i] - r1_pos) % 26

        result.append(alphabet[i])

    return "".join(result)

def enigma_single_letter(letter, left, middle, right):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    char_to_i = {c: i for i, c in enumerate(alphabet)}

    r1 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
    r2 = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
    r3 = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
    reflector = "EJMZALYXVBWFCRQUONTSPIKHGD"

    r1_map = [char_to_i[c] for c in r1]
    r2_map = [char_to_i[c] for c in r2]
    r3_map = [char_to_i[c] for c in r3]
    ref_map = [char_to_i[c] for c in reflector]

    r1_inv = [r1_map.index(i) for i in range(26)]
    r2_inv = [r2_map.index(i) for i in range(26)]
    r3_inv = [r3_map.index(i) for i in range(26)]

    r1_pos = char_to_i[right]
    r2_pos = char_to_i[middle]
    r3_pos = char_to_i[left]

    i = char_to_i[letter]

    # forward (NO stepping)
    i = r1_map[(i + r1_pos) % 26]
    i = r2_map[(i + r2_pos) % 26]
    i = r3_map[(i + r3_pos) % 26]

    # reflector
    i = ref_map[i]

    # backward
    i = (r3_inv[i] - r3_pos) % 26
    i = (r2_inv[i] - r2_pos) % 26
    i = (r1_inv[i] - r1_pos) % 26

    return alphabet[i]


@app.post("/encode")
def encode_message(message: Message):
    # Expecting exactly 3 single-letter rotor positions
    if len(message.keys) != 3:
        return {"error": "Exactly 3 rotor letters are required"}

    left, middle, right = [k.upper() for k in message.keys]

    encoded = enigma_encode(
        message.text,
        left_rotor_pos=left,
        middle_rotor_pos=middle,
        right_rotor_pos=right
    )

    return {"encoded": encoded}




alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

class EncodeRequest(BaseModel):
    plaintext: str
    ciphertext: str

# --- Core Enigma functions ---

def crib_finder(ciphertext: str, plaintext: str):
    cipherarray = list(ciphertext)
    plainarray = list(plaintext)
    validList = []

    for offset in range(len(ciphertext) - len(plaintext) + 1):
        valid = True
        for i in range(len(plaintext)):
            if cipherarray[i + offset] == plainarray[i]:
                valid = False
                break
        if valid:
            validList.append(offset)
    return validList

def menu_builder(ciphertext: str, crib: str, offset: int):
    neighbour_dict = {ch: set() for ch in alphabet}
    edges = []
    for i in range(len(crib)):
        p = crib[i]
        c = ciphertext[offset + i]
        if p != c:
            neighbour_dict[p].add(c)
            neighbour_dict[c].add(p)
            edges.append((p, c, offset+i))
    neighbour_dict = {k: v for k, v in neighbour_dict.items() if v}
    return neighbour_dict, edges

def find_cycles(neighbour_dict: dict):
    visited = set()
    cycles = []

    def dfs(node, parent, path):
        path.append(node)
        for neighbor in neighbour_dict[node]:
            if neighbor not in path:
                dfs(neighbor, node, path)
            elif neighbor != parent:
                cycle_start_index = path.index(neighbor)
                cycle = path[cycle_start_index:].copy()
                if not any(set(cycle) == set(c) for c in cycles):
                    cycles.append(cycle)
        path.pop()

    for node in neighbour_dict:
        if node not in visited:
            dfs(node, None, [])

    return cycles

def encode_single_letter(letter, left, middle, right):
    return enigma_single_letter(letter, left, middle, right)

def enigma_rotors(cycles, edges, right_letter, middle_letter, left_letter):
    for cycle in cycles:
        n = len(cycle)
        for index in range(n):
            letter = cycle[index]
            expected = cycle[(index + 1) % n]
            result = encode_single_letter(letter, left_letter, middle_letter, right_letter)
            if result != expected:
                return False

    for edge in edges:
        encoded_crib_letter = encode_single_letter(edge[0], left_letter, middle_letter, right_letter)
        if encoded_crib_letter == edge[1]:
            return False
    return True

def crib_matches(ciphertext, crib, offset, left, middle, right):
    encoded_cipher = encoder.enigma_encode(ciphertext, left, middle, right)
    cipher_section = encoded_cipher[offset:offset+len(crib)]
    if cipher_section == crib:
        return encoded_cipher
    else:
        return None
    # return cipher_section == crib

# def crib_matches(ciphertext, crib, offset, left, middle, right):
#     for i, crib_letter in enumerate(crib):
#         encoded = enigma_single_letter(
#             ciphertext[offset + i], left, middle, right
#         )
#         if encoded != crib_letter:
#             return False
#     return True

# --- FastAPI route ---
@app.post("/crib")
def run_bombe(req: EncodeRequest):
    ciphertext = req.ciphertext.upper()
    plaintext = req.plaintext.upper()

    rotorR = list("EKMFLGDQVZNTOWYHXUSPAIBRCJ")  # Right rotor
    rotorM = list("AJDKSIRUXBLHWTMCQGZNPYFVOE")  # Middle rotor
    rotorL = list("BDFHJLCPRTXVZNYEIWGAKMUSQO")  # Left rotor

    results = []

    crib_list = crib_finder(ciphertext, plaintext)
    for offset in crib_list:
        neighbour_dict, edges = menu_builder(ciphertext, plaintext, offset)
        cycles = find_cycles(neighbour_dict)

        for left_pos in range(26):
            l_letter = alphabet[left_pos]
            for middle_pos in range(26):
                m_letter = alphabet[middle_pos]
                for right_pos in range(26):
                    r_letter = alphabet[right_pos]
                    if not enigma_rotors(cycles, edges, r_letter, m_letter, l_letter):
                        continue
                    decoded = crib_matches(ciphertext, plaintext, offset, l_letter, m_letter, r_letter)
                    if decoded is not None:
                    # if crib_matches(ciphertext, plaintext, offset, l_letter, m_letter, r_letter):
                        # decoded = enigma_encode(ciphertext, l_letter, m_letter, r_letter)
                        results.append({
                            "offset": offset,
                            "rotor_positions": {"left": l_letter, "middle": m_letter, "right": r_letter},
                            "decoded": decoded
                        })
    return {"results": results}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render sets PORT automatically
    uvicorn.run(app, host="0.0.0.0", port=port)