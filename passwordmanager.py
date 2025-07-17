import os
import json
from cryptography.fernet import Fernet
from getpass import getpass

class PasswordManager:
    def __init__(self, master_password, data_file='passwords.json', key_file='key.key'):
        self.data_file = data_file
        self.key_file = key_file
        self.master_password = master_password
        
        # Load or create encryption key
        if os.path.exists(self.key_file):
            self._load_key()
        else:
            self._generate_key()
        
        # Load or initialize password database
        if os.path.exists(self.data_file):
            self._load_data()
        else:
            self.passwords = {}
    
    def _generate_key(self):
        """Generate a new encryption key and save it to file"""
        self.key = Fernet.generate_key()
        with open(self.key_file, 'wb') as f:
            f.write(self.key)
    
    def _load_key(self):
        """Load the encryption key from file"""
        with open(self.key_file, 'rb') as f:
            self.key = f.read()
    
    def _load_data(self):
        """Load and decrypt the password database"""
        with open(self.data_file, 'rb') as f:
            encrypted_data = f.read()
        
        fernet = Fernet(self.key)
        decrypted_data = fernet.decrypt(encrypted_data)
        self.passwords = json.loads(decrypted_data.decode())
    
    def _save_data(self):
        """Encrypt and save the password database"""
        fernet = Fernet(self.key)
        encrypted_data = fernet.encrypt(json.dumps(self.passwords).encode())
        
        with open(self.data_file, 'wb') as f:
            f.write(encrypted_data)
    
    def add_password(self, service, username, password):
        """Add a new password entry"""
        if service not in self.passwords:
            self.passwords[service] = []
        
        # Check if username already exists for this service
        for entry in self.passwords[service]:
            if entry['username'] == username:
                print(f"Username '{username}' already exists for {service}. Updating password.")
                entry['password'] = password
                break
        else:
            self.passwords[service].append({
                'username': username,
                'password': password
            })
        
        self._save_data()
        print(f"Password for {service} added/updated successfully.")
    
    def get_password(self, service, username=None):
        """Retrieve a password"""
        if service not in self.passwords:
            print(f"No entries found for {service}.")
            return None
        
        if username:
            for entry in self.passwords[service]:
                if entry['username'] == username:
                    return entry['password']
            print(f"No entry found for username '{username}' in {service}.")
            return None
        else:
            # Return all entries for the service
            return self.passwords[service]
    
    def list_services(self):
        """List all services with stored passwords"""
        if not self.passwords:
            print("No passwords stored yet.")
            return
        
        print("\nStored services:")
        for service in self.passwords.keys():
            print(f"- {service} ({len(self.passwords[service])} accounts)")
    
    def delete_entry(self, service, username):
        """Delete a password entry"""
        if service in self.passwords:
            for i, entry in enumerate(self.passwords[service]):
                if entry['username'] == username:
                    del self.passwords[service][i]
                    # Remove service if no more entries
                    if not self.passwords[service]:
                        del self.passwords[service]
                    self._save_data()
                    print(f"Entry for {username}@{service} deleted successfully.")
                    return
            
            print(f"No entry found for username '{username}' in {service}.")
        else:
            print(f"No entries found for {service}.")

def main():
    print("=== Password Manager ===")
    
    # Set or verify master password
    if os.path.exists('master_pw.key'):
        with open('master_pw.key', 'rb') as f:
            stored_master = f.read()
        entered_master = getpass("Enter master password: ").encode()
        if entered_master != stored_master:
            print("Incorrect master password!")
            return
        master_password = stored_master
    else:
        master_password = getpass("Set master password: ").encode()
        confirm = getpass("Confirm master password: ").encode()
        if master_password != confirm:
            print("Passwords don't match!")
            return
        with open('master_pw.key', 'wb') as f:
            f.write(master_password)
        print("Master password set successfully.")
    
    # Initialize password manager
    pm = PasswordManager(master_password)
    
    while True:
        print("\nOptions:")
        print("1. Add new password")
        print("2. Retrieve password")
        print("3. List all services")
        print("4. Delete password entry")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            service = input("Enter service name (e.g., 'Gmail'): ")
            username = input("Enter username/email: ")
            password = getpass("Enter password: ")
            pm.add_password(service, username, password)
        
        elif choice == '2':
            service = input("Enter service name: ")
            username = input("Enter username (leave blank to see all): ").strip() or None
            result = pm.get_password(service, username)
            
            if result:
                if isinstance(result, list):
                    print(f"\nAccounts for {service}:")
                    for entry in result:
                        print(f"Username: {entry['username']}")
                        print(f"Password: {entry['password']}\n")
                else:
                    print(f"\nPassword for {username}@{service}: {result}\n")
        
        elif choice == '3':
            pm.list_services()
        
        elif choice == '4':
            service = input("Enter service name: ")
            username = input("Enter username to delete: ")
            pm.delete_entry(service, username)
        
        elif choice == '5':
            print("Exiting Password Manager. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
