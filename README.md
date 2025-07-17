# PythonClI-Password-Manager-
Password Manager Documentation
Overview
This Password Manager is a secure command-line application that allows users to store, retrieve, and manage their passwords for different services (e.g., Gmail, Facebook, etc.). It uses Fernet encryption (a symmetric encryption method from the cryptography library) to securely store passwords in an encrypted file.
Key Features
✅ Secure Master Password Protection – Uses SHA-256 hashing for master password storage.
✅ Encrypted Password Storage – All passwords are encrypted before saving to a file.
✅ Password Recovery – Allows resetting the master password if forgotten.
✅ User-Friendly CLI – Simple menu-driven interface for easy interaction.
✅ Multiple Accounts per Service – Supports storing multiple usernames per service (e.g., multiple Gmail accounts).
________________________________________
How It Works
1. Initial Setup
When run for the first time, the program prompts the user to set a master password.
The master password is hashed (SHA-256) and stored in master_pw.hash.
An encryption key (key.key) is generated to encrypt/decrypt stored passwords.
2. Authentication
On subsequent runs, the user must enter the correct master password to access stored passwords.
If the password is forgotten, the user can type reset to set a new master password.
3. Password Management
Add Passwords – Store usernames and passwords for different services.
Retrieve Passwords – View stored passwords by service and username.
List Services – See all services with stored passwords.
Delete Passwords – Remove stored entries.
Change Master Password – Securely update the master password.
________________________________________


Technical Details
Files Used

File	Purpose
passwords.json	Encrypted storage of all passwords.
key.key	Fernet encryption key for securing passwords.
master_pw.hash	SHA-256 hash of the master password (not the actual password).
Encryption & Security

Fernet (AES-128)	(AES-128) – Used to encrypt/decrypt stored passwords.

SHA-256 Hashing	SHA-256 Hashing
Secure Input Handling	Uses getpass() to hide password input

________________________________________
Usage Guide
1. Starting the Program
Run the script:
bash
python password_manager.py
2. First-Time Setup
You will be prompted to set a master password.
This password will be required to access stored passwords later.
3. Main Menu Options
text
=== Password Manager ===

Options:
1. Add new password
2. Retrieve password
3. List all services
4. Delete password entry
5. Change master password
6. Exit
1. Add New Password
Enter the service name (e.g., "Gmail").
Enter the username/email.
Enter the password (hidden input).
2. Retrieve Password
Enter the service name.
Optionally, enter a username to get a specific password.
If no username is given, all accounts for that service are shown.
3. List All Services
Shows all services with stored passwords.
4. Delete Password Entry
Enter the service name and username to delete an entry.
5. Change Master Password
Requires the current master password for verification.
Prompts for a new master password (must be confirmed).
6. Exit
Safely closes the program.
________________________________________
Security Considerations
🔒 Never stores plaintext passwords – All passwords are encrypted.
🔒 Master password is hashed – Prevents exposure even if the hash file is compromised.
⚠ No cloud backup – Passwords are stored locally; users should ensure safe storage of passwords.json and key.key.
________________________________________
Future Improvements
1.	Two-Factor Authentication (2FA) for master password access.
2.	Automatic backups of encrypted password files.
3.	Password strength checker when setting new passwords.
________________________________________
Conclusion
This Password Manager provides a secure and easy-to-use way to store and manage passwords locally. It ensures strong encryption and master password protection, making it a reliable tool for personal password management.

