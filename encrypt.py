import streamlit as st
import re

# Function to generate Playfair key matrix
def generate_matrix(key):
    key = key.upper().replace("J", "I")  # Replace J with I
    matrix = []
    used = set()

    for char in key:
        if char.isalpha() and char not in used:
            used.add(char)
            matrix.append(char)

    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":  # No J
        if char not in used:
            used.add(char)
            matrix.append(char)

    return [matrix[i:i+5] for i in range(0, 25, 5)]

# Function to find position of a character
def find_position(matrix, char):
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            if val == char:
                return i, j
    return None

# Preprocess plaintext (insert X between duplicates, pad if odd length)
def prepare_text(plaintext):
    text = re.sub(r'[^A-Za-z]', '', plaintext).upper().replace("J", "I")
    prepared = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else "X"
        if a == b:  # avoid duplicates in pair
            prepared += a + "X"
            i += 1
        else:
            prepared += a + b
            i += 2
    if len(prepared) % 2 != 0:
        prepared += "X"
    return prepared

# Playfair encryption
def playfair_encrypt(plaintext, key):
    matrix = generate_matrix(key)
    plaintext = prepare_text(plaintext)
    ciphertext = ""

    for i in range(0, len(plaintext), 2):
        a, b = plaintext[i], plaintext[i+1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)

        if row_a == row_b:  # Same row → shift right
            ciphertext += matrix[row_a][(col_a + 1) % 5]
            ciphertext += matrix[row_b][(col_b + 1) % 5]
        elif col_a == col_b:  # Same column → shift down
            ciphertext += matrix[(row_a + 1) % 5][col_a]
            ciphertext += matrix[(row_b + 1) % 5][col_b]
        else:  # Rectangle swap
            ciphertext += matrix[row_a][col_b]
            ciphertext += matrix[row_b][col_a]

    return ciphertext

# Streamlit UI
st.title("🔐 IEDC Cipher Encryption Tool")

# safer: let user enter key instead of st.secrets
key = st.secrets["key"]
plaintext = st.text_area("Enter Plaintext:")

if st.button("Encrypt"):
    if key and plaintext:
        encrypted_text = playfair_encrypt(plaintext, key)
        st.success(f"✅ Encrypted Text: {encrypted_text}")
    else:
        st.warning("Please enter both key and plaintext.")
