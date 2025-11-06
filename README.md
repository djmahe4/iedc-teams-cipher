# IEDC Teams Cipher

Web apps for encrypting and decrypting IEDC Team names using the Playfair cipher algorithm.

**[Decryption App](https://iedc-teams-cipher.streamlit.app/)** <br>
**[Encryption App](https://iedc-teams-test.streamlit.app/)** <br>

## How It Works

This project implements the **Playfair cipher**, a manual symmetric encryption technique that encrypts pairs of letters (digraphs) using a 5×5 matrix of letters constructed from a keyword.

### Playfair Cipher Process

1. **Key Matrix Generation**: A 5×5 matrix is created from the encryption key, combining the key with the remaining letters of the alphabet (I and J are treated as the same letter).

2. **Encryption**:
   - Text is preprocessed: non-alphabetic characters removed, J replaced with I
   - Letters are paired (adding X between duplicate letters in a pair)
   - Each pair is encrypted based on their position in the matrix:
     - Same row → shift right
     - Same column → shift down
     - Different row/column → rectangle swap

3. **Decryption**:
   - Reverse process: shift left for same row, shift up for same column
   - Rectangle swap remains the same

## Local Deployment

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/djmahe4/iedc-teams-cipher.git
   cd iedc-teams-cipher
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the encryption key**:
   
   Create a `.streamlit` directory in the project root and add a `secrets.toml` file:
   
   ```bash
   mkdir .streamlit
   ```
   
   Create `.streamlit/secrets.toml` with the following content:
   ```toml
   key = "YOUR_SECRET_KEY_HERE"
   ```
   
   Replace `YOUR_SECRET_KEY_HERE` with your desired encryption key (e.g., "IEDCMEC").
   
   **Important**: The `.streamlit/secrets.toml` file should never be committed to version control as it contains sensitive information. Ensure it's listed in `.gitignore`.

4. **Run the applications**:
   
   For decryption:
   ```bash
   streamlit run decrypt.py
   ```
   
   For encryption:
   ```bash
   streamlit run encrypt.py
   ```

## Usage

### Encryption
1. Run the encryption app
2. Enter your plaintext team name
3. Click "Encrypt" to get the encrypted text

### Decryption
1. Run the decryption app
2. Enter the encrypted ciphertext
3. Click "Decrypt" to reveal the team name

## Project Structure

```
iedc-teams-cipher/
├── encrypt.py          # Streamlit app for encryption
├── decrypt.py          # Streamlit app for decryption
├── requirements.txt    # Python dependencies
├── .streamlit/         # Streamlit configuration (local only)
│   └── secrets.toml   # Secret key storage (not in repo)
└── README.md          # This file
```

## Security Notes

- The encryption key is stored in `st.secrets["key"]` which reads from `.streamlit/secrets.toml` during local deployment
- For production deployment on Streamlit Cloud, configure secrets through the Streamlit Cloud dashboard
- Never commit the `secrets.toml` file to version control
