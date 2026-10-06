import sqlite3
import os

# Create SQLite database
DB_PATH = 'mental_health_app.db'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(100),
    role VARCHAR(30) NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS diary_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title VARCHAR(255),
    content TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS doctor_assigned (
    student_email VARCHAR(255) PRIMARY KEY,
    student_name VARCHAR(255),
    doctor_name VARCHAR(255),
    doctor_email VARCHAR(255)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS game_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    game_name VARCHAR(50),
    score INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    time VARCHAR(20),
    moves INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    receiver_id INTEGER,
    message TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS questionnaire_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    score INTEGER,
    percentage INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    option_a VARCHAR(255),
    score_a INTEGER,
    option_b VARCHAR(255),
    score_b INTEGER,
    option_c VARCHAR(255),
    score_c INTEGER,
    option_d VARCHAR(255),
    score_d INTEGER,
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)
''')

# Insert seed data
cursor.execute('''
INSERT OR IGNORE INTO users (id, username, email, password, role) VALUES
(2, 'Nandini', 'nandini@gmail.com', 'abcde', 'Student'),
(6, 'Dr Remya', 'remya1@gmail.com', 'remya123', 'Counsellor'),
(12, 'Jyothsna', 'jyothsna@gmail.com', '1', 'Student'),
(15, 'Admin', 'admin@gmail.com', 'admin123', 'Admin')
''')

cursor.execute('''
INSERT OR IGNORE INTO questions (id, question, option_a, score_a, option_b, score_b, option_c, score_c, option_d, score_d) VALUES
(1, 'How often do you feel stressed?', 'Never', 3, 'Sometimes', 2, 'Often', 1, 'Always', 0),
(2, 'How well do you sleep?', 'Very well', 3, 'Okay', 2, 'Poorly', 1, 'Very poorly', 0),
(3, 'How often do you feel happy?', 'Always', 3, 'Often', 2, 'Rarely', 1, 'Never', 0),
(4, 'Do you feel motivated daily?', 'Very', 3, 'Somewhat', 2, 'Low', 1, 'None', 0),
(5, 'How often do you feel anxious?', 'Never', 3, 'Sometimes', 2, 'Often', 1, 'Always', 0),
(6, 'How well do you manage emotions?', 'Very well', 3, 'Okay', 2, 'Poorly', 1, 'Very poorly', 0),
(7, 'Do you feel connected to others?', 'Very', 3, 'Somewhat', 2, 'Not much', 1, 'Not at all', 0),
(8, 'How often do you feel tired?', 'Never', 3, 'Sometimes', 2, 'Often', 1, 'Always', 0),
(9, 'How do you handle challenges?', 'Very well', 3, 'Okay', 2, 'Struggle', 1, 'Cannot handle', 0),
(10, 'How satisfied are you with life?', 'Very', 3, 'Somewhat', 2, 'Not much', 1, 'Not at all', 0),
(11, 'How often do you feel lonely?', 'Never', 3, 'Sometimes', 2, 'Often', 1, 'Always', 0),
(12, 'Do you enjoy activities?', 'Always', 3, 'Often', 2, 'Rarely', 1, 'Never', 0),
(13, 'How confident do you feel?', 'Very', 3, 'Moderate', 2, 'Low', 1, 'None', 0),
(14, 'How often do you feel calm?', 'Always', 3, 'Often', 2, 'Rarely', 1, 'Never', 0),
(15, 'Do you feel overwhelmed?', 'Never', 3, 'Sometimes', 2, 'Often', 1, 'Always', 0),
(16, 'How is your concentration?', 'Excellent', 3, 'Good', 2, 'Poor', 1, 'Very poor', 0),
(17, 'How often do you feel hopeless?', 'Never', 3, 'Sometimes', 2, 'Often', 1, 'Always', 0),
(18, 'Do you feel energetic?', 'Always', 3, 'Often', 2, 'Rarely', 1, 'Never', 0),
(19, 'How do you handle stress?', 'Very well', 3, 'Okay', 2, 'Poorly', 1, 'Very poorly', 0),
(20, 'Do you feel emotionally stable?', 'Very', 3, 'Somewhat', 2, 'Not much', 1, 'Not at all', 0),
(21, 'How often do you worry?', 'Never', 3, 'Sometimes', 2, 'Often', 1, 'Always', 0),
(22, 'Do you feel positive about future?', 'Very', 3, 'Somewhat', 2, 'Not much', 1, 'Not at all', 0),
(23, 'How often do you feel relaxed?', 'Always', 3, 'Often', 2, 'Rarely', 1, 'Never', 0),
(24, 'Do you feel in control of your life?', 'Fully', 3, 'Somewhat', 2, 'Little', 1, 'Not at all', 0),
(25, 'How often do you feel irritable?', 'Never', 3, 'Sometimes', 2, 'Often', 1, 'Always', 0)
''')

cursor.execute('''
INSERT OR IGNORE INTO diary_entries (id, user_id, title, content, created_at) VALUES
(67, 1, 'hi', '<div style="text-align: left;">helo</div>', '2026-04-15 02:21:55'),
(69, 1, 'helo', '<b>hiohb</b><div>iuyuk<b>jygh</b></div>', '2026-04-15 02:41:25'),
(70, 2, 'hi', 'helloo', '2026-04-15 22:22:05'),
(72, 1, 'hy', 'oug', '2026-04-16 03:19:58'),
(73, 16, 'Zenzest Project Plan', 'Day 1 -<div><ol><li>&nbsp;Install Python Flask</li><li>Download others packages</li><li>Create a project</li></ol></div>', '2026-04-22 13:18:47')
''')

cursor.execute('''
INSERT OR IGNORE INTO doctor_assigned (student_email, student_name, doctor_name, doctor_email) VALUES
('jake@gmail.com', 'Jake', 'Dr Remya', 'remya@gmail.com'),
('jyothsna@gmail.com', 'Jyothsna', 'Dr Remya', 'remya@gmail.com'),
('nandini@gmail.com', 'Nandini', 'Dr Remya', 'remya@gmail.com')
''')

conn.commit()
conn.close()

print(f"SQLite database '{DB_PATH}' created successfully!")
