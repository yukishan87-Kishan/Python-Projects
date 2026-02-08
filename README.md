# Clean Tkinter Login UI

A lightweight, modern login application built with Python's Tkinter library. No external packages required.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Workflow](#workflow)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [File Formats](#file-formats)
- [Important Notes](#important-notes)

## 🎯 Overview

This project provides a clean, modern-looking authentication interface using Tkinter. It demonstrates best practices in UI/UX design with a simple yet functional login and account creation system.

## ✨ Features

- **Clean UI Design**: Modern, intuitive interface with proper styling
- **User Authentication**: Sign in with stored credentials
- **Account Creation**: Create new user accounts
- **No External Dependencies**: Built entirely with Python's standard Tkinter library
- **File-Based Storage**: Simple credential storage in `loginData.txt`

## 🔄 Workflow

### Sign In Flow
1. User enters username and password on login screen
2. Application verifies credentials against `loginData.txt`
3. Supports multiple credential formats (hashed or plain text)
4. On successful authentication, user gains access; otherwise, error message displayed

### Account Creation Flow
1. User clicks "Create Account" button
2. User enters desired username and password
3. Password is hashed using SHA256 algorithm
4. New entry is appended to `loginData.txt` in format: `username:sha256(password_hash)`
5. User can proceed to sign in with new credentials

## 📁 Project Structure

```
PythonProject/
├── Project1.py           # Main application entry point
├── loginData.txt         # Credential storage file
├── README.md            # Project documentation
└── __pycache__/         # Python cache directory
```

## 🚀 Installation

1. Ensure Python is installed on your system
2. No additional packages needed - uses only standard library

## 💻 Usage

Run the application using PowerShell or command prompt:

```powershell
python Project1.py
```

Or alternatively:

```cmd
python Project1.py
```

## 📝 File Formats

### loginData.txt

Stores user credentials in one of the following formats:

- **Hashed Format**: `username:sha256_password_hash`
- **Plain Text Format**: `username:rawpassword`
- **Separated Format**: `username,password` or `username password`

Example:
```
john:5e884898da28047151d0e56f8dc62927
alice:securepassword123
bob:a1b2c3d4e5f6g7h8i9j0
```

## ⚠️ Important Notes

- **Demo Purpose**: This is a simple demonstration project focusing on UI/UX layout and design
- **Not for Production**: Do not use in production environments
- **Security Considerations**: 
  - Replace file-based storage with a secure database (PostgreSQL, MongoDB, etc.)
  - Implement proper password hashing (bcrypt, Argon2)
  - Use environment variables for configuration
  - Implement proper authentication tokens/sessions
  - Add rate limiting to prevent brute force attacks

## 🛠️ Future Improvements

- Database integration
- Enhanced security measures
- Password strength validation
- Forgot password functionality
- User profile management
- Remember me functionality
