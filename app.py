from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

app.secret_key = "your_secret_key"

# SQLite Configuration
DB_PATH = 'mental_health_app.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['email'] = user[2]
            session['role'] = user[4]

            if user[4] == 'Student':
                return redirect('/home')
            elif user[4] == 'Admin':
                return redirect('/admin')
            elif user[4] == 'Counsellor':
                return redirect('/counsellor')
            else:
                error = "Invalid user role"
        else:
            error = "Invalid email or password"

    return render_template("login.html", error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        session['signup_data'] = {
            'username': request.form['username'],
            'email': request.form['email'],
            'password': request.form['password'],
            'role': request.form['role']
        }

        # 👉 Only students select doctor
        if request.form['role'] == 'Student':
            return redirect('/select-doctor')
        else:
            # Direct signup for others
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
                (
                    request.form['username'],
                    request.form['email'],
                    request.form['password'],
                    request.form['role']
                )
            )
            conn.commit()
            conn.close()

            return redirect('/')

    return render_template("signup.html")

@app.route('/check-doctor', methods=['POST'])
def check_doctor():
    query = (request.json.get('email') or request.json.get('query') or '').strip()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT username, email FROM users
        WHERE role='Counsellor'
          AND (LOWER(username) LIKE ? OR LOWER(email) LIKE ?)
        ORDER BY username
        LIMIT 1
        """,
        ('%' + query.lower() + '%', '%' + query.lower() + '%')
    )
    doctor = cursor.fetchone()
    conn.close()

    if doctor:
        return jsonify({
            "status": "found",
            "name": doctor[0],
            "email": doctor[1]
        })
    return jsonify({"status": "not_found"})
    
@app.route('/confirm-doctor', methods=['POST'])
def confirm_doctor():
    data = session.get('signup_data')

    if not data:
        return redirect('/signup')

    doctor_email = request.form['doctor_email']
    doctor_name = request.form['doctor_name']

    conn = get_db()
    cursor = conn.cursor()

    # ✅ Insert user NOW (correct place)
    cursor.execute("""
        INSERT INTO users (username, email, password, role)
        VALUES (?, ?, ?, ?)
    """, (
        data['username'],
        data['email'],
        data['password'],
        data['role']
    ))

    # ✅ Insert doctor assignment
    cursor.execute("""
        INSERT INTO doctor_assigned 
        (student_email, student_name, doctor_name, doctor_email)
        VALUES (?, ?, ?, ?)
    """, (
        data['email'],
        data['username'],
        doctor_name,
        doctor_email
    ))

    conn.commit()
    conn.close()

    session.pop('signup_data', None)

    return redirect('/')

@app.route('/get-counsellor-list')
def get_counsellor_list():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username, email FROM users WHERE role='Counsellor' ORDER BY username")
    rows = cursor.fetchall()
    conn.close()

    return jsonify([
        {"name": row[0], "email": row[1]} for row in rows
    ])


@app.route('/reassign-doctor', methods=['POST'])
def reassign_doctor():
    if session.get('role') != 'Student':
        return jsonify({"status": "error", "message": "Only students can reassign a doctor."}), 403

    data = request.get_json()
    doctor_name = data.get('doctor_name', '').strip()
    doctor_email = data.get('doctor_email', '').strip()

    if not doctor_name or not doctor_email:
        return jsonify({"status": "error", "message": "Doctor details are required."}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO doctor_assigned (student_email, student_name, doctor_name, doctor_email)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(student_email) DO UPDATE SET
            student_name=excluded.student_name,
            doctor_name=excluded.doctor_name,
            doctor_email=excluded.doctor_email
    """, (session.get('email'), session.get('username'), doctor_name, doctor_email))
    conn.commit()
    conn.close()

    return jsonify({"status": "ok", "message": "Doctor reassigned successfully."})


@app.route('/get-doctor')
def get_doctor():
    user_email = session.get('email')
    role = session.get('role')

    conn = get_db()
    cursor = conn.cursor()

    if role == "Student":
        cursor.execute("""
            SELECT doctor_name, doctor_email
            FROM doctor_assigned
            WHERE student_email = ?
        """, (user_email,))
        
        doctor = cursor.fetchone()
        conn.close()

        if doctor:
            return jsonify({
                "name": doctor[0],
                "email": doctor[1]
            })

    elif role == "Counsellor":
        cursor.execute("""
            SELECT student_name, student_email
            FROM doctor_assigned
            WHERE doctor_email = ?
        """, (user_email,))
        
        students = cursor.fetchall()
        conn.close()

        return jsonify([
            {"name": s[0], "email": s[1]} for s in students
        ])

    conn.close()
    return jsonify({})

@app.route('/get-questions')
def get_questions():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions")
    rows = cursor.fetchall()
    conn.close()

    questions = []
    for r in rows:
        questions.append({
            "question": r[1],
            "options": [
                {"text": r[2], "score": r[3]},
                {"text": r[4], "score": r[5]},
                {"text": r[6], "score": r[7]},
                {"text": r[8], "score": r[9]}
            ]
        })

    return jsonify(questions)

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()

    sender_id = session.get('user_id')
    receiver_id = data.get('receiver_id')
    message = data.get('message')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO messages (sender_id, receiver_id, message)
        VALUES (?, ?, ?)
    """, (sender_id, receiver_id, message))

    conn.commit()
    conn.close()

    return jsonify({"status": "sent"})  

@app.route('/get-messages/<int:other_user_id>')
def get_messages(other_user_id):
    user_id = session.get('user_id')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sender_id, message, created_at
        FROM messages
        WHERE (sender_id=? AND receiver_id=?)
           OR (sender_id=? AND receiver_id=?)
        ORDER BY created_at ASC
    """, (user_id, other_user_id, other_user_id, user_id))

    rows = cursor.fetchall()
    conn.close()

    messages = []
    for r in rows:
        # Parse timestamp string if needed
        timestamp = r[2]
        if isinstance(timestamp, str):
            time_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            time_str = time_obj.strftime("%H:%M")
        else:
            time_str = timestamp.strftime("%H:%M")
        
        messages.append({
            "sender": r[0],
            "message": r[1],
            "time": time_str
        })

    return jsonify(messages)

@app.route('/get-user-id-by-email', methods=['POST'])
def get_user_id():
    email = request.json.get('email')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"user_id": user[0]})
    return jsonify({})

@app.route('/get-assigned-students')
def get_assigned_students():
    doctor_email = session.get('email')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT student_name, student_email
        FROM doctor_assigned
        WHERE doctor_email = ?
    """, (doctor_email,))

    rows = cursor.fetchall()
    conn.close()

    return jsonify([
        {"name": r[0], "email": r[1]} for r in rows
    ])

@app.route('/counsellor-messages')
def counsellor_messages():
    return render_template(
        "Counsellor/messages.html",
        user_id=session['user_id']
    )

@app.route('/student-profile')
def student_profile():
    email = request.args.get('email')
    return render_template('Counsellor/student_profile.html', email=email)


@app.route('/student-progress-data')
def student_progress_data():
    email = request.args.get('email', '').strip()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE email=? AND role='Student'", (email,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return jsonify({"username": "Student", "progress": [], "games": []})

    user_id = user[0]
    cursor.execute("""
        SELECT created_at, score, percentage
        FROM questionnaire_results
        WHERE user_id=?
        ORDER BY created_at DESC
    """, (user_id,))
    progress_rows = cursor.fetchall()

    cursor.execute("""
        SELECT game_name, score, moves, created_at
        FROM game_scores
        WHERE user_id=?
        ORDER BY created_at DESC
        LIMIT 10
    """, (user_id,))
    game_rows = cursor.fetchall()
    conn.close()

    progress = []
    for row in progress_rows:
        timestamp = row[0]
        if isinstance(timestamp, str):
            date_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            date_str = date_obj.strftime("%b %d, %Y")
        else:
            date_str = timestamp.strftime("%b %d, %Y")
        progress.append({"date": date_str, "score": row[1], "percentage": row[2]})

    games = []
    for row in game_rows:
        timestamp = row[3]
        if isinstance(timestamp, str):
            time_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            time_str = time_obj.strftime("%b %d, %I:%M %p")
        else:
            time_str = timestamp.strftime("%b %d, %I:%M %p")
        games.append({"game": row[0], "score": row[1], "moves": row[2], "time": time_str})

    return jsonify({"username": user[1], "progress": progress, "games": games})

@app.route('/admin/get-students')
def admin_get_students():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.id, u.username, u.email, u.password, d.doctor_name, d.doctor_email
        FROM users u
        LEFT JOIN doctor_assigned d 
        ON u.email = d.student_email
        WHERE u.role='Student'
    """)
    rows = cursor.fetchall()
    conn.close()

    return jsonify([
        {
            "id": r[0],
            "name": r[1],
            "email": r[2],
            "password": r[3],
            "doctor": r[4] if r[4] else "Not Assigned",
            "doctor_email": r[5] if r[5] else ""
        } for r in rows
    ])

@app.route('/admin/delete-student/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT email FROM users WHERE id=? AND role='Student'", (id,))
    student = cursor.fetchone()

    if student:
        cursor.execute("DELETE FROM doctor_assigned WHERE student_email=?", (student[0],))

    cursor.execute("DELETE FROM users WHERE id=? AND role='Student'", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Student deleted"})

@app.route('/admin/update-student', methods=['POST'])
def update_student():
    data = request.get_json()

    conn = get_db()
    cursor = conn.cursor()
    password = data.get('password', '')

    cursor.execute("SELECT email FROM users WHERE id=? AND role='Student'", (data['id'],))
    current_student = cursor.fetchone()
    old_student_email = current_student[0] if current_student else data['email']

    cursor.execute("""
        UPDATE users 
        SET username=?, email=?, password=? 
        WHERE id=? AND role='Student'
    """, (data['name'], data['email'], password, data['id']))

    cursor.execute("""
        UPDATE doctor_assigned
        SET student_email=?, student_name=?
        WHERE student_email=?
    """, (data['email'], data['name'], old_student_email))

    conn.commit()
    conn.close()

    return jsonify({"message": "Updated"})

@app.route('/admin/get-counsellors')
def admin_get_counsellors():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, password FROM users WHERE role='Counsellor'")
    rows = cursor.fetchall()
    conn.close()

    return jsonify([
        {"id": r[0], "name": r[1], "email": r[2], "password": r[3]} for r in rows
    ])

@app.route('/admin/get-counsellor-students/<int:id>')
def admin_get_counsellor_students(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT username, email FROM users WHERE id=? AND role='Counsellor'", (id,))
    counsellor = cursor.fetchone()

    if not counsellor:
        conn.close()
        return jsonify([])

    counsellor_email = counsellor[1]
    cursor.execute("""
        SELECT u.username, u.email, d.doctor_email
        FROM users u
        LEFT JOIN doctor_assigned d
        ON u.email = d.student_email
        WHERE u.role='Student'
        ORDER BY u.username
    """)
    rows = cursor.fetchall()
    conn.close()

    return jsonify([
        {
            "name": r[0],
            "email": r[1],
            "assigned": r[2] == counsellor_email,
            "assigned_doctor_email": r[2] or ""
        } for r in rows
    ])

@app.route('/admin/delete-counsellor/<int:id>', methods=['DELETE'])
def delete_counsellor(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT email FROM users WHERE id=? AND role='Counsellor'", (id,))
    counsellor = cursor.fetchone()

    if counsellor:
        cursor.execute("UPDATE doctor_assigned SET doctor_name=NULL, doctor_email=NULL WHERE doctor_email=?", (counsellor[0],))

    cursor.execute("DELETE FROM users WHERE id=? AND role='Counsellor'", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Deleted"})

@app.route('/admin/update-counsellor', methods=['POST'])
def update_counsellor():
    data = request.get_json()

    conn = get_db()
    cursor = conn.cursor()
    password = data.get('password', '')

    cursor.execute("SELECT email FROM users WHERE id=? AND role='Counsellor'", (data['id'],))
    current_counsellor = cursor.fetchone()
    old_counsellor_email = current_counsellor[0] if current_counsellor else data['email']

    cursor.execute("""
        UPDATE users 
        SET username=?, email=?, password=? 
        WHERE id=? AND role='Counsellor'
    """, (data['name'], data['email'], password, data['id']))

    cursor.execute("""
        UPDATE doctor_assigned
        SET doctor_name=?, doctor_email=?
        WHERE doctor_email=?
    """, (data['name'], data['email'], old_counsellor_email))

    if 'assigned_students' in data:
        assigned_students = data.get('assigned_students') or []

        cursor.execute("""
            UPDATE doctor_assigned
            SET doctor_name=NULL, doctor_email=NULL
            WHERE doctor_email=?
        """, (data['email'],))

        for student_email in assigned_students:
            cursor.execute("SELECT username FROM users WHERE email=? AND role='Student'", (student_email,))
            student = cursor.fetchone()
            if not student:
                continue

            cursor.execute("""
                INSERT INTO doctor_assigned (student_email, student_name, doctor_name, doctor_email)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(student_email) DO UPDATE SET
                    student_name=excluded.student_name,
                    doctor_name=excluded.doctor_name,
                    doctor_email=excluded.doctor_email
            """, (student_email, student[0], data['name'], data['email']))

    conn.commit()
    conn.close()

    return jsonify({"message": "Updated"})

@app.route('/admin/get-progress/<int:user_id>')
def admin_get_progress(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT created_at, score, percentage
        FROM questionnaire_results
        WHERE user_id=?
        ORDER BY created_at DESC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    result = []
    for r in rows:
        # Parse timestamp if needed
        timestamp = r[0]
        if isinstance(timestamp, str):
            date_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            date_str = date_obj.strftime("%b %d, %Y")
        else:
            date_str = timestamp.strftime("%b %d, %Y")
        
        result.append({
            "date": date_str,
            "score": r[1],
            "percentage": r[2]
        })

    return jsonify(result)

@app.route('/admin/get-questions')
def admin_get_questions():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions")
    rows = cursor.fetchall()
    conn.close()

    data = []
    for r in rows:
        data.append({
            "id": r[0],
            "question": r[1],
            "options": [r[2], r[4], r[6], r[8]],
            "scores": [r[3], r[5], r[7], r[9]]
        })

    return jsonify(data)

@app.route('/admin/add-question', methods=['POST'])
def add_question():
    data = request.get_json()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO questions 
        (question, option_a, score_a, option_b, score_b, option_c, score_c, option_d, score_d)
        VALUES (?,?,?,?,?,?,?,?,?)
    """, (
        data['question'],
        data['opt1'], data['score1'],
        data['opt2'], data['score2'],
        data['opt3'], data['score3'],
        data['opt4'], data['score4']
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Added"})

@app.route('/admin/update-question', methods=['POST'])
def update_question():
    data = request.get_json()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE questions SET
        question=?,
        option_a=?, score_a=?,
        option_b=?, score_b=?,
        option_c=?, score_c=?,
        option_d=?, score_d=?
        WHERE id=?
    """, (
        data['question'],
        data['opt1'], data['score1'],
        data['opt2'], data['score2'],
        data['opt3'], data['score3'],
        data['opt4'], data['score4'],
        data['id']
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Updated"})

@app.route('/admin/delete-question/<int:id>', methods=['DELETE'])
def delete_question(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM questions WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Deleted"})

@app.route('/forgotpassword')
def forgotpassword():
    return render_template("forgot-password.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/admin')
def admin():
    return render_template("Admin/admin.html")

@app.route('/counsellor')
def counsellor ():
    return render_template("Counsellor/counsellor.html")

@app.route('/select-doctor')
def sd():
    return render_template("dr_selection.html")

@app.route('/StudentMessage')
def stMessage():
    return render_template("student_message.html", user_id=session['user_id'])

@app.route('/mh')
def mh():
    return render_template("mentalhealth.html")

@app.route('/About')
def about():
    return render_template("about.html")

@app.route('/Contact')
def contact():
    return render_template("contact.html")

@app.route('/Questionnaire - Start')
def questionnairestart():
    return render_template("questionstartpage.html")

@app.route('/Questionnaire')
def questionnaire():
    return render_template("questionnaire.html")


@app.route('/Games')
def games():
    return render_template("games.html")


@app.route('/Diary')
def diary():
    return render_template("diary.html")


@app.route('/Current-Status')
def status():
    return render_template("status.html")

@app.route('/Sudoku')
def sudoku():
    return render_template("sudoku.html")


@app.route('/MemoryGame')
def memory():
    return render_template("memory-game.html")


@app.route('/WordScramble')
def wordScramble():
    return render_template("word-scramble.html")


@app.route('/TicTacToe')
def tictactoe():
    return render_template("tic-tac-toe.html")

@app.route('/PrivacyPolicy')
def privacypolicy():
    return render_template("privacy-policy.html")

@app.route('/save-score', methods=['POST'])
def save_score():
    data = request.get_json()

    game_name = data.get('game_name')
    score = data.get('score')
    time = data.get('time')
    moves = data.get('moves')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO game_scores (user_id, game_name, score, time, moves)
        VALUES (?, ?, ?, ?, ?)
    """, (session.get('user_id'), game_name, score, time, moves))

    conn.commit()
    conn.close()

    return jsonify({"message": "Score saved"})

@app.route('/save-questionnaire', methods=['POST'])
def save_questionnaire():
    data = request.get_json()

    score = data.get('score')
    percentage = data.get('percentage')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO questionnaire_results (user_id, score, percentage)
        VALUES (?, ?, ?)
    """, (session.get('user_id'), score, percentage))

    conn.commit()
    conn.close()

    return jsonify({"message": "Saved"})

@app.route('/save-diary', methods=['POST'])
def save_diary():
    data = request.get_json()

    title = data.get('title')
    content = data.get('content')
    note_id = data.get('id')

    conn = get_db()
    cursor = conn.cursor()

    if note_id:  
        # UPDATE existing note
        cursor.execute("""
            UPDATE diary_entries 
            SET title=?, content=? 
            WHERE id=? AND user_id=?
        """, (title, content, note_id, session.get('user_id')))
    else:
        # INSERT new note
        cursor.execute("""
            INSERT INTO diary_entries (user_id, title, content)
            VALUES (?, ?, ?)
        """, (session.get('user_id'), title, content))

    conn.commit()
    conn.close()

    return jsonify({"message": "Saved"})

@app.route('/get-diary')
def get_diary():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, content 
        FROM diary_entries 
        WHERE user_id=? 
        ORDER BY created_at DESC
    """, (session.get('user_id'),))

    notes = cursor.fetchall()
    conn.close()

    result = []
    for n in notes:
        result.append({
            "id": n[0],
            "title": n[1],
            "content": n[2]
        })

    return jsonify(result)

@app.route('/delete-diary/<int:id>', methods=['DELETE'])
def delete_diary(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM diary_entries 
        WHERE id=? AND user_id=?
    """, (id, session.get('user_id')))

    conn.commit()
    conn.close()

    return jsonify({"message": "Deleted"})

@app.route('/get-user')
def get_user():
    return jsonify({"username": session['username']})

@app.route('/get-progress')
def get_progress():
    user_id = session['user_id']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT created_at, score 
        FROM questionnaire_results
        WHERE user_id = ? 
        ORDER BY created_at DESC 
        LIMIT 7
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    data = []
    for row in rows:
        # Parse timestamp if needed
        timestamp = row[0]
        if isinstance(timestamp, str):
            date_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            day_str = date_obj.strftime("%b %d")
        else:
            day_str = timestamp.strftime("%b %d")
        
        data.append({
            "day": day_str,
            "score": row[1]
        })

    return jsonify(data)

@app.route('/get-games')
def get_games():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify([])

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT game_name, score, moves, created_at
        FROM game_scores
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 10
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    data = []

    for row in rows:
        # Parse timestamp if needed
        timestamp = row[3]
        if isinstance(timestamp, str):
            time_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            time_str = time_obj.strftime("%b %d, %I:%M %p")
        else:
            time_str = timestamp.strftime("%b %d, %I:%M %p")
        
        data.append({
            "game": row[0],
            "score": row[1],
            "moves": row[2],
            "time": time_str
        })

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
