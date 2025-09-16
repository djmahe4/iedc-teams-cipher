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

# Clean ciphertext (basic preprocessing only)
def clean_text(ciphertext):
    return re.sub(r'[^A-Za-z]', '', ciphertext).upper().replace("J", "I")

# Playfair decryption
def playfair_decrypt(ciphertext, key):
    matrix = generate_matrix(key)
    text = clean_text(ciphertext)

    if len(text) % 2 != 0:
        text += "X"  # padding if needed

    plaintext = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)

        if row_a == row_b:  # Same row → shift left
            plaintext += matrix[row_a][(col_a - 1) % 5]
            plaintext += matrix[row_b][(col_b - 1) % 5]
        elif col_a == col_b:  # Same column → shift up
            plaintext += matrix[(row_a - 1) % 5][col_a]
            plaintext += matrix[(row_b - 1) % 5][col_b]
        else:  # Rectangle swap
            plaintext += matrix[row_a][col_b]
            plaintext += matrix[row_b][col_a]

    return plaintext

# Streamlit UI
st.title("🔐 IEDC Cipher Decryption Tool")

key = st.secrets["key"]
ciphertext = st.text_area("Enter Ciphertext:")

if st.button("Decrypt"):
    if key and ciphertext:
        decrypted_text = playfair_decrypt(ciphertext, key)
        st.success(f"✅ Your Team name is : {decrypted_text}")
        st.balloons()
    else:
        st.warning("Please enter both key and ciphertext.")
