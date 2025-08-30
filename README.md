# Token Extraction and Decryption Script

This script extracts and decrypts tokens from various applications and browsers by parsing their local storage files. It uses regular expressions to find tokens and decrypts them using AES encryption with keys extracted from application data files.

## **Disclaimer**
This project is provided **for educational and demonstrational purposes only**.  
The author is **not responsible for any loss, damage, or misuse** resulting from the use of this program.  
Use entirely at your own risk.

## **Requirements**
- Python 3.x
- pycryptodome library for AES decryption
- pywin32 library for Windows cryptography

    ### You can install the required libraries using pip:
    ```shell
    pip install pycryptodome pywin32
    ```

## **Files Used**
- Local State file from browser and application directories for decrypting keys.
- LevelDB files from local storage directories for extracting tokens.

## **How It Works**
1. Define Paths: The script defines paths to various applications and browsers where token data might be stored.
2. Extract Key: It reads the Local State file to obtain the encryption key used for decrypting tokens.
3. Parse Files: It searches through LevelDB files and extracts potential tokens using regex patterns.
4. Decrypt Tokens: Extracted tokens are decrypted using AES encryption with the obtained key.
5. Match Tokens: Tokens are matched against predefined regex patterns to identify valid tokens.
6. Output: The script prints out the extracted and decrypted tokens.

## **Script Details**
### Importing Libraries
```shell
from base64 import b64decode
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
from os import listdir
from json import loads
from re import findall
import re
import os
```

## **Key Functions**
- decrypt(buff, master_key): Decrypts a given buffer using AES encryption.
- get_token(): Extracts and processes tokens from various application and browser data files.

## **Regular Expressions**
- regex0: Matches standard token formats.
- regex1: Matches MFA token formats.
- regex2: Matches extended token formats.

## **Usage**
1. Clone the repository or download the script file.
2. Ensure the required libraries are installed.
3. Run the script:
```shell
python main.py
```

## **Notes**
- Ensure you have the necessary permissions to access and read the local storage files.
- The script is designed for educational and research purposes. Use it responsibly and ethically.

## **License**
This script is provided for educational purposes and may be used according to its license agreement. Ensure compliance with all relevant laws and regulations. [LICENSE](LICENSE).