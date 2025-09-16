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

# Preprocess ciphertext
def prepare_text(ciphertext):
    text = re.sub(r'[^A-Za-z]', '', ciphertext).upper().replace("J", "I")
    prepared = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else "x"
        if a == b:  # avoid duplicates in a pair
            prepared += a + "x"
            i += 1
        else:
            prepared += a + b
            i += 2
    if len(prepared) % 2 != 0:  # padding
        prepared += "x"
    return prepared

# Playfair decryption
def playfair_decrypt(ciphertext, key):
    matrix = generate_matrix(key)
    prepared = prepare_text(ciphertext)
    ciphertext = ""

    for i in range(0, len(prepared), 2):
        a, b = prepared[i], prepared[i+1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)

        if row_a == row_b:  # Same row
            ciphertext += matrix[row_a][(col_a + 1) % 5]
            ciphertext += matrix[row_b][(col_b + 1) % 5]
        elif col_a == col_b:  # Same column
            ciphertext += matrix[(row_a + 1) % 5][col_a]
            ciphertext += matrix[(row_b + 1) % 5][col_b]
        else:  # Rectangle
            ciphertext += matrix[row_a][col_b]
            ciphertext += matrix[row_b][col_a]

    return ciphertext

# Streamlit UI
st.title("🔐 IEDC Cipher Decryption Tool")

key = st.secrets["key"]
ciphertext = st.text_area("Enter Ciphertext:")

if st.button("Decrypt"):
    if key and ciphertext:
        decrypted_text = playfair_decrypt(ciphertext, key)
        #st.success(f"✅ Decrypted Text: {decrypted_text}")
        st.success(f"Your Team name is :{decrypted_text}")
        st.balloons()
    else:
        st.warning("Please enter both key and ciphertext.")
