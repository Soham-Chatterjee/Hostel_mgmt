import tkinter
import tkinter.messagebox
import pickle
import mysql.connector
import os
from hostel_mgmt.gen_details_pdf import gen_details_pdf

db = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='password',
    database='hostel_mgmt',
)

cursor = db.cursor(buffered=True)

def get_stu_for_show():
    heading_list = ['Student ID', 'Name', 'Contact','Course ID', 'Room ID']
    cursor.execute(f"select s.stu_id, sd.name, sd.contact_no, s.course_id, s.room_id from student s, stu_details sd where s.stu_id=sd.stu_id")
    return ('stu_details', heading_list, cursor.fetchall())



def get_block_for_show():
    heading_list = ['Block ID', 'Type', 'Gender', 'Total Rooms', 'Number of beds', 'Vacant Beds']
    cursor.execute(f"select block_id, block_type, gender, no_of_rooms, no_of_beds, vacant_beds from blocks")
    return ('block_details', heading_list, cursor.fetchall())



def get_room_for_show():
    heading_list = ['Room ID', 'Block ID', 'Type', 'Total Rooms', 'Occupants']
    cursor.execute(f"select room_id, block_id, room_type, no_of_beds, occupants from room")
    return ('room_details', heading_list, cursor.fetchall())



def get_staff_for_show():
    heading_list = ['Staff ID', 'Name', 'Gender', 'Date of Birth', 'Contact']
    cursor.execute(f"select staff_id, name, gender, dob, contact_no from staff")
    return ('staff_details', heading_list, cursor.fetchall())



def get_mess_for_show():
    heading_list = ['Mess ID']
    cursor.execute(f"select mess_id from mess")
    return ('mess_details', heading_list, cursor.fetchall())

def get_courses_for_show():
    heading_list = ['Course ID', 'Course Name', 'Semesters']
    cursor.execute(f"select course_id, course_name, num_sems from courses")
    return ('courses_details', heading_list, cursor.fetchall())

with open("pvt.dat", "rb") as pvt_file:
    pswd_correct = pickle.load(pvt_file)

def on_close():
    result = tkinter.messagebox.askyesno("RSGH - RMD", "Do you want to exit the database?")
    if result == True:
        quit()
try:
    directory = "details"
    filedir = os.getcwd()
    subdir = os.path.join(filedir, directory)
    os.mkdir(subdir)
except FileExistsError as e:
    pass

try:
    directory = "fee receipts"
    filedir = os.getcwd()
    subdir = os.path.join(filedir, directory)
    os.mkdir(subdir)
except FileExistsError:
    pass



root = tkinter.Tk()


w, h = root.winfo_screenwidth(), root.winfo_screenheight()
pos_x = int(root.winfo_screenwidth()/2 - w/2)
pos_y = int(root.winfo_screenheight()/2 - h/2)
root.state("zoomed")
root.minsize(w,h)
root.title("RSGH - Records Management Database - Administrator")


import hostel_mgmt.auth

import hostel_mgmt.design

root.protocol('WM_DELETE_WINDOW', on_close)
filename, heading, data = get_stu_for_show()
gen_details_pdf(filename, heading, data)
filename, heading, data = get_room_for_show()
gen_details_pdf(filename, heading, data)
filename, heading, data = get_block_for_show()
gen_details_pdf(filename, heading, data)
filename, heading, data = get_mess_for_show()
gen_details_pdf(filename, heading, data)
filename, heading, data = get_staff_for_show()
gen_details_pdf(filename, heading, data)
filename, heading, data = get_courses_for_show()
gen_details_pdf(filename, heading, data)

root.mainloop()