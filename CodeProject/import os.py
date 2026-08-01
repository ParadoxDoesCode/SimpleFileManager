import os
import time
import sys
import random
import string
import base64
import hashlib
from datetime import datetime

# Global Configuration
folder_path = r'D:\VeryCoolFolder'
merged_file_name = 'mergedtext.txt'

def ensure_folder_exists():
    """Checks for the D: drive folder and creates it if missing.
    Falls back to the user's Documents folder on C: if D: does not exist."""
    global folder_path
    d_drive_root = 'D:\\'

    if os.path.exists(d_drive_root):
        target_path = folder_path
    else:
        documents_root = os.path.join(os.path.expanduser('~'), 'Documents')
        target_path = os.path.join(documents_root, 'VeryCoolFolder')
        folder_path = target_path
        print(f"[System] D drive not found. Using Documents folder: {folder_path}")

    if not os.path.exists(target_path):
        try:
            os.makedirs(target_path)
            print(f"[System] Created folder: {target_path}")
        except OSError:
            print(f"[Error] Could not create folder: {target_path}")
            sys.exit()

def rename_target_folder():
    """Renames the current folder and updates the path variable."""
    global folder_path
    print(f"\n--- Rename Folder (Current: {folder_path}) ---")
    new_name = input("Enter the new folder name: ").strip()
    
    if not new_name:
        print("--> Error: Folder name cannot be empty.")
        return

    current_drive = os.path.splitdrive(folder_path)[0].upper()
    if current_drive == 'D:' and os.path.exists('D:\\'):
        new_path = os.path.join(r'D:', new_name)
    else:
        base_folder = os.path.dirname(folder_path)
        new_path = os.path.join(base_folder, new_name)

    try:
        if os.path.exists(new_path):
            print(f"--> Error: A folder named '{new_name}' already exists at the target location.")
        else:
            os.rename(folder_path, new_path)
            folder_path = new_path
            print(f"--> Success! Folder is now: {folder_path}")
    except Exception as e:
        print(f"--> Error renaming folder: {e}")

def list_files():
    """Displays all .txt files in the directory."""
    files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    if not files:
        print("--> The folder is currently empty.")
    else:
        print(f"\n--- Files in {folder_path} ---")
        for index, filename in enumerate(files, start=1):
            file_path = os.path.join(folder_path, filename)
            size = os.path.getsize(file_path)
            print(f"{index}. {filename} ({size} bytes)")
        print(f"Total files: {len(files)}")

def hash_text():
    """Asks for text and saves its MD5 hash to a file."""
    text_to_hash = input("Enter the text to hash (MD5): ")
    hash_object = hashlib.md5(text_to_hash.encode())
    md5_hash = hash_object.hexdigest()

    timestamp = datetime.now().strftime("%H%M%S")
    filename = f"hash_{timestamp}.txt"
    full_path = os.path.join(folder_path, filename)

    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(md5_hash)
    print(f"--> MD5 Hash ({md5_hash}) saved to: {filename}")

def hash_password_file():
    """Lists password files, lets user choose one, hashes it, and saves both."""
    pass_files = [f for f in os.listdir(folder_path) if "password" in f.lower() and f.endswith('.txt')]
    
    if not pass_files:
        print("--> No 'password' files found.")
        return

    print("\n--- Select a Password File ---")
    for i, filename in enumerate(pass_files, start=1):
        print(f"{i}. {filename}")
    
    try:
        choice = int(input("\nEnter the number of the file to hash: "))
        if 1 <= choice <= len(pass_files):
            selected_file = pass_files[choice - 1]
            full_path = os.path.join(folder_path, selected_file)
            
            with open(full_path, 'r', encoding='utf-8') as f:
                raw_password = f.read().strip()
            
            hash_obj = hashlib.md5(raw_password.encode())
            hashed_password = hash_obj.hexdigest()
            
            timestamp = datetime.now().strftime("%H%M%S")
            hp_filename = f"hashpass_{timestamp}.txt"
            hp_path = os.path.join(folder_path, hp_filename)
            
            with open(hp_path, 'w', encoding='utf-8') as f:
                f.write(f"Original Password: {raw_password}\nMD5 Hash: {hashed_password}")
            
            print(f"--> Success! Created {hp_filename}")
        else:
            print("--> Invalid selection.")
    except ValueError:
        print("--> Please enter a valid number.")

def clear_folder():
    """Deletes all .txt files in the folder."""
    files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    if not files:
        print("--> Folder is already empty.")
        return

    confirm = input(f"Delete {len(files)} files? (y/n): ").lower().strip()
    if confirm == 'y':
        for f in files:
            os.remove(os.path.join(folder_path, f))
        print("--> All text files deleted.")
    else:
        print("--> Action cancelled.")

def generate_random_password():
    """Generates a random 8-16 char password and saves it."""
    length = random.randint(8, 16)
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    
    timestamp = datetime.now().strftime("%H%M%S")
    filename = f"password_{timestamp}.txt"
    full_path = os.path.join(folder_path, filename)

    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(password)
    print(f"--> Random password saved to: {filename}")

def encode_base64():
    """Asks for text, encodes it to Base64, and saves to a file."""
    text_to_encode = input("Enter text for Base64: ")
    base64_string = base64.b64encode(text_to_encode.encode()).decode()

    timestamp = datetime.now().strftime("%H%M%S")
    filename = f"base64_{timestamp}.txt"
    full_path = os.path.join(folder_path, filename)

    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(base64_string)
    print(f"--> Base64 saved to: {filename}")

def merge_files():
    """Combines all existing .txt files into one master file."""
    files = [f for f in os.listdir(folder_path) if f.endswith('.txt') and f != merged_file_name]
    if not files:
        print("--> No .txt files found to merge.")
        return

    show_progress_bar()
    full_merge_path = os.path.join(folder_path, merged_file_name)
    with open(full_merge_path, 'w', encoding='utf-8') as outfile:
        for filename in files:
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as infile:
                outfile.write(f"--- Source: {filename} ---\n{infile.read()}\n\n")
    print(f"--> Merged into '{merged_file_name}'")

def create_file(content):
    """Creates a new text file."""
    custom_name = input("File name (leave blank for timestamp): ").strip()
    filename = (custom_name if custom_name else f"note_{datetime.now().strftime('%H%M%S')}") + ".txt"
    full_path = os.path.join(folder_path, filename)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"--> Saved as: {filename}")

def show_goodbye():
    """Displays ASCII GOODBYE message."""
    print(r"""
  GGGG   OOOOO   OOOOO  DDDD   BBBB   Y   Y  EEEEE
 G       O   O   O   O  D   D  B   B   Y Y   E
 G  GG   O   O   O   O  D   D  BBBB     Y    EEEE
 G   G   O   O   O   O  D   D  B   B    Y    E
  GGGG   OOOOO   OOOOO  DDDD   BBBB     Y    EEEEE
    """)
    print("      Closing application. Have a great day! :333")

# --- Main Program Loop ---
ensure_folder_exists()
print("==========================================")
print("         PARADOX'S RANDOM TOOL            ")
print("==========================================")
print("Commands: 'list' | 'merge' | 'random' | 'hashpass' | 'base 64' | 'hash'")
print("          'rename folder' | 'clear' | 'exit'")
print("Otherwise, just type your text to save it.")

while True:
    user_input = input("\nInput: ").strip()
    cmd = user_input.lower()

    if cmd == 'exit':
        show_goodbye()
        break
    elif cmd == 'rename folder':
        rename_target_folder()
    elif cmd == 'merge':
        merge_files()
    elif cmd == 'list':
        list_files()
    elif cmd == 'random':
        generate_random_password()
    elif cmd == 'hashpass':
        hash_password_file()
    elif cmd == 'base 64':
        encode_base64()
    elif cmd == 'hash':
        hash_text()
    elif cmd == 'clear':
        clear_folder()
    elif user_input == "":
        continue
    else:
        create_file(user_input)