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

# Playfair encryption
def playfair_encrypt(plaintext, key):
    matrix = generate_matrix(key)
    plaintext = re.sub(r'[^A-Za-z]', '', plaintext).upper().replace("J", "I")

    if len(plaintext) % 2 != 0:
        plaintext += "X"  # padding if needed

    plaintext = ""
    for i in range(0, len(plaintext), 2):
        a, b = plaintext[i], plaintext[i+1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)

        if row_a == row_b:  # Same row
            plaintext += matrix[row_a][(col_a - 1) % 5]
            plaintext += matrix[row_b][(col_b - 1) % 5]
        elif col_a == col_b:  # Same column
            plaintext += matrix[(row_a - 1) % 5][col_a]
            plaintext += matrix[(row_b - 1) % 5][col_b]
        else:  # Rectangle
            plaintext += matrix[row_a][col_b]
            plaintext += matrix[row_b][col_a]

    return plaintext

# Streamlit UI
st.title("🔐 IEDC Cipher Encryption Tool")

key = st.secrets["key"]
plaintext = st.text_area("Enter Plaintext:")

if st.button("Encrypt"):
    if key and plaintext:
        encrypted_text = playfair_encrypt(plaintext, key)
        st.success(f"✅ Encrypted Text: {encrypted_text}")
    else:
        st.warning("Please enter both key and plaintext.")
