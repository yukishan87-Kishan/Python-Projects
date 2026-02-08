# Clean Tkinter UI sample

This small example provides a clean, modern-looking login UI built with Tkinter (no external packages required).

Run:
```powershell
python app_gui.py
```

Behavior:
- Sign in with credentials stored in `loginData.txt` (format: `username:password_hash` or `username:rawpassword` or comma/space-separated)
- Create account will append a new `username:sha256(password)` line to `loginData.txt`.

Notes:
- This is a simple demo focusing on layout and style. For production use, replace storage with a secure database and proper password handling.
