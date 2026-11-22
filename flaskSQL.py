import sqlite3
from flask import Flask, render_template, g, request, redirect, url_for

app = Flask(__name__)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("school.db")
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")

    return g.db

def create_table():
    db = get_db()

    db.execute("""
    
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY,
            student_id INTEGER,
            amount INTEGER,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    
    """)
    db.commit()

def get_students():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM students")
    return cursor.fetchall()


@app.teardown_appcontext
def close_db(error=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


@app.route("/students")
def students():
    student_records = get_students()

    return render_template(
        "students.html",
        students=student_records
    )


@app.route("/add-student", methods=['GET', 'POST'])
def add_student_page():

    if request.method == "POST":
        student_name = request.form.get("name")
        student_age = request.form.get("age")

        if not student_name or not student_name.strip():
            return render_template("add_students.html")

        if not student_age:
            return render_template("add_students.html")

        try:
            student_age_to_number = int(student_age)
        except ValueError:
            return render_template("add_students.html")

        if student_age_to_number <= 0:
            return render_template("add_students.html")

        save_student = get_db()
        cursor = save_student.cursor()

        cursor.execute(
            "INSERT INTO students (name, age) VALUES (?, ?)",
            (student_name.strip(), student_age_to_number)
        )

        save_student.commit()

        return redirect(url_for("students"))

    return render_template("add_students.html")


@app.route("/update-student/<int:student_id>", methods=['GET', 'POST'])
def update_student(student_id):

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if student is None:
        return "Student not found"

    if request.method == "POST":

        updated_name = request.form.get("name")
        update_age = request.form.get("age")

        if not updated_name or not updated_name.strip():
            return "Name is required"

        if not update_age:
            return "Age is required"

        try:
            update_age = int(update_age)
        except ValueError:
            return "Age must be a valid number"

        if update_age <= 0:
            return "Age must be greater than zero"

        cursor.execute(
            "UPDATE students SET name = ?, age = ? WHERE id = ?",
            (updated_name.strip(), update_age, student_id)
        )

        db.commit()

        return redirect(url_for("students"))

    return render_template(
        "edit_student.html",
        student=student
    )


@app.route("/delete-student/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    db = get_db()

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )
    db.commit()

    return redirect(url_for("students"))


@app.route("/setup-database")
def setup_database():
    create_table()
    return "Payment table created"

@app.route("/add-payment")
def add_payment():
    db = get_db()

    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO payments (student_id, amount) VALUES(?, ?)",
        (2, 5000)
    )
    db.commit()
    return "Payment Successful"


@app.route("/payments")
def payments():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT payments.id, students.name, payments.amount
        FROM payments
        JOIN students
        ON payments.student_id = students.id;
    """)

    payments = cursor.fetchall()
    
    return render_template(
        "payments.html",
        payments=payments
    )


import sqlite3
from flask import Flask, render_template, g, request, redirect, url_for

app = Flask(__name__)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("school.db")
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")

    return g.db

def create_table():
    db = get_db()

    db.execute("""
    
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY,
            student_id INTEGER,
            amount INTEGER,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    
    """)
    db.commit()

def get_students():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM students")
    return cursor.fetchall()


@app.teardown_appcontext
def close_db(error=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


@app.route("/students")
def students():
    student_records = get_students()

    return render_template(
        "students.html",
        students=student_records
    )


@app.route("/add-student", methods=['GET', 'POST'])
def add_student_page():

    if request.method == "POST":
        student_name = request.form.get("name")
        student_age = request.form.get("age")

        if not student_name or not student_name.strip():
            return render_template("add_students.html")

        if not student_age:
            return render_template("add_students.html")

        try:
            student_age_to_number = int(student_age)
        except ValueError:
            return render_template("add_students.html")

        if student_age_to_number <= 0:
            return render_template("add_students.html")

        save_student = get_db()
        cursor = save_student.cursor()

        cursor.execute(
            "INSERT INTO students (name, age) VALUES (?, ?)",
            (student_name.strip(), student_age_to_number)
        )

        save_student.commit()

        return redirect(url_for("students"))

    return render_template("add_students.html")


@app.route("/update-student/<int:student_id>", methods=['GET', 'POST'])
def update_student(student_id):

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if student is None:
        return "Student not found"

    if request.method == "POST":

        updated_name = request.form.get("name")
        update_age = request.form.get("age")

        if not updated_name or not updated_name.strip():
            return "Name is required"

        if not update_age:
            return "Age is required"

        try:
            update_age = int(update_age)
        except ValueError:
            return "Age must be a valid number"

        if update_age <= 0:
            return "Age must be greater than zero"

        cursor.execute(
            "UPDATE students SET name = ?, age = ? WHERE id = ?",
            (updated_name.strip(), update_age, student_id)
        )

        db.commit()

        return redirect(url_for("students"))

    return render_template(
        "edit_student.html",
        student=student
    )


@app.route("/delete-student/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    db = get_db()

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )
    db.commit()

    return redirect(url_for("students"))


@app.route("/setup-database")
def setup_database():
    create_table()
    return "Payment table created"

@app.route("/add-payment")
def add_payment():
    db = get_db()

    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO payments (student_id, amount) VALUES(?, ?)",
        (2, 5000)
    )
    db.commit()
    return "Payment Successful"


@app.route("/payments")
def payments():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT payments.id, students.name, payments.amount
        FROM payments
        JOIN students
        ON payments.student_id = students.id;
    """)

    payments = cursor.fetchall()
    
    return render_template(
        "payments.html",
        payments=payments
    )


@app.route("/student-payments")
def student_payments():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT students.name, payments.amount
        FROM stidents, payments
        LEFT JOIN students
        ON students.id = payments.student.id
    """)

    student_payments = cursor.fetchall()

    return render_template(
        "student_payments.html",
        student_payments=student_payments
    )


if __name__ == "__main__":
    app.run(debug=True)


if __name__ == "__main__":
    app.run(debug=True)