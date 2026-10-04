# Employee Management System

A desktop application for managing employee records, built with Python,
CustomTkinter (GUI), and MySQL (database).

## Features
- Secure login screen
- Add / update / delete employee records
- Search by Id, Name, Phone, Role, Gender, or Salary
- Filter by exact Employee ID
- Paginated record view (10 per page)
- Upload and view an employee's photo
- Export all records to Excel (.xlsx)
- Input validation (required fields, 10-digit phone, numeric salary)

## Tech Stack
| Layer       | Technology |
|-------------|------------|
| GUI         | CustomTkinter (built on Tkinter) |
| Database    | MySQL (via PyMySQL) |
| Image handling | Pillow |
| Excel export | pandas + openpyxl |
| Packaging   | PyInstaller |

## Project Structure
```
EmployeeManagementSystem/
├── login.py          # Login window (entry point)
├── ems.py             # Main application window
├── database.py        # Database connection and queries
├── config.ini          # DB credentials (edit this, not the .py files)
├── requirements.txt
├── login.spec          # PyInstaller build config
├── cover_pic.jpeg       # Login screen image (placeholder included)
├── bg.jpeg               # Header banner image (placeholder included)
└── employee_images/      # Created automatically when you upload a photo
```

## Setup (Development)

1. **Install Python 3.9+** from python.org (check "Add to PATH" on Windows).

2. **Install MySQL** (MySQL Community Server, or XAMPP/WAMP) and make sure
   the server is running.

3. **Edit `config.ini`** with your MySQL credentials:
   ```ini
   [database]
   host = localhost
   user = root
   password = your_password_here
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **(Optional) Replace the placeholder images** — `cover_pic.jpeg` and
   `bg.jpeg` are auto-generated placeholders. Swap in your own images
   (keep the same filenames) for a polished look.

6. **Run the app:**
   ```bash
   python login.py
   ```
   Login with:
   - Username: `mounish`
   - Password: `30062006`

   (To change these, edit the `login()` function in `login.py`.)

## Building a Standalone .exe (Windows)

Once the app runs correctly with `python login.py`:

```bash
pip install pyinstaller
pyinstaller login.spec
```

The executable will be in `dist/EmployeeManagementSystem.exe`. It still
needs a MySQL server reachable at the host/credentials in `config.ini`,
so ship `config.ini` alongside the .exe (or instruct the user to edit it).

> Note: PyInstaller builds a Windows `.exe` only when run **on Windows**.
> Build it on your Windows laptop, not on another OS.

## Known Limitations / Possible Next Steps
- Login credentials are hardcoded in `login.py` (fine for a student
  project; for production, hash and store them properly).
- No password hashing / no multi-user accounts — single shared login.
- MySQL must be running locally; there's no cloud/remote DB setup here.
- Employee photos are stored as local files (`employee_images/`), not in
  the database — the `Image_Path` DB column is currently unused.

## Troubleshooting
| Problem | Fix |
|---|---|
| "Could not connect to MySQL" | Make sure MySQL server is running and `config.ini` has the right password |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| App window doesn't open / crashes instantly | Run from a terminal (not double-click) so you can see the error message |
| Images look like placeholder boxes | Replace `cover_pic.jpeg` and `bg.jpeg` with your own images |
