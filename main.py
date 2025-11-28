from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import encoder
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://enigmawebsiteappvercel.vercel.app"],  # Next.js dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    text: str

def enigma_encode(inputstr: str):

    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    plugboard = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
    rota1 = list("EKMFLGDQVZNTOWYHXUSPAIBRCJ")
    rota2 = list("AJDKSIRUXBLHWTMCQGZNPYFVOE")
    rota3 = list("BDFHJLCPRTXVZNYEIWGAKMUSQO")
    reflector = list("EJMZALYXVBWFCRQUONTSPIKHGD")
    rota1notch = "Q"
    rota2notch = "E"
    rota3notch = "V"

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

@app.post("/encode")
def encode_message(message: Message):
    encoded = enigma_encode(message.text)
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
    # Must encode only one letter, no stepping
    encoded = encoder.enigma_single_letter(letter, left, middle, right)
    return encoded[0]

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
    return cipher_section == crib

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
                    if crib_matches(ciphertext, plaintext, offset, l_letter, m_letter, r_letter):
                        decoded = encoder.enigma_encode(ciphertext, l_letter, m_letter, r_letter)
                        results.append({
                            "offset": offset,
                            "rotor_positions": {"left": l_letter, "middle": m_letter, "right": r_letter},
                            "decoded": decoded
                        })
    return {"results": results}