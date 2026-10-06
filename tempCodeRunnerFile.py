.commit()
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
    for r in ro