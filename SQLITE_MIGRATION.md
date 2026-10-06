# SQLite Migration Guide

## Overview
This project has been successfully migrated from **MySQL (XAMPP)** to **SQLite**. All database operations have been updated to use SQLite instead of Flask-MySQLdb.

## What Changed

### 1. Database Configuration
- **Before**: Used `Flask-MySQLdb` with XAMPP localhost connection
- **After**: Uses Python's built-in `sqlite3` module with a local `.db` file

### 2. Files Modified
- `app.py` - Updated all database connections and queries to use SQLite

### 3. Files Created
- `init_db.py` - Database initialization script (run this once to create the database)
- `mental_health_app.db` - The SQLite database file (auto-generated)

## Key Differences

### Connection Method
```python
# OLD (MySQL)
cursor = mysql.connection.cursor()
cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))

# NEW (SQLite)
conn = get_db()
cursor = conn.cursor()
cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
conn.close()
```

### Parameter Placeholders
- MySQL used: `%s`
- SQLite uses: `?`

### Timestamp Handling
SQLite returns timestamps as strings, so we added datetime parsing:
```python
timestamp = row[0]
if isinstance(timestamp, str):
    date_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    date_str = date_obj.strftime("%b %d, %Y")
else:
    date_str = timestamp.strftime("%b %d, %Y")
```

## Installation & Setup

### 1. Install Required Package
```bash
pip install flask
# sqlite3 is built-in, no additional installation needed
```

### 2. Initialize Database
```bash
python init_db.py
```

This creates `mental_health_app.db` with all tables and seed data from your original SQL file.

### 3. Run the Application
```bash
python app.py
```

## Database File Location
- `mental_health_app.db` is located in the same directory as `app.py`
- The database contains all tables: `users`, `diary_entries`, `doctor_assigned`, `game_scores`, `messages`, `questionnaire_results`, `questions`

## Advantages of SQLite

✅ **No Server Required**: No need to run XAMPP/MySQL server  
✅ **Single File**: Easy to backup, copy, or distribute  
✅ **Lightweight**: Minimal memory footprint  
✅ **Built-in**: Python has SQLite support by default  
✅ **Perfect for Development**: Great for small to medium projects  

## Test Credentials

The database comes with sample data:

| Role | Email | Password |
|------|-------|----------|
| Student | nandini@gmail.com | abcde |
| Student | jyothsna@gmail.com | 1 |
| Counsellor | remya1@gmail.com | remya123 |
| Admin | admin@gmail.com | admin123 |

## Troubleshooting

### Database File Not Found
- Run `python init_db.py` again to recreate it

### Import Errors
- Make sure you have Flask installed: `pip install flask`

### Queries Not Working
- Check that all SQL queries use `?` instead of `%s`
- Ensure you call `conn.close()` after using the connection

## No Longer Needed
You can remove or keep these for reference:
- XAMPP MySQL server (not required)
- `Flask-MySQLdb` package (not imported anymore)

## Notes
- The `mental_health_app.sql` file is kept for reference but is no longer used
- All data operations now go directly to `mental_health_app.db`
- The app is backward compatible with your existing frontend (HTML templates)
