from configparser import InterpolationMissingOptionError
import re
from typing import List
import tkinter
from tkinter import ttk
import tkcalendar
import tkinter.messagebox
from mysql.connector.errors import IntegrityError
from hostel_mgmt import db, cursor
import json
from datetime import datetime
from hostel_mgmt.gen_pdf import gen_pdf
from collections import Counter
from datetime import date

from hostel_mgmt.support_queries import get_stu_for_show, get_staff_for_show, get_mess_for_show, get_room_for_show, get_block_for_show, get_courses_for_show
from hostel_mgmt.gen_details_pdf import gen_details_pdf



month_index = {"JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6, "JUL": 7, "AUG": 8, "SEPT": 9, "OCT": 10, "NOV": 11, "DEC": 12}


def insert_stu(name, dob, c_id, g_name, gender, add, r_id, c_no, g_c_no, blood_grp, is_veg):
    #Inserting into stu_details table
    cursor.execute(f"insert into stu_details (name, dob, guardian_name, gender, address, contact_no, guardian_cont_no, blood_grp) values ('{name}', '{dob}', '{g_name}', '{gender}', '{add}', {c_no}, {g_c_no}, '{blood_grp}')")
    db.commit()

    cursor.execute(f"select last_insert_id() from stu_details ")
    id = cursor.fetchone()[0]

    cursor.execute(f"select cost from room where room_id='{r_id}'")
    room_charges = cursor.fetchone()[0]
    
    cursor.execute(f"select block_id from room where room_id='{r_id}'")
    block_id = cursor.fetchone()[0]

    cursor.execute(f"select mess_id from blocks where block_id='{block_id}'")
    mess_id = cursor.fetchone()[0]

    cursor.execute(f"select mess_charges from mess where mess_id='{mess_id}'")
    mess_charges = cursor.fetchone()[0]

    #Inserting into stu_fees table
    cursor.execute(f"insert into stu_fees (stu_id, room_charges, mess_charges, add_charges) values ({id}, {room_charges}, {mess_charges}, 0)")
    db.commit()

    cursor.execute(f"select total_charge from stu_fees where stu_id='{id}'")
    total_charge = cursor.fetchone()[0]

    #Inserting into student table
    cursor.execute(f"insert into student (stu_id, course_id, room_id, is_veg) values ({id}, '{c_id}', '{r_id}', '{is_veg}')")
    db.commit()

    #Update room occupants and status
    cursor.execute(f"select occupants from room where room_id='{r_id}'")
    occupants = int(cursor.fetchone()[0])
    cursor.execute(f"select no_of_beds from room where room_id='{r_id}'")
    num_beds = int(cursor.fetchone()[0])
    cursor.execute(f"update room set occupants=occupants+1 where room_id='{r_id}'")
    if occupants+1 == num_beds:
        cursor.execute(f"update room set status='occupied' where room_id='{r_id}'")

    #Update block status
    cursor.execute(f"update blocks set vacant_beds=vacant_beds-1 where block_id='{block_id}'")
    cursor.execute(f"select vacant_beds from blocks where block_id='{block_id}'")
    vacancy = int(cursor.fetchone()[0])
    if vacancy == 0:
        cursor.execute(f"update blocks set status='occupied' where block_id='{block_id}'") 

    db.commit()

    filename, heading, data = get_stu_for_show()
    gen_details_pdf(filename, heading, data)
    filename, heading, data = get_room_for_show()
    gen_details_pdf(filename, heading, data)
    filename, heading, data = get_block_for_show()
    gen_details_pdf(filename, heading, data)



def change_stu_details(id, name, g_name, add, c_no, g_c_no, is_veg):
    #Updating student details
    cursor.execute(f"update stu_details set name='{name}', guardian_name='{g_name}', address='{add}', contact_no={c_no}, guardian_cont_no={g_c_no} where stu_id={id}")
    cursor.execute(f"update student set is_veg='{is_veg}'")
    db.commit()

    filename, heading, data = get_stu_for_show()
    gen_details_pdf(filename, heading, data)



def change_room(stu_id, new_b_id, new_r_id):
    cursor.execute(f"select cost from room where room_id='{new_r_id}'")
    room_charges = cursor.fetchone()[0]

    cursor.execute(f"select mess_id from blocks where block_id='{new_b_id}'")
    mess_id = cursor.fetchone()[0]

    cursor.execute(f"select mess_charges from mess where mess_id='{mess_id}'")
    mess_charges = cursor.fetchone()[0]

    cursor.execute(f"select room_id from student where stu_id={stu_id}")
    old_r_id = cursor.fetchone()[0]

    cursor.execute(f"select block_id from room where room_id='{old_r_id}'")
    old_b_id = cursor.fetchone()[0]

    #Change room
    cursor.execute(f"update student set room_id='{new_r_id}' where stu_id={stu_id}")
    cursor.execute(f"update stu_fees set room_charges={room_charges}, mess_charges={mess_charges} where stu_id={stu_id}")

    #Update room occupants and status
    cursor.execute(f"select occupants from room where room_id='{new_r_id}'")
    occupants = int(cursor.fetchone()[0])
    cursor.execute(f"select no_of_beds from room where room_id='{new_r_id}'")
    num_beds = int(cursor.fetchone()[0])
    cursor.execute(f"update room set occupants=occupants+1 where room_id='{new_r_id}'")
    if occupants+1 == num_beds:
        cursor.execute(f"update room set status='occupied' where room_id='{new_r_id}'")

    #Update block status
    cursor.execute(f"update blocks set vacant_beds=vacant_beds-1 where block_id='{new_b_id}'")
    db.commit()
    cursor.execute(f"select vacant_beds from blocks where block_id='{new_b_id}'")
    vacancy = int(cursor.fetchone()[0])
    if vacancy == 0:
        cursor.execute(f"update blocks set status='occupied' where block_id='{new_b_id}'")

    #Update old room/block details
    cursor.execute(f"update room set occupants=occupants-1, status='vacant' where room_id='{old_r_id}'")
    cursor.execute(f"update blocks set vacant_beds=vacant_beds+1, status='vacant' where block_id='{old_b_id}'")

    db.commit()

    filename, heading, data = get_stu_for_show()
    gen_details_pdf(filename, heading, data)
    filename, heading, data = get_block_for_show()
    gen_details_pdf(filename, heading, data)
    filename, heading, data = get_room_for_show()
    gen_details_pdf(filename, heading, data)



def insert_block(id, type, w_id, gender, mess_id, num_beds, num_single, num_double, num_tripple, btn_window, func):
    #Creating blocks
    try:
        num_rooms = num_single + num_double + num_tripple
        num_beds = num_single + (num_double*2) + (num_tripple*3)
        cursor.execute(f"insert into blocks values ('{id}', '{type}', '{w_id}', '{gender}', {num_rooms}, {num_beds},'{mess_id}', {num_beds}, 'vacant')")
        db.commit()
        tkinter.messagebox.showinfo("RSGH - RMD", f"Block added successfully!\nBlock ID: {id}", parent=btn_window)
        btn_window.destroy()
        func()
    except IntegrityError:
        tkinter.messagebox.showerror("RSGH - RMD", f"Block {id} already exists!", parent=btn_window)
        return

    if type == "NAC":
        cost_single = 3000
        cost_double = 2500
        cost_tripple = 2000
    elif type == "AC":
        cost_single = 4000
        cost_double = 3500
        cost_tripple = 3000

    #Creating rooms
    for num in range(1, num_single+1):
        cursor.execute(f"insert into room values ('{id}{str(num).zfill(3)}', '{id}', '{type}', {float(cost_single)}, 1, 0, 'vacant')")
    for num in range(num_single+1, num_single+num_double+1):
        cursor.execute(f"insert into room values ('{id}{str(num).zfill(3)}', '{id}', '{type}', {float(cost_double)}, 2, 0, 'vacant')")
    for num in range(num_single+num_double+1, num_single+num_double+num_tripple+1):
        cursor.execute(f"insert into room values ('{id}{str(num).zfill(3)}', '{id}', '{type}', {float(cost_tripple)}, 3, 0, 'vacant')")

    db.commit()

    filename, heading, data = get_block_for_show()
    gen_details_pdf(filename, heading, data)
    filename, heading, data = get_room_for_show()
    gen_details_pdf(filename, heading, data)



def extend_block(bid, type, size, num_of_rooms):
    cursor.execute(f"select room_id from room where block_id='{bid}'")
    n = int(cursor.fetchall()[-1][0][2:])
    
    cursor.execute(f"select block_type from blocks where block_id='{bid}'")
    type = cursor.fetchone()[0]

    if type == "NAC":
        cost_single = 3000
        cost_double = 2500
        cost_tripple = 2000
    elif type == "AC":
        cost_single = 4000
        cost_double = 3500
        cost_tripple = 3000

    if size.lower() == 'single':
        beds = 1
        cost = cost_single
    elif size.lower() == 'double':
        beds = 2
        cost = cost_double
    elif size.lower() == 'triple':
        beds = 3
        cost = cost_tripple
    
    #Adding rooms
    for num in range(n+1, n+num_of_rooms+1):
        cursor.execute(f"insert into room values ('{bid}{str(num).zfill(3)}', '{bid}', '{type}', {float(cost)}, {beds}, 0, 'vacant')")
    
    cursor.execute(f"update blocks set no_of_rooms=no_of_rooms+{num_of_rooms}, no_of_beds = no_of_beds+{num_of_rooms*beds}, vacant_beds=vacant_beds+{num_of_rooms*beds}, status='vacant' where block_id='{bid}'")
    
    db.commit()

    filename, heading, data = get_block_for_show()
    gen_details_pdf(filename, heading, data)
    filename, heading, data = get_room_for_show()
    gen_details_pdf(filename, heading, data)



def change_warden(b_id, w_id):
    #Change warden
    cursor.execute(f"update blocks set warden_id='{w_id}' where block_id='{b_id}'")
    db.commit()


def insert_mess(id, btn_window, first_input, charges=2100):
    #Inserting into mess table
    try:
        cursor.execute(f"insert into mess values ('{id}', {charges})")
        db.commit()
        filename, heading, data = get_mess_for_show()
        gen_details_pdf(filename, heading, data)

        tkinter.messagebox.showinfo("RSGH - RMD", f"Mess added successfully!\nMess ID: {id}", parent=btn_window)
        for widget in btn_window.winfo_children():
            if isinstance(widget, tkinter.Entry):
                widget.delete(0,'end')
            if isinstance(widget, tkinter.Text):
                widget.delete('1.0','end')
            first_input.focus_set()
    except IntegrityError:
        tkinter.messagebox.showerror("RSGH - RMD", f'Mess {id} already exists!', parent=btn_window)
        


def insert_staff(id, name, c_no, dob, gender, is_warden, btn_window, func):
    #Adding staff
    try:
        cursor.execute(f"insert into staff values ('{id}', '{name}', {c_no}, '{gender}', '{dob}', '{is_warden}')")
        db.commit()
        filename, heading, data = get_staff_for_show()
        gen_details_pdf(filename, heading, data)

        tkinter.messagebox.showinfo("RSGH - RMD", f"Staff added successfully!\nStaff ID: {id}", parent=btn_window)
        btn_window.destroy()
        func()
    except IntegrityError:
        tkinter.messagebox.showerror("RSGH - RMD", f'Staff {id} already exists!', parent=btn_window)


def change_staff_details(id, name, c_no):
    #Changing staff details
    cursor.execute(f"update staff set name='{name}', contact_no={c_no} where staff_id='{id}'")
    db.commit()
    filename, heading, data = get_staff_for_show()
    gen_details_pdf(filename, heading, data)

def insert_course(c_id, c_name, sems, btn_window, func):
    #Adding a course
    try:
        cursor.execute(f"insert into courses values ('{c_id}', '{c_name}', {sems})")
        db.commit()
        filename, heading, data = get_courses_for_show()
        gen_details_pdf(filename, heading, data)

        tkinter.messagebox.showinfo("RSGH - RMD", f"New Course added successfully!\nCourse ID: {c_id}", parent=btn_window)
        btn_window.destroy()
        func()
    except IntegrityError:
        tkinter.messagebox.showerror("RSGH - RMD", f'Course {c_id} already exists!', parent=btn_window)


def transaction(s_id):
    cursor.execute(f"select months_due from student where stu_id={s_id}")
    month_list = json.loads(f"{cursor.fetchone()[0]}")

    #Month to be paid
    month_paid = month_list.pop(0)
    month_paid_index = month_index[month_paid]
    if len(month_list) == 0:
        month_list = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEPT", "OCT", "NOV", "DEC"]
    months_due = json.dumps(month_list)

    #Calculating Charges & Date
    cursor.execute(f"select room_charges, mess_charges, add_charges, total_charge from stu_fees where stu_id={s_id}")
    result = cursor.fetchone()
    room_charges = result[0]
    mess_charges = result[1]
    add_charges = result[2]
    total_charge = result[3]

    date = datetime.now()
    month = int(date.strftime("%m"))

    late_fee = (float(100*(abs(month-month_paid_index))) if month_paid_index<month else 0)

    fee_amount = total_charge + late_fee
    
    #Remarks to get data later during bill generation
    remarks = json.dumps({"room_charge": room_charges, "mess_charges": mess_charges, "late_fee": late_fee, "add_charges": add_charges})

    #Making transaction
    cursor.execute(f"insert into transactions (stu_id, amount, month_paid, remarks) values ({s_id}, {fee_amount}, '{month_paid}', '{remarks}')")

    cursor.execute(f"update student set months_due='{months_due}' where stu_id={s_id}")

    cursor.execute(f"update stu_fees set add_charges=0 where stu_id='{s_id}'")

    db.commit()


def give_add_charges(s_id, amount):
    cursor.execute(f"update stu_fees set add_charges=add_charges+{amount} where stu_id='{s_id}'")
    db.commit()


def gen_monthly_bill(s_id, t_id):
    #Student details
    cursor.execute(f"select name, course_id, room_id from stu_details, student where (stu_details.stu_id=student.stu_id) and student.stu_id={s_id}")
    result = cursor.fetchone()
    name = result[0]
    c_id = result[1]
    r_id = result[2]

    cursor.execute(f"select room_type from room where room_id='{r_id}'")
    r_type = cursor.fetchone()[0]

    #Fee details
    cursor.execute(f"select date_of_tran, month_paid, amount, remarks from transactions where transaction_id={t_id}")
    result = cursor.fetchone()
    t_date = result[0]
    month_paid_list = [result[1]]
    total_charge = result[2]
    remarks = json.loads(result[3])
    r_charge = remarks["room_charge"]
    m_charge = remarks["mess_charges"]
    late_fee = remarks["late_fee"]
    add_fee = remarks["add_charges"]

    gen_pdf(name, s_id, c_id, r_id, r_type, t_id, t_date, month_paid_list, r_charge, m_charge, late_fee, add_fee, total_charge)



def del_stu(s_id, btn_window):
    cursor.execute(f"select room_id from student where stu_id={s_id}")
    r_id = cursor.fetchone()[0]
    cursor.execute(f"select block_id from room where room_id='{r_id}'")
    b_id = cursor.fetchone()[0]

    #Update block status
    cursor.execute(f"select status from blocks where block_id='{b_id}'")
    status = cursor.fetchone()[0]
    if status == "occupied":
        cursor.execute(f"update blocks set status='vacant' where block_id='{b_id}'")
    cursor.execute(f"update blocks set vacant_beds=vacant_beds+1 where block_id='{b_id}'")

    #Update room_status
    cursor.execute(f"select status from room where room_id='{r_id}'")
    status = cursor.fetchone()[0]
    if status == "occupied":
        cursor.execute(f"update room set status='vacant' where room_id='{r_id}'")
    cursor.execute(f"update room set occupants=occupants-1 where room_id='{r_id}'")

    #Removing student details
    cursor.execute(f"delete from student where stu_id={s_id}")
    cursor.execute(f"delete from stu_fees where stu_id={s_id}")
    cursor.execute(f"delete from stu_details where stu_id={s_id}")

    db.commit()

    filename, heading, data = get_stu_for_show()
    gen_details_pdf(filename, heading, data)
    filename, heading, data = get_room_for_show()
    gen_details_pdf(filename, heading, data)
    filename, heading, data = get_block_for_show()
    gen_details_pdf(filename, heading, data)

    tkinter.messagebox.showinfo(f"RSGH - RMD", f"Student {s_id} has been successfully removed!", parent=btn_window)


def del_staff(id, btn_window):
    cursor.execute(f"select warden_id from blocks")
    warden_list = []
    warden_res = cursor.fetchall()
    for i in range(len(warden_res)):
        warden_list.append(warden_res[i][0])
    if id in warden_list:
        cursor.execute(f"select block_id from blocks where warden_id='{id}'")
        res = cursor.fetchall()
        if len(res)==1:
            tkinter.messagebox.showerror("RSGH - RMD", f"Staff {id} has been assigned as warden of block {res[0][0]}.\nPlease change the warden of the mentioned block before attempting deletion!", parent=btn_window) #Assigned as warden
        else:
            block_list = []
            for i in range(len(res)):
                block_list.append(res[i][0])
            tkinter.messagebox.showerror("RSGH - RMD", f"Staff {id} has been assigned as warden of blocks {block_list}.\nPlease change the warden of the mentioned blocks before attempting deletion!", parent=btn_window)
    else:
        cursor.execute(f"delete from staff where staff_id='{id}'")
        db.commit()
        filename, heading, data = get_staff_for_show()
        gen_details_pdf(filename, heading, data)
        filename, heading, data = get_staff_for_show()
        gen_details_pdf(filename, heading, data)

        tkinter.messagebox.showinfo(f"RSGH - RMD", f"Staff {id} has been successfully removed!", parent=btn_window)

def del_block(id, btn_window):
    cursor.execute(f"select sum(occupants) from room where block_id='{id}'")
    occupants = cursor.fetchone()[0]
    if occupants!=0:
        tkinter.messagebox.showerror('RSGH - RMD', f'Block {id} is occupied. Please empty block before deletion!', parent=btn_window)
    else:
        cursor.execute(f"delete from room where block_id='{id}'")
        cursor.execute(f"delete from blocks where block_id='{id}'")
        db.commit()
        filename, heading, data = get_block_for_show()
        gen_details_pdf(filename, heading, data)
        filename, heading, data = get_room_for_show()
        gen_details_pdf(filename, heading, data)
        tkinter.messagebox.showinfo(f"RSGH - RMD", f"Block {id} has been successfully removed!", parent=btn_window)