*Here include a short description of the project*
# Project for module CST1510 

 # Week 7: Secure Authentication System
Student Name: Sean-Perez Mukudzeyi Mudhara
Student ID: M01059264
Course: CST1510 -CW2 - Multi-Domain Intelligence Platform
## Project Description
A command-line authentication system implementing secure password hashing
This system allows users to register accounts and log in with proper pass
## Features
- Secure password hashing using bcrypt with automatic salt generation
- User registration with duplicate username prevention
- User login with password verification
- Input validation for usernames and passwords
- File-based user data persistence
## Technical Implementation
- Hashing Algorithm: bcrypt with automatic salting
- Data Storage: Plain text file (`users.txt`) with comma-separated values
- Password Security: One-way hashing, no plaintext storage
- Validation: Username (3-20 alphanumeric characters), Password (6-50 characters; containing at least 1 capital letter, 1 lower case letter, and 1 number)

To run enter streamlit run Home.py