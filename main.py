import streamlit as st
import sqlite3
from streamlit_option_menu import option_menu

# Database connection
def connectdb():
    return sqlite3.connect("mydb.db")

# Create table if not exists
def createTable():
    with connectdb() as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS student(name TEXT, password TEXT, roll INTEGER PRIMARY KEY, branch TEXT)")
        conn.commit()

# Insert record into database
def addRecord(data):
    with connectdb() as conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO student(name, password, roll, branch) VALUES (?, ?, ?, ?)", data)
            conn.commit()
        except sqlite3.IntegrityError:
            st.error("Student already registered!")

# Fetch all student records
def display():
    with connectdb() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM student")
        return cur.fetchall()

# Search student by roll number
def search_student(roll):
    with connectdb() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM student WHERE roll = ?", (roll,))
        return cur.fetchone()

# Delete student by roll number
def delete_student(roll):
    with connectdb() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM student WHERE roll = ?", (roll,))
        conn.commit()
        st.success("Student record deleted successfully!")

# Update password
def reset_password(roll, new_password):
    with connectdb() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE student SET password = ? WHERE roll = ?", (new_password, roll))
        conn.commit()
        st.success("Password updated successfully!")

# Signup form
def signup():
    st.title("Registration Page")
    name = st.text_input("Enter name")
    password = st.text_input("Enter password", type='password')
    repassword = st.text_input("Retype your password", type='password')
    roll = st.number_input("Enter roll number", format="%0.0f")
    branch = st.selectbox("Select Branch", options=['CSE', 'AIML', 'IT', 'ECE'])

    if st.button('Sign Up'):
        if password != repassword:
            st.warning("Password mismatch!")
        else:
            addRecord((name, password, roll, branch))
            st.success("Student Registered Successfully!")

# Display records with branch filter
def display_records():
    st.title("All Student Records")

    # Filter records by branch
    branch_filter = st.selectbox("Filter by Branch", options=['All', 'CSE', 'AIML', 'IT', 'ECE'])
    data = display()

    if branch_filter != 'All':
        data = [record for record in data if record[3] == branch_filter]

    st.table(data)

# Search by roll number
def search():
    st.title("Search Student")
    roll = st.number_input("Enter Roll Number", format="%0.0f")

    if st.button("Search"):
        student = search_student(roll)
        if student:
            st.success(f"Student Found: {student}")
        else:
            st.error("No student found with this Roll Number!")

# Reset Password Form
def reset_pass():
    st.title("Reset Password")
    roll = st.number_input("Enter Roll Number", format="%0.0f")
    new_password = st.text_input("Enter New Password", type='password')

    if st.button("Reset Password"):
        reset_password(roll, new_password)

# Delete Record
def delete_record():
    st.title("Delete Student Record")
    roll = st.number_input("Enter Roll Number to Delete", format="%0.0f")

    if st.button("Delete"):
        delete_student(roll)

# Sidebar Menu
with st.sidebar:
    selected = option_menu("My App", ['Signup', 'Display All Records', 'Search', 'Reset Password', 'Delete Record'])

# Ensure table exists
createTable()

# Page navigation
if selected == 'Signup':
    signup()
elif selected == 'Display All Records':
    display_records()
elif selected == 'Search':
    search()
elif selected == 'Reset Password':
    reset_pass()
elif selected == 'Delete Record':
    delete_record()
