from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import random
import os

app = Flask(__name__)
app.secret_key = "erp_secret"

# ================= LOGIN USERS =================
users = {
    "Satya": "satyaerp",
    "Kesav": "kesaverp",
    "Somesh": "somesherp",
    "Ravi": "ravierp",
    "Sudheer": "sudheererp"
}

# ================= SUBJECTS =================
cse_subjects = ["java", "python", "dti", "maths", "ds"]
aids_subjects = ["python", "ids", "ai", "java", "dsp", "dlco","python"]

# ================= STUDENT DATABASE =================
students = {
    "1st year": ["mani", "pavan", "rakesh", "dhoni", "muni", "mahesh"],
    "2nd year": ["pavan", "nukesh", "satya", "kesav", "somesh", "devara", "eswar", "ravi"],
    "2nd year": ["ram","tony","edith","edward","peter","danie","sai"]
}

# ================= ROUTES =================

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/login', methods=["POST"])
def do_login():
    username = request.form["username"]
    password = request.form["password"]

    if username in users and users[username] == password:
        session["user"] = username
        return redirect(url_for("chat"))
    else:
        return "Invalid credentials"

@app.route('/chat')
def chat():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("chat.html", user=session["user"])

# ================= FETCH DATA =================

@app.route('/get_data', methods=["POST"])
def get_data():

    data = request.json
    name = data["student"].lower()
    year = data["year"].lower()
    branch = data["branch"].lower()
    query_type = data["type"]
    subject = data.get("subject", "").lower()

    # Validate year
    if year not in students:
        return jsonify({"error": "Invalid year. Only 1st year & 2nd year available."})

    # Validate student
    if name not in students[year]:
        return jsonify({"error": f"{name.title()} not found in {year}."})

    # Select subjects
    if branch == "cse":
        valid_subjects = cse_subjects
    elif branch == "aids":
        valid_subjects = aids_subjects
    else:
        return jsonify({"error": "Branch must be CSE or AIDS."})

    # Validate subject
    if subject not in valid_subjects:
        return jsonify({"error": f"Invalid subject for {branch.upper()}."})

    # ========== ATTENDANCE ==========
    if query_type == "attendance":
        attendance = random.randint(60, 100)
        message = f"{attendance}% attendance in {subject}"

        if attendance < 75:
            message += ". ⚠ Your attendance is low. Attend daily classes to improve your attendance percentage."

        return jsonify({"result": message})

    # ========== MARKS ==========
    elif query_type == "marks":
        marks = random.randint(50, 100)
        return jsonify({"result": f"{marks}/100 in {subject}"})

    # ========== EXAM DATE ==========
    elif query_type == "exam":
        exam_date = datetime(2026, 3, 26)
        return jsonify({"result": f"{subject} exam on {exam_date.strftime('%d %B %Y')}"})

    return jsonify({"error": "Invalid query type"})

# ================= PDF REPORT =================

@app.route("/download_report", methods=["POST"])
def download_report():

    data = request.json
    name = data["student"].lower()
    year = data["year"].lower()
    branch = data["branch"].lower()

    if year not in students or name not in students[year]:
        return jsonify({"error": "Student not found!"})

    if branch == "cse":
        subject_list = cse_subjects
    elif branch == "aids":
        subject_list = aids_subjects
    else:
        return jsonify({"error": "Invalid branch!"})

    file_path = f"{name}_report.pdf"
    doc = SimpleDocTemplate(file_path)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("Student Full Report", styles["Title"]))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(f"Name: {name.title()}", styles["Normal"]))
    elements.append(Paragraph(f"Year: {year.title()}", styles["Normal"]))
    elements.append(Paragraph(f"Branch: {branch.upper()}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    # Attendance Table
    elements.append(Paragraph("Attendance", styles["Heading2"]))
    attendance_data = [["Subject", "Percentage"]]

    for subject in subject_list:
        percent = random.randint(60, 100)
        status = " (Low)" if percent < 75 else ""
        attendance_data.append([subject, f"{percent}%{status}"])

    attendance_table = Table(attendance_data)
    attendance_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))

    elements.append(attendance_table)
    elements.append(Spacer(1, 20))

    # Marks Table
    elements.append(Paragraph("Marks", styles["Heading2"]))
    marks_data = [["Subject", "Marks"]]

    for subject in subject_list:
        marks = random.randint(50, 100)
        marks_data.append([subject, f"{marks}/100"])

    marks_table = Table(marks_data)
    marks_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))

    elements.append(marks_table)
    elements.append(Spacer(1, 20))

    # Exam Date Section
    elements.append(Paragraph("Exam Dates", styles["Heading2"]))
    exam_data = [["Subject", "Date"]]

    for subject in subject_list:
        exam_data.append([subject, "26 March 2026"])

    exam_table = Table(exam_data)
    exam_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))

    elements.append(exam_table)

    doc.build(elements)

    return send_file(file_path, as_attachment=True)

# ================= LOGOUT =================

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)