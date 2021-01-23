import os
import tkinter
from tkinter.constants import DISABLED
import tkinter.messagebox
from tkinter import ttk
from datetime import date
from typing import ContextManager
from hostel_mgmt import root
from hostel_mgmt.design import center_frame
from hostel_mgmt.center_frame import home_text
from hostel_mgmt.left_frame_func import btn_list
from tkcalendar import DateEntry
from hostel_mgmt.models import *
from hostel_mgmt.support_queries import *
import sys

def enable_widget(widget):
    widget['state'] = 'readonly'
    
def on_enter(btn):
    btn['bg'] = "bisque"

def on_leave(btn):
    btn['bg'] = "bisque3"


def btn_exit(btn_window):
        btn_window.destroy()


def ref():
    for widget in root.winfo_children():
        if isinstance(widget, tkinter.Toplevel):
            widget.destroy()
    for btn in btn_list:
        btn.place_forget()


def add_stu():
    def pass_stu():
        c_id = courseid_input.get()
        name = f"{firstname_input.get()} {lastname_input.get()}"
        dob = f"{dob_input.get()[6:]}-{dob_input.get()[3:5]}-{dob_input.get()[:2]}"
        gender = gender_input.get()
        blood_grp = bgrp_input.get()
        c_no = contact_input.get()
        r_id = roomid_input.get()
        is_veg = isveg_input.get()
        add = address_input.get('1.0', 'end-1c')
        g_name = guarname_input.get()
        g_c_no = guarcont_input.get()
        values = [c_id, name, dob, gender, blood_grp, c_no, r_id, is_veg, add, g_name, g_c_no]
        if "" in values:
            tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
        else:
            insert_stu(name, dob, c_id, g_name, gender, add, r_id, c_no, g_c_no, blood_grp, is_veg)
            bid = get_last_stu_id()
            r_list = show_vacant_rooms()
            roomid_input['values'] = r_list
            tkinter.messagebox.showinfo("RSGH - RMD", f"New Student added successfully!\nStudent ID: {bid}\nStudent Name: {name}", parent=btn_window)
            btn_window.destroy()
            add_stu()
    
    def update_room_list():
        gender = gender_input.get()
        r_list = get_room_by_cat(gender)
        roomid_input['values'] = r_list
        roomid_input['state'] = 'readonly'

    btn_window = tkinter.Toplevel(root)
    btn_window.attributes("-topmost", "true")
    btn_window.resizable(False, False)
    btn_window.focus_set()
    btn_window.title("Add Student")
    windowWidth = 800
    windowHeight = int(root.winfo_screenheight())
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    btn_window.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")
    btn_window.configure(bg="bisque3")
    btn_window.grab_set()

    head = tkinter.Label(btn_window, text="Add Student Form", font=('Courier New', 20, 'bold'), bg="bisque3")
    head.place(x=260, y=30)
    btn_window.update()
    pos_x = int((btn_window.winfo_width()/2)-(head.winfo_width()/2))
    pos_y = int((btn_window.winfo_height()/2)-(head.winfo_height()/2))/8
    head['fg'] = "black"
    head.place(x=pos_x, y=pos_y)
    btn_window.update()
    
    c_list = show_courses()
    courseid_label = tkinter.Label(btn_window, text="Course ID :", font=('Courier New', 15), bg="bisque3")
    courseid_input = ttk.Combobox(btn_window, width=10, font=('Courier New', 15), values=c_list, state='readonly')
    
    firstname_label = tkinter.Label(btn_window, text="First Name :", font=('Courier New', 15), bg="bisque3")
    firstname_input = tkinter.Entry(btn_window, width=10,  font=('Courier New', 15))

    lastname_label = tkinter.Label(btn_window, text="Last Name :", font=('Courier New', 15), bg="bisque3")
    lastname_input = tkinter.Entry(btn_window, width=11,  font=('Courier New', 15))
    
    dob_label = tkinter.Label(btn_window, text="Birth Date:", font=('Courier New', 15), bg="bisque3")
    dob_input = DateEntry(btn_window, locale='en_US', date_pattern='dd/MM/yyyy', font=('Courier New', 15), width=9, state='readonly')

    gender_label = tkinter.Label(btn_window, text="Gender:", font=('Courier New', 15), bg="bisque3")
    gender_input = ttk.Combobox(btn_window, width = 10, font=('Courier New', 15), values=['Male', 'Female'], state='readonly')
    
    bgrp_label = tkinter.Label(btn_window, text="Blood Group:", font=('Courier New', 15), bg="bisque3")
    bgrp_input = ttk.Combobox(btn_window, width=8, font=('Courier New', 15), values=['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'], state='readonly')

    contact_label = tkinter.Label(btn_window, text="Contact:", font=('Courier New', 15), bg="bisque3")
    contact_input = tkinter.Entry(btn_window, width=11,  font=('Courier New', 15))
    
    roomid_label = tkinter.Label(btn_window, text="Room ID :", font=('Courier New', 15), bg="bisque3")
    roomid_input = ttk.Combobox(btn_window, width=8, font=('Courier New', 15), state=DISABLED)

    isveg_label = tkinter.Label(btn_window, text="Is Veg?", font=('Courier New', 15), bg="bisque3")
    isveg_input = ttk.Combobox(btn_window, width=10, font=('Courier New', 15), values=['Yes', 'No'], state='readonly')
    
    address_label = tkinter.Label(btn_window, text="Address :", font=('Courier New', 15), bg="bisque3")
    address_input = tkinter.Text(btn_window, width=35,  font=('Courier New', 15), height=3)
    
    tkinter.Label(btn_window, text="----------Guardian Details----------", font=('Courier New', 20), bg="bisque3").place(x=102, y=410)
    
    guarname_label = tkinter.Label(btn_window, text="Guardian Name:", font=('Courier New', 15), bg="bisque3")
    guarname_input = tkinter.Entry(btn_window, width=33,  font=('Courier New', 15))
    
    guarcont_label = tkinter.Label(btn_window, text="Contact:", font=('Courier New', 15), bg="bisque3")
    guarcont_input = tkinter.Entry(btn_window, width=11,  font=('Courier New', 15))
    
    add_button = tkinter.Button(btn_window, text="Add Student", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: pass_stu())
    exit_button = tkinter.Button(btn_window, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window))

    courseid_label.place(x=100, y=110)
    courseid_input.place(x=255, y=110)
    
    firstname_label.place(x=100, y=150)
    firstname_input.place(x=255, y=150)
    lastname_label.place(x=400, y=150)
    lastname_input.place(x=545, y=150)
    
    dob_label.place(x=100, y=190)
    dob_input.place(x=255, y=190)
    gender_label.place(x=400, y=190)
    gender_input.place(x=545, y=190)
    
    bgrp_label.place(x=100, y=230)
    bgrp_input.place(x=255, y=230)
    contact_label.place(x=400, y=230)
    contact_input.place(x=545, y=230)
    
    roomid_label.place(x=100, y=270)
    roomid_input.place(x=255, y=270)
    isveg_label.place(x=400, y=270)
    isveg_input.place(x=545, y=270)
    
    address_label.place(x=100, y=310)
    address_input.place(x=255, y=310)
    
    guarname_label.place(x=100, y=480)
    guarname_input.place(x=285, y=480)
    
    guarcont_label.place(x=100, y=520)
    guarcont_input.place(x=285, y=520)
    
    
    add_button.place(x=300, y=620)
    exit_button.place(x=440, y=620)

    btn_window.bind('<F5>', lambda event: ref())
    gender_input.bind("<<ComboboxSelected>>", lambda event: update_room_list())


def edit_stu():
    def pass_edit_stu(sid, firstname_input, lastname_input, g_name_input, add_input, c_no_input, g_c_no_input, is_veg_input):
        name = f"{firstname_input.get()} {lastname_input.get()}"
        g_name = g_name_input.get()
        add = add_input.get("1.0", "end-1c")
        c_no = c_no_input.get()
        g_c_no = g_c_no_input.get()
        is_veg = is_veg_input.get()
        values = [name, g_name, add, c_no, g_c_no, is_veg]
        if "" in values:
            tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
        else:
            change_stu_details(sid, name, g_name, add, c_no, g_c_no, is_veg)

            tkinter.messagebox.showinfo("RSGH - RMD", f"Student details edited successfully!\nStudent ID: {sid}", parent=btn_window)
            btn_window.destroy()
            edit_stu()


    def con():
        sid = sid_input.get()
        values = [sid]
        if "" in values:
            tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
        else:
            sid_label.place_forget()
            sid_input.place_forget()
            con_button.place_forget()
            exit_button1.place_forget()
            windowWidth = 800
            windowHeight = int(root.winfo_screenheight())
            positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
            positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
            btn_window.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")

            
            stuid_label = tkinter.Label(btn_window, text="Student ID:", font=('Courier New', 15), bg="bisque3")
            stuid_input = tkinter.Label(btn_window, text=sid, font=('Courier New', 15), bg="bisque3")
            course_data = get_stu_course(sid)
            courseid_label = tkinter.Label(btn_window, text="Course ID :", font=('Courier New', 15), bg="bisque3")
            courseid_input = tkinter.Label(btn_window, text=course_data, font=('Courier New', 15), bg="bisque3")
            
            old_stu_name = get_stu_name(sid)
            firstname_label = tkinter.Label(btn_window, text="First Name :", font=('Courier New', 15), bg="bisque3")
            firstname_input = tkinter.Entry(btn_window, width=10,  font=('Courier New', 15))
            lastname_label = tkinter.Label(btn_window, text="Last Name :", font=('Courier New', 15), bg="bisque3")
            lastname_input = tkinter.Entry(btn_window, width=11,  font=('Courier New', 15))
            firstname_input.insert(0, old_stu_name.split()[0])
            lastname_input.insert(0, old_stu_name.split()[1])
            
            gender_data = get_stu_gender(sid)
            dob_data = get_stu_dob(sid)
            dob_label = tkinter.Label(btn_window, text="Birth Date:", font=('Courier New', 15), bg="bisque3")
            dob_input = tkinter.Label(btn_window, text=dob_data, font=('Courier New', 15), bg="bisque3")
            gender_label = tkinter.Label(btn_window, text="Gender:", font=('Courier New', 15), bg="bisque3")
            gender_input = tkinter.Label(btn_window, text=gender_data, font=('Courier New', 15), bg="bisque3")
            
            bgrp_data = get_stu_bgrp(sid)
            cont_no = get_stu_cont(sid)
            bgrp_label = tkinter.Label(btn_window, text="Blood Group:", font=('Courier New', 15), bg="bisque3")
            bgrp_input = tkinter.Label(btn_window, text=bgrp_data, font=('Courier New', 15), bg="bisque3")
            contact_label = tkinter.Label(btn_window, text="Contact:", font=('Courier New', 15), bg="bisque3")
            contact_input = tkinter.Entry(btn_window, width=11,  font=('Courier New', 15))
            contact_input.insert(0, cont_no)
            
            room_data = get_stu_room(sid)
            meal_pref = get_meal_pref(sid)
            value_list = ['Yes', 'No']
            roomid_label = tkinter.Label(btn_window, text="Room ID :", font=('Courier New', 15), bg="bisque3")
            roomid_input = tkinter.Label(btn_window, text=room_data, font=('Courier New', 15), bg="bisque3")
            isveg_label = tkinter.Label(btn_window, text="Is Veg?", font=('Courier New', 15), bg="bisque3")
            isveg_input = ttk.Combobox(btn_window, width=10, font=('Courier New', 15), values=value_list, state='readonly')
            isveg_input.current(value_list.index(meal_pref))
            
            stu_add = get_stu_address(sid)
            address_label = tkinter.Label(btn_window, text="Address :", font=('Courier New', 15), bg="bisque3")
            address_input = tkinter.Text(btn_window, width=35,  font=('Courier New', 15), height=3)
            address_input.insert(tkinter.END, stu_add)
            
            tkinter.Label(btn_window, text="----------Guardian Details----------", font=('Courier New', 20), bg="bisque3").place(x=102, y=410)
            
            guar_name = get_guar_name(sid)
            guarname_label = tkinter.Label(btn_window, text="Guardian Name:", font=('Courier New', 15), bg="bisque3")
            guarname_input = tkinter.Entry(btn_window, width=33,  font=('Courier New', 15))
            guarname_input.insert(0, guar_name)
            
            guar_cont = get_guar_cont(sid)
            guarcont_label = tkinter.Label(btn_window, text="Contact:", font=('Courier New', 15), bg="bisque3")
            guarcont_input = tkinter.Entry(btn_window, width=11,  font=('Courier New', 15))
            guarcont_input.insert(0, guar_cont)
            
            add_button = tkinter.Button(btn_window, text="Save Changes", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: pass_edit_stu(sid, firstname_input, lastname_input, guarname_input, address_input, contact_input, guarcont_input, isveg_input))
            exit_button = tkinter.Button(btn_window, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window))

            stuid_label.place(x=100, y=110)
            stuid_input.place(x=255, y=110)
            courseid_label.place(x=400, y=110)
            courseid_input.place(x=545, y=110)
            
            firstname_label.place(x=100, y=150)
            firstname_input.place(x=255, y=150)
            lastname_label.place(x=400, y=150)
            lastname_input.place(x=545, y=150)
            
            dob_label.place(x=100, y=190)
            dob_input.place(x=255, y=190)
            gender_label.place(x=400, y=190)
            gender_input.place(x=545, y=190)
            
            bgrp_label.place(x=100, y=230)
            bgrp_input.place(x=255, y=230)
            contact_label.place(x=400, y=230)
            contact_input.place(x=545, y=230)
            
            roomid_label.place(x=100, y=270)
            roomid_input.place(x=255, y=270)
            isveg_label.place(x=400, y=270)
            isveg_input.place(x=545, y=270)
            
            address_label.place(x=100, y=310)
            address_input.place(x=255, y=310)
            
            guarname_label.place(x=100, y=480)
            guarname_input.place(x=285, y=480)
            
            guarcont_label.place(x=100, y=520)
            guarcont_input.place(x=285, y=520)
            
            
            add_button.place(x=300, y=620)
            exit_button.place(x=440, y=620)

            btn_window.bind('<F5>', lambda event: ref())


    btn_window = tkinter.Toplevel(root)
    btn_window.attributes("-topmost", "true")
    btn_window.focus_set()
    btn_window.title("Edit Student")
    btn_window.resizable(False, False)
    windowWidth = 800
    windowHeight = int(root.winfo_screenheight())-400
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    btn_window.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")
    btn_window.configure(bg="bisque3")
    btn_window.grab_set()

    s_id_list = show_all_stu()
    head = tkinter.Label(btn_window, text="Edit Student Form", font=('Courier New', 20, 'bold'), bg="bisque3")
    head.place(x=260, y=30)
    btn_window.update()
    pos_x = int((btn_window.winfo_width()/2)-(head.winfo_width()/2))
    pos_y = int((btn_window.winfo_height()/2)-(head.winfo_height()/2))/3
    head['fg'] = "black"
    head.place(x=pos_x, y=pos_y)
    btn_window.update()

    sid_label = tkinter.Label(btn_window, text="Student ID :", font=('Courier New', 15), bg="bisque3")
    sid_input = ttk.Combobox(btn_window, width=10, font=('Courier New', 15), values=s_id_list, state='readonly')
    sid_label.place(x=250, y=165)
    sid_input.place(x=405, y=165)

    con_button = tkinter.Button(btn_window, text="Continue", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command= con)
    exit_button1 = tkinter.Button(btn_window, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window))

    con_button.place(x=300, y=290)
    exit_button1.place(x=440, y=290)

    btn_window.bind('<F5>', lambda event: ref())


def change_rooms():
    def pass_change_rooms(stu_id, new_b_id_input, new_r_id_input):
        new_b_id = new_b_id_input.get()
        new_r_id = new_r_id_input.get()
        values = [new_b_id, new_r_id]
        if "" in values:
            tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
        else:
            change_room(stu_id, new_b_id, new_r_id)
            tkinter.messagebox.showinfo("RSGH - RMD", f"Room(s) changed successfully!\nNew room ID: {new_r_id}", parent=btn_window)
            btn_window.destroy()
            change_rooms()

    def con():

        sid = sid_input.get()
        bid = new_blockid_input.get()
        values = [sid, bid]
        if "" in values:
            tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
        else:
            con_button.place_forget()
            exit_button1.place_forget()
            sid_label.place_forget()
            sid_input.place_forget()
            new_blockid_input.place_forget()
            new_blockid_label.place_forget()
            stuid_label = tkinter.Label(btn_window, text="Student ID:", font=('Courier New', 15), bg="bisque3")
            stuid_input = tkinter.Label(btn_window, text=sid, font=('Courier New', 15), bg="bisque3")

            stu_name = get_stu_name(sid)
            stuname_label = tkinter.Label(btn_window, text="Name:", font=('Courier New', 15), bg="bisque3")
            stuname_input = tkinter.Label(btn_window, text=stu_name, font=('Courier New', 15), bg="bisque3")
            
            old_room = get_stu_room(sid)
            roomid_label = tkinter.Label(btn_window, text="Room ID :", font=('Courier New', 15), bg="bisque3")
            roomid_input = tkinter.Label(btn_window, text=old_room, font=('Courier New', 15), bg="bisque3")

            r_id_list = show_rooms_from_block(bid)
            new_roomid_label = tkinter.Label(btn_window, text="New Room ID:", font=('Courier New', 15), bg="bisque3")
            new_roomid_input = ttk.Combobox(btn_window, width=10, font=('Courier New', 15), values=r_id_list, state='readonly') 

            add_button = tkinter.Button(btn_window, text="Save Changes", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: pass_change_rooms(sid, new_blockid_input, new_roomid_input))
            exit_button = tkinter.Button(btn_window, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window))

            stuid_label.place(x=100, y=110)
            stuid_input.place(x=255, y=110)
            stuname_label.place(x=400, y=110)
            stuname_input.place(x=545, y=110)   

            roomid_label.place(x=100, y=150)
            roomid_input.place(x=255, y=150)

            new_roomid_label.place(x=400, y=150)
            new_roomid_input.place(x=550, y=150)

            add_button.place(x=280, y=290)
            exit_button.place(x=440, y=290)

            btn_window.bind('<F5>', lambda event: ref())
        

    btn_window = tkinter.Toplevel(root)
    btn_window.attributes("-topmost", "true")
    btn_window.resizable(False, False)
    btn_window.focus_set()
    btn_window.title("Change Room")
    windowWidth = 800
    windowHeight = int(root.winfo_screenheight())-400
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    btn_window.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")
    btn_window.configure(bg="bisque3")
    btn_window.grab_set()

    s_id_list = show_all_stu()
    head = tkinter.Label(btn_window, text="Change Room Form", font=('Courier New', 20, 'bold'), bg="bisque3")
    head.place(x=260, y=30)
    btn_window.update()
    pos_x = int((btn_window.winfo_width()/2)-(head.winfo_width()/2))
    pos_y = int((btn_window.winfo_height()/2)-(head.winfo_height()/2))/3
    head['fg'] = "black"
    head.place(x=pos_x, y=pos_y)
    btn_window.update()
    sid_label = tkinter.Label(btn_window, text="Student ID :", font=('Courier New', 15), bg="bisque3")
    sid_input = ttk.Combobox(btn_window, width=10, font=('Courier New', 15), values=s_id_list, state='readonly')

    b_id_list = show_all_blocks()
    new_blockid_label = tkinter.Label(btn_window, text="New Block ID:", font=('Courier New', 15), bg="bisque3")
    new_blockid_input = ttk.Combobox(btn_window, width=10, font=('Courier New', 15), values=b_id_list, state=DISABLED)

    sid_label.place(x=250, y=145)
    sid_input.place(x=405, y=145)

    new_blockid_label.place(x=245, y=180)
    new_blockid_input.place(x=410, y=180)

    con_button = tkinter.Button(btn_window, text="Continue", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command= con)
    exit_button1 = tkinter.Button(btn_window, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window))

    con_button.place(x=300, y=290)
    exit_button1.place(x=440, y=290)

    btn_window.bind('<F5>', lambda event: ref())
    sid_input.bind("<<ComboboxSelected>>", lambda event: enable_widget(new_blockid_input))

def display_stu():
    def sing_disp():
        def con():
            sid = sid_input.get()
            values = [sid]
            if "" in values:
                tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
            else:
                sid_label.place_forget()
                sid_input.place_forget()
                con_button.place_forget()
                exit_button1.place_forget()
                windowWidth = 800
                windowHeight = int(root.winfo_screenheight())
                positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
                positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
                btn_window1.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")

                
                stuid_label = tkinter.Label(btn_window1, text="Student ID:", font=('Courier New', 15), bg="bisque3")
                stuid_input = tkinter.Label(btn_window1, text=sid, font=('Courier New', 15), bg="bisque3")
                course_data = get_stu_course(sid)
                courseid_label = tkinter.Label(btn_window1, text="Course ID :", font=('Courier New', 15), bg="bisque3")
                courseid_input = tkinter.Label(btn_window1, text=course_data, font=('Courier New', 15), bg="bisque3")
                
                old_stu_name = get_stu_name(sid)
                firstname_label = tkinter.Label(btn_window1, text="First Name :", font=('Courier New', 15), bg="bisque3")
                firstname_input = tkinter.Label(btn_window1, text=old_stu_name.split()[0], font=('Courier New', 15), bg="bisque3")
                lastname_label = tkinter.Label(btn_window1, text="Last Name :", font=('Courier New', 15), bg="bisque3")
                lastname_input = tkinter.Label(btn_window1, text=old_stu_name.split()[1], font=('Courier New', 15), bg="bisque3")
                
                gender_data = get_stu_gender(sid)
                dob_data = get_stu_dob(sid)
                dob_label = tkinter.Label(btn_window1, text="Birth Date:", font=('Courier New', 15), bg="bisque3")
                dob_input = tkinter.Label(btn_window1, text=dob_data, font=('Courier New', 15), bg="bisque3")
                gender_label = tkinter.Label(btn_window1, text="Gender:", font=('Courier New', 15), bg="bisque3")
                gender_input = tkinter.Label(btn_window1, text=gender_data, font=('Courier New', 15), bg="bisque3")
                
                bgrp_data = get_stu_bgrp(sid)
                cont_no = get_stu_cont(sid)
                bgrp_label = tkinter.Label(btn_window1, text="Blood Group:", font=('Courier New', 15), bg="bisque3")
                bgrp_input = tkinter.Label(btn_window1, text=bgrp_data, font=('Courier New', 15), bg="bisque3")
                contact_label = tkinter.Label(btn_window1, text="Contact:", font=('Courier New', 15), bg="bisque3")
                contact_input = tkinter.Label(btn_window1, text=cont_no, font=('Courier New', 15), bg="bisque3")
                
                room_data = get_stu_room(sid)
                meal_pref = get_meal_pref(sid)
                value_list = ['Yes', 'No']
                roomid_label = tkinter.Label(btn_window1, text="Room ID :", font=('Courier New', 15), bg="bisque3")
                roomid_input = tkinter.Label(btn_window1, text=room_data, font=('Courier New', 15), bg="bisque3")
                isveg_label = tkinter.Label(btn_window1, text="Is Veg?", font=('Courier New', 15), bg="bisque3")
                isveg_input = tkinter.Label(btn_window1, text=meal_pref, font=('Courier New', 15), bg="bisque3")
                
                stu_add = get_stu_address(sid)
                address_label = tkinter.Label(btn_window1, text="Address :", font=('Courier New', 15), bg="bisque3")
                address_input = tkinter.Label(btn_window1, text=stu_add, wraplength=500, font=('Courier New', 15), bg="bisque3")
                
                tkinter.Label(btn_window1, text="----------Guardian Details----------", font=('Courier New', 20), bg="bisque3").place(x=102, y=410)
                
                guar_name = get_guar_name(sid)
                guarname_label = tkinter.Label(btn_window1, text="Guardian Name:", font=('Courier New', 15), bg="bisque3")
                guarname_input = tkinter.Label(btn_window1, text=guar_name, font=('Courier New', 15), bg="bisque3")
                
                guar_cont = get_guar_cont(sid)
                guarcont_label = tkinter.Label(btn_window1, text="Contact:", font=('Courier New', 15), bg="bisque3")
                guarcont_input = tkinter.Label(btn_window1, text=guar_cont, font=('Courier New', 15), bg="bisque3")
                
                exit_button = tkinter.Button(btn_window1, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window1))

                stuid_label.place(x=100, y=110)
                stuid_input.place(x=255, y=110)
                courseid_label.place(x=400, y=110)
                courseid_input.place(x=545, y=110)
                
                firstname_label.place(x=100, y=150)
                firstname_input.place(x=255, y=150)
                lastname_label.place(x=400, y=150)
                lastname_input.place(x=545, y=150)
                
                dob_label.place(x=100, y=190)
                dob_input.place(x=255, y=190)
                gender_label.place(x=400, y=190)
                gender_input.place(x=545, y=190)
                
                bgrp_label.place(x=100, y=230)
                bgrp_input.place(x=255, y=230)
                contact_label.place(x=400, y=230)
                contact_input.place(x=545, y=230)
                
                roomid_label.place(x=100, y=270)
                roomid_input.place(x=255, y=270)
                isveg_label.place(x=400, y=270)
                isveg_input.place(x=545, y=270)
                
                address_label.place(x=100, y=310)
                address_input.place(x=255, y=310)
                
                guarname_label.place(x=100, y=480)
                guarname_input.place(x=285, y=480)
                
                guarcont_label.place(x=100, y=520)
                guarcont_input.place(x=285, y=520)
                
                exit_button.place(x=380, y=620)
        btn_window1 = tkinter.Toplevel(root)
        btn_window1.attributes("-topmost", "true")
        btn_window1.resizable(False, False)
        btn_window1.focus_set()
        btn_window1.title("Display Individual Student Details")
        windowWidth = 800
        windowHeight = int(root.winfo_screenheight())-400
        positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
        btn_window1.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")
        btn_window1.configure(bg="bisque3")
        btn_window1.grab_set()

        s_id_list = show_all_stu()
        head = tkinter.Label(btn_window1, text="Display Individual Student Details", font=('Courier New', 20, 'bold'), bg="bisque3")
        head.place(x=260, y=30)
        btn_window1.update()
        pos_x = int((btn_window1.winfo_width()/2)-(head.winfo_width()/2))
        pos_y = int((btn_window1.winfo_height()/2)-(head.winfo_height()/2))/3
        head['fg'] = "black"
        head.place(x=pos_x, y=pos_y)
        btn_window1.update()

        sid_label = tkinter.Label(btn_window1, text="Student ID :", font=('Courier New', 15), bg="bisque3")
        sid_input = ttk.Combobox(btn_window1, width=10, font=('Courier New', 15), values=s_id_list, state='readonly')
        sid_label.place(x=250, y=165)
        sid_input.place(x=405, y=165)

        con_button = tkinter.Button(btn_window1, text="Continue", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command = lambda: con())
        exit_button1 = tkinter.Button(btn_window1, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window1))

        con_button.place(x=300, y=290)
        exit_button1.place(x=440, y=290)

        btn_window1.bind('<Return>', lambda event: con())
        btn_window1.bind('<Escape>', lambda event: btn_window.destroy())
        btn_window1.bind('<F5>', lambda event: ref())

    def all_disp_stu():
        try:
            path = os.path.join(sys.path[0], "details/")
            filename = 'stu_details.pdf'
            os.startfile(f"{path}{filename}")
        except OSError:
            tkinter.messagebox.showerror("RSGH - RMD", "The file/directory has been moved or does not exist! Please restart the application to fix this error!")
        



    btn_window = tkinter.Toplevel(root)
    btn_window.focus_set()
    btn_window.title("Display Student Details")
    btn_window.resizable(False, False)
    windowWidth = 800
    windowHeight = int(root.winfo_screenheight())-400
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    btn_window.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")
    btn_window.configure(bg="bisque3")
    btn_window.grab_set()

    head = tkinter.Label(btn_window, text="Display Student Details", font=('Courier New', 20, 'bold'), bg="bisque3")
    head.place(x=260, y=30)
    btn_window.update()
    pos_x = int((btn_window.winfo_width()/2)-(head.winfo_width()/2))
    pos_y = int((btn_window.winfo_height()/2)-(head.winfo_height()/2))/3
    head['fg'] = "black"
    head.place(x=pos_x, y=pos_y)
    btn_window.update()

    all_disp_button = tkinter.Button(btn_window, text="Display All Details", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=all_disp_stu)
    sing_disp_button = tkinter.Button(btn_window, text="Display Individual Student Details", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=sing_disp)


    all_disp_button.place(x=300, y=290)
    sing_disp_button.place(x=250, y=200)
    btn_window.update()
    pos_x_sdb = int((btn_window.winfo_width()/2)-(sing_disp_button.winfo_width()/2))
    pos_y_sdb = int((btn_window.winfo_height()/2)-(sing_disp_button.winfo_height()/2))
    pos_x_adb = int((btn_window.winfo_width()/2)-(all_disp_button.winfo_width()/2))
    pos_y_adb = int((btn_window.winfo_height()/2)-(all_disp_button.winfo_height()/2))+50
    sing_disp_button['fg'] = "black"
    all_disp_button['fg'] = "black"
    sing_disp_button.place(x=pos_x_sdb, y=pos_y_sdb)
    all_disp_button.place(x=pos_x_adb, y=pos_y_adb)
    btn_window.update()



def add_block():

    def pass_block():
        bid = blockid_input.get()
        type = blocktype_input.get()
        w_id = wardenid_input.get()
        gender = gender_input.get()
        mess_id = messid_input.get()
        num_single = singroom_input.get()
        num_double = doubroom_input.get()
        num_tripple = triproom_input.get()
        values = [bid, type, w_id, gender, mess_id, num_single, num_double, num_tripple]
        if "" in values:
            tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
        else:
            num_single = int(num_single)
            num_double = int(num_double)
            num_tripple = int(num_tripple)
            num_beds = (num_single*1) + (num_double*2) + (num_tripple*3)
            insert_block(bid, type, w_id, gender, mess_id, num_beds, num_single, num_double, num_tripple, btn_window, add_block)
            
            

    btn_window = tkinter.Toplevel(root)
    btn_window.attributes("-topmost", "true")
    btn_window.focus_set()
    btn_window.title("Add Block")
    btn_window.resizable(False, False)
    windowWidth = 800
    windowHeight = int(root.winfo_screenheight())-200
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    btn_window.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")
    btn_window.configure(bg="bisque3")
    btn_window.grab_set()

    head = tkinter.Label(btn_window, text="Add Block Form", font=('Courier New', 20, 'bold'), bg="bisque3")
    head.place(x=260, y=30)
    btn_window.update()
    pos_x = int((btn_window.winfo_width()/2)-(head.winfo_width()/2))
    pos_y = int((btn_window.winfo_height()/2)-(head.winfo_height()/2))/6
    head['fg'] = "black"
    head.place(x=pos_x, y=pos_y)
    btn_window.update()
    
    blockid_label = tkinter.Label(btn_window, text="Block ID :", font=('Courier New', 15), bg="bisque3")
    blockid_input = tkinter.Entry(btn_window, width=10,  font=('Courier New', 15))

    blocktype_label = tkinter.Label(btn_window, text="Block Type:", font=('Courier New', 15), bg="bisque3")
    blocktype_input = ttk.Combobox(btn_window, width=10, font=('Courier New', 15), values=['AC', 'NAC'], state='readonly')
    
    warden_list = get_all_wardens()
    wardenid_label = tkinter.Label(btn_window, text="Warden ID:", font=('Courier New', 15), bg="bisque3")
    wardenid_input = ttk.Combobox(btn_window, width=8, font=('Courier New', 15), values=warden_list, state='readonly')

    gender_label = tkinter.Label(btn_window, text="Gender:", font=('Courier New', 15), bg="bisque3")
    gender_input = ttk.Combobox(btn_window, width = 10, font=('Courier New', 15), values=['Male', 'Female'], state='readonly')

    mess_id = show_all_mess()
    messid_label = tkinter.Label(btn_window, text="Mess ID:", font=('Courier New', 15), bg="bisque3")
    messid_input = ttk.Combobox(btn_window, width=8, font=('Courier New', 15), values=mess_id, state='readonly')

    tkinter.Label(btn_window, text="----------Room Details----------", font=('Courier New', 20), bg="bisque3").place(x=135, y=255)
    
    singroom_label = tkinter.Label(btn_window, text="Single Sharing:", font=('Courier New', 15), bg="bisque3")
    singroom_input = tkinter.Entry(btn_window, width=3,  font=('Courier New', 15))
    
    doubroom_label = tkinter.Label(btn_window, text="Double Sharing:", font=('Courier New', 15), bg="bisque3")
    doubroom_input = tkinter.Entry(btn_window, width=3,  font=('Courier New', 15))

    triproom_label = tkinter.Label(btn_window, text="Triple Sharing:", font=('Courier New', 15), bg="bisque3")
    triproom_input = tkinter.Entry(btn_window, width=3,  font=('Courier New', 15))
    
    add_button = tkinter.Button(btn_window, text="Add Block", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: pass_block())
    exit_button = tkinter.Button(btn_window, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window))

    blockid_label.place(x=100, y=110)
    blockid_input.place(x=255, y=110)
    blocktype_label.place(x=400, y=110)
    blocktype_input.place(x=545, y=110)
    
    wardenid_label.place(x=100, y=150)
    wardenid_input.place(x=255, y=150)

    gender_label.place(x=400, y=150)
    gender_input.place(x=545, y=150)
    
    messid_label.place(x=100, y=190)
    messid_input.place(x=255, y=190)

    singroom_label.place(x=100, y=330)
    singroom_input.place(x=300, y=330)
    
    doubroom_label.place(x=450, y=330)
    doubroom_input.place(x=650, y=330)

    triproom_label.place(x=275, y=370)
    triproom_input.place(x=475, y=370)
    
    
    add_button.place(x=300, y=450)
    exit_button.place(x=440, y=450)

    btn_window.bind('<F5>', lambda event: ref())

def edit_block():
    def pass_edit_block(bid, type, size_input, num_rooms_input):
        size = size_input.get()
        num_of_rooms = int(num_rooms_input.get())
        values = [size, num_of_rooms]
        if "" in values:
            tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
        else:
            extend_block(bid, type, size, num_of_rooms)
            tkinter.messagebox.showinfo("RSGH - RMD", f"Rooms added successfully to Block {bid}", parent=btn_window)
            btn_window.destroy()
            edit_block()

    def con():
        b_id = b_id_input.get()
        values = [b_id]
        if "" in values:
            tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
        else:
            b_id_label.place_forget()
            b_id_input.place_forget()
            con_button.place_forget()
            exit_button1.place_forget()
            block_type = get_block_type(b_id)
            blockid_label = tkinter.Label(btn_window, text="Block ID :", font=('Courier New', 15), bg="bisque3")
            blockid_input = tkinter.Label(btn_window, text=b_id, font=('Courier New', 15), bg="bisque3")

            blocktype_label = tkinter.Label(btn_window, text="Block Type:", font=('Courier New', 15), bg="bisque3")
            blocktype_input = tkinter.Label(btn_window, text=block_type, font=('Courier New', 15), bg="bisque3")

            wardenid_label = tkinter.Label(btn_window, text="Warden ID:", font=('Courier New', 15), bg="bisque3")
            w_id = get_w_id(b_id)
            wardenid_input = tkinter.Label(btn_window, text=w_id, font=('Courier New', 15), bg="bisque3")

            block_gender = get_block_gender(b_id)
            gender_label = tkinter.Label(btn_window, text="Gender:", font=('Courier New', 15), bg="bisque3")
            gender_input = tkinter.Label(btn_window, text=block_gender, font=('Courier New', 15), bg="bisque3")
            
            size_label = tkinter.Label(btn_window, text="Bed sharing:", font=('Courier New', 15), bg="bisque3")
            size_input = ttk.Combobox(btn_window, width=8, font=('Courier New', 15), values=['Single', 'Double', 'Triple'], state='readonly')
        
            num_room_label = tkinter.Label(btn_window, text="No. of rooms:", font=('Courier New', 15), bg="bisque3")
            num_room_input = tkinter.Entry(btn_window, width=3,  font=('Courier New', 15))

            add_button = tkinter.Button(btn_window, text="Save Changes", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: pass_edit_block(b_id, block_type, size_input, num_room_input))
            exit_button = tkinter.Button(btn_window, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window))

            blockid_label.place(x=100, y=110)
            blockid_input.place(x=255, y=110)
            blocktype_label.place(x=400, y=110)
            blocktype_input.place(x=545, y=110)

            wardenid_label.place(x=100, y=150)
            wardenid_input.place(x=235, y=150)

            gender_label.place(x=400, y=150)
            gender_input.place(x=545, y=150)

            size_label.place(x=100, y=190)
            size_input.place(x=265, y=190)

            num_room_label.place(x=400, y=190)
            num_room_input.place(x=565, y=190)

            add_button.place(x=280, y=290)
            exit_button.place(x=440, y=290)
        
            btn_window.bind('<F5>', lambda event: ref())


    btn_window = tkinter.Toplevel(root)
    btn_window.attributes("-topmost", "true")
    btn_window.focus_set()
    btn_window.title("Extend Block")
    btn_window.resizable(False, False)
    windowWidth = 800
    windowHeight = int(root.winfo_screenheight())-400
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    btn_window.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")
    btn_window.configure(bg="bisque3")
    btn_window.grab_set()

    b_id_list = show_all_blocks()
    head = tkinter.Label(btn_window, text="Extend Block Form", font=('Courier New', 20, 'bold'), bg="bisque3")
    head.place(x=260, y=30)
    btn_window.update()
    pos_x = int((btn_window.winfo_width()/2)-(head.winfo_width()/2))
    pos_y = int((btn_window.winfo_height()/2)-(head.winfo_height()/2))/5
    head['fg'] = "black"
    head.place(x=pos_x, y=pos_y)
    btn_window.update()

    b_id_label = tkinter.Label(btn_window, text="Block ID :", font=('Courier New', 15), bg="bisque3")
    b_id_input = ttk.Combobox(btn_window, width=10, font=('Courier New', 15), values=b_id_list, state='readonly')
    b_id_label.place(x=250, y=165)
    b_id_input.place(x=405, y=165)

    con_button = tkinter.Button(btn_window, text="Continue", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command= con)
    exit_button1 = tkinter.Button(btn_window, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window))

    con_button.place(x=300, y=290)
    exit_button1.place(x=440, y=290)

    btn_window.bind('<F5>', lambda event: ref())



def changewarden():
    def pass_change_warden(b_id, w_id_input):
        w_id = w_id_input.get()
        values = [w_id]
        if "" in values:
            tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
        else:
            change_warden(b_id, w_id)
            tkinter.messagebox.showinfo("RSGH - RMD", f"Warden changed successfully!\nNew Warden ID: {w_id}", parent=btn_window)
            btn_window.destroy()
            changewarden()


    def con():
        b_id = b_id_input.get()
        values = [b_id]
        if "" in values:
            tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
        else:
            b_id_label.place_forget()
            b_id_input.place_forget()
            con_button.place_forget()
            exit_button1.place_forget()
            wid = get_w_id(b_id)
            wardenid_label = tkinter.Label(btn_window, text="Warden ID :", font=('Courier New', 15), bg="bisque3")
            wardenid_input = tkinter.Label(btn_window, text=wid, font=('Courier New', 15), bg="bisque3")
            
            warden_id = get_updated_w_id(wid)
            newwarden_label = tkinter.Label(btn_window, text="New Warden ID:", font=('Courier New', 15), bg="bisque3")
            newwarden_input = ttk.Combobox(btn_window, width=8, font=('Courier New', 15), values=warden_id, state='readonly')

            wardenid_label.place(x=100, y=150)
            wardenid_input.place(x=255, y=150)
            newwarden_label.place(x=360, y=150)
            newwarden_input.place(x=545, y=150)

            add_button = tkinter.Button(btn_window, text="Save Changes", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: pass_change_warden(b_id, newwarden_input))
            exit_button = tkinter.Button(btn_window, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window))

            add_button.place(x=280, y=290)
            exit_button.place(x=440, y=290)

            btn_window.bind('<F5>', lambda event: ref())

    btn_window = tkinter.Toplevel(root)
    btn_window.attributes("-topmost", "true")
    btn_window.resizable(False, False)
    btn_window.focus_set()
    btn_window.title("Change Warden")
    windowWidth = 800
    windowHeight = int(root.winfo_screenheight())-400
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    btn_window.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")
    btn_window.configure(bg="bisque3")
    btn_window.grab_set()

    b_id_list = show_all_blocks()
    head = tkinter.Label(btn_window, text="Change Warden Form", font=('Courier New', 20, 'bold'), bg="bisque3")
    head.place(x=260, y=30)
    btn_window.update()
    pos_x = int((btn_window.winfo_width()/2)-(head.winfo_width()/2))
    pos_y = int((btn_window.winfo_height()/2)-(head.winfo_height()/2))/3
    head['fg'] = "black"
    head.place(x=pos_x, y=pos_y)
    btn_window.update()

    b_id_label = tkinter.Label(btn_window, text="Block ID :", font=('Courier New', 15), bg="bisque3")
    b_id_input = ttk.Combobox(btn_window, width=10, font=('Courier New', 15), values=b_id_list, state='readonly')
    b_id_label.place(x=250, y=165)
    b_id_input.place(x=405, y=165)

    con_button = tkinter.Button(btn_window, text="Continue", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command= con)
    exit_button1 = tkinter.Button(btn_window, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window))

    con_button.place(x=300, y=290)
    exit_button1.place(x=440, y=290)

    btn_window.bind('<F5>', lambda event: ref())

def display_block():
    def sing_disp_block():
        def con():
            bid = bid_input.get()
            values = [bid]
            if "" in values:
                tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
            else:
                bid_label.place_forget()
                bid_input.place_forget()
                con_button.place_forget()
                exit_button1.place_forget()
                windowWidth = 800
                windowHeight = int(root.winfo_screenheight())-200
                positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
                positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
                btn_window1.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")

                blockid_label = tkinter.Label(btn_window1, text="Block ID :", font=('Courier New', 15), bg="bisque3")
                blockid_input = tkinter.Label(btn_window1, text=bid, font=('Courier New', 15), bg="bisque3")

                type = get_block_type(bid)
                blocktype_label = tkinter.Label(btn_window1, text="Block Type:", font=('Courier New', 15), bg="bisque3")
                blocktype_input = tkinter.Label(btn_window1, text=type, font=('Courier New', 15), bg="bisque3")
                
                warden = get_block_warden(bid)
                wardenid_label = tkinter.Label(btn_window1, text="Warden ID:", font=('Courier New', 15), bg="bisque3")
                wardenid_input = tkinter.Label(btn_window1, text=warden, font=('Courier New', 15), bg="bisque3")

                gender = get_block_gender(bid)
                gender_label = tkinter.Label(btn_window1, text="Gender:", font=('Courier New', 15), bg="bisque3")
                gender_input = tkinter.Label(btn_window1, text=gender, font=('Courier New', 15), bg="bisque3")

                mess_id = get_block_mess(bid)
                messid_label = tkinter.Label(btn_window1, text="Mess ID:", font=('Courier New', 15), bg="bisque3")
                messid_input = tkinter.Label(btn_window1, text=mess_id, font=('Courier New', 15), bg="bisque3")

                section = tkinter.Label(btn_window1, text="----------Room Details----------", font=('Courier New', 20), bg="bisque3")
                section.place(x=260, y=30)
                btn_window1.update()
                pos_x = int((btn_window1.winfo_width()/2)-(section.winfo_width()/2))
                section['fg'] = "black"
                section.place(x=pos_x, y=255)
                btn_window1.update()
                
                sing_room = get_sing_room(bid)
                singroom_label = tkinter.Label(btn_window1, text="Single Sharing:", font=('Courier New', 15), bg="bisque3")
                singroom_input = tkinter.Label(btn_window1, text=sing_room, font=('Courier New', 15), bg="bisque3")
                
                doub_room = get_doub_room(bid)
                doubroom_label = tkinter.Label(btn_window1, text="Double Sharing:", font=('Courier New', 15), bg="bisque3")
                doubroom_input = tkinter.Label(btn_window1, text=doub_room, font=('Courier New', 15), bg="bisque3")

                trip_room = get_trip_room(bid)
                triproom_label = tkinter.Label(btn_window1, text="Triple Sharing:", font=('Courier New', 15), bg="bisque3")
                triproom_input = tkinter.Label(btn_window1, text=trip_room, font=('Courier New', 15), bg="bisque3")

                exit_button = tkinter.Button(btn_window1, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window1))

                blockid_label.place(x=147, y=110)
                blockid_input.place(x=302, y=110)
                blocktype_label.place(x=447, y=110)
                blocktype_input.place(x=592, y=110)
                
                wardenid_label.place(x=147, y=150)
                wardenid_input.place(x=302, y=150)

                gender_label.place(x=447, y=150)
                gender_input.place(x=592, y=150)
                
                messid_label.place(x=147, y=190)
                messid_input.place(x=302, y=190)

                singroom_label.place(x=120, y=330)
                singroom_input.place(x=320, y=330)
                
                doubroom_label.place(x=470, y=330)
                doubroom_input.place(x=670, y=330)

                triproom_label.place(x=295, y=370)
                triproom_input.place(x=495, y=370)
                
                exit_button.place(x=380, y=450)
        btn_window1 = tkinter.Toplevel(root)
        btn_window1.attributes("-topmost", "true")
        btn_window1.resizable(False, False)
        btn_window1.focus_set()
        btn_window1.title("Display Individual Block Details")
        windowWidth = 800
        windowHeight = int(root.winfo_screenheight())-400
        positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
        btn_window1.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")
        btn_window1.configure(bg="bisque3")
        btn_window1.grab_set()

        b_id_list = show_all_blocks()
        head = tkinter.Label(btn_window1, text="Display Individual Block Details", font=('Courier New', 20, 'bold'), bg="bisque3")
        head.place(x=260, y=30)
        btn_window1.update()
        pos_x = int((btn_window1.winfo_width()/2)-(head.winfo_width()/2))
        pos_y = int((btn_window1.winfo_height()/2)-(head.winfo_height()/2))/3
        head['fg'] = "black"
        head.place(x=pos_x, y=pos_y)
        btn_window1.update()

        bid_label = tkinter.Label(btn_window1, text="Block ID :", font=('Courier New', 15), bg="bisque3")
        bid_input = ttk.Combobox(btn_window1, width=10, font=('Courier New', 15), values=b_id_list, state='readonly')
        bid_label.place(x=250, y=165)
        bid_input.place(x=405, y=165)

        con_button = tkinter.Button(btn_window1, text="Continue", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command = lambda: con())
        exit_button1 = tkinter.Button(btn_window1, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window1))

        con_button.place(x=300, y=290)
        exit_button1.place(x=440, y=290)

        btn_window1.bind('<Return>', lambda event: con())
        btn_window1.bind('<Escape>', lambda event: btn_window.destroy())
        btn_window1.bind('<F5>', lambda event: ref())

    def all_disp_block():
        try:
            path = os.path.join(sys.path[0], "details/")
            filename = 'block_details.pdf'
            os.startfile(f"{path}{filename}")
        except OSError:
            tkinter.messagebox.showerror("RSGH - RMD", "The file/directory has been moved or does not exist! Please restart the application to fix this error!")

    btn_window = tkinter.Toplevel(root)
    btn_window.focus_set()
    btn_window.title("Display Block Details")
    btn_window.resizable(False, False)
    windowWidth = 800
    windowHeight = int(root.winfo_screenheight())-400
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    btn_window.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")
    btn_window.configure(bg="bisque3")
    btn_window.grab_set()

    head = tkinter.Label(btn_window, text="Display Block Details", font=('Courier New', 20, 'bold'), bg="bisque3")
    head.place(x=260, y=30)
    btn_window.update()
    pos_x = int((btn_window.winfo_width()/2)-(head.winfo_width()/2))
    pos_y = int((btn_window.winfo_height()/2)-(head.winfo_height()/2))/3
    head['fg'] = "black"
    head.place(x=pos_x, y=pos_y)
    btn_window.update()

    all_disp_button = tkinter.Button(btn_window, text="Display All Details", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=all_disp_block)
    sing_disp_button = tkinter.Button(btn_window, text="Display Individual Block Details", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=sing_disp_block)


    all_disp_button.place(x=300, y=290)
    sing_disp_button.place(x=250, y=200)
    btn_window.update()
    pos_x_sdb = int((btn_window.winfo_width()/2)-(sing_disp_button.winfo_width()/2))
    pos_y_sdb = int((btn_window.winfo_height()/2)-(sing_disp_button.winfo_height()/2))
    pos_x_adb = int((btn_window.winfo_width()/2)-(all_disp_button.winfo_width()/2))
    pos_y_adb = int((btn_window.winfo_height()/2)-(all_disp_button.winfo_height()/2))+50
    sing_disp_button['fg'] = "black"
    all_disp_button['fg'] = "black"
    sing_disp_button.place(x=pos_x_sdb, y=pos_y_sdb)
    all_disp_button.place(x=pos_x_adb, y=pos_y_adb)
    btn_window.update()

def all_disp_room():
    try:
        path = os.path.join(sys.path[0], "details/")
        filename = 'room_details.pdf'
        os.startfile(f"{path}{filename}")
    except OSError:
        tkinter.messagebox.showerror("RSGH - RMD", "The file/directory has been moved or does not exist! Please restart the application to fix this error!")

def add_mess():
    def pass_mess():
        mid = messid_input.get()
        values = [mid]
        if "" in values:
            tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
        else:
            insert_mess(mid, btn_window, messid_input)
            

    btn_window = tkinter.Toplevel(root)
    btn_window.attributes("-topmost", "true")
    btn_window.resizable(False, False)
    btn_window.focus_set()
    btn_window.title("Add Mess")
    windowWidth = 800
    windowHeight = int(root.winfo_screenheight())-400
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    btn_window.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")
    btn_window.configure(bg="bisque3")
    btn_window.grab_set()

    head = tkinter.Label(btn_window, text="Add Mess Form", font=('Courier New', 20, 'bold'), bg="bisque3")
    head.place(x=260, y=30)
    btn_window.update()
    pos_x = int((btn_window.winfo_width()/2)-(head.winfo_width()/2))
    pos_y = int((btn_window.winfo_height()/2)-(head.winfo_height()/2))/3
    head['fg'] = "black"
    head.place(x=pos_x, y=pos_y)
    btn_window.update()

    messid_label = tkinter.Label(btn_window, text="Mess ID :", font=('Courier New', 15), bg="bisque3")
    messid_input = tkinter.Entry(btn_window, width=10, font=('Courier New', 15))
    messid_label.place(x=250, y=165)
    messid_input.place(x=405, y=165)

    add_button = tkinter.Button(btn_window, text="Add Mess", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: pass_mess())
    exit_button = tkinter.Button(btn_window, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window))

    add_button.place(x=280, y=290)
    exit_button.place(x=440, y=290)
    
    btn_window.bind('<F5>', lambda event: ref())

def all_disp_mess():
    try:
        path = os.path.join(sys.path[0], "details/")
        filename = 'mess_details.pdf'
        os.startfile(f"{path}{filename}")
    except OSError:
        tkinter.messagebox.showerror("RSGH - RMD", "The file/directory has been moved or does not exist! Please restart the application to fix this error!")

def add_staff():
    def pass_add_staff():
        sid = staffid_input.get()
        is_warden = iswarden_input.get()
        name = name_input.get()
        c_no = contact_input.get()
        dob = f"{dob_input.get()[6:]}-{dob_input.get()[3:5]}-{dob_input.get()[:2]}"
        gender = gender_input.get()
        values = [sid, name, c_no, dob, gender, is_warden]
        if "" in values:
            tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
        else:
            insert_staff(sid, name, c_no, dob, gender, is_warden, btn_window, add_staff)

            

    btn_window = tkinter.Toplevel(root)
    btn_window.attributes("-topmost", "true")
    btn_window.resizable(False, False)
    btn_window.focus_set()
    btn_window.title("Add Staff")
    windowWidth = 800
    windowHeight = int(root.winfo_screenheight())-400
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    btn_window.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")
    btn_window.configure(bg="bisque3")
    btn_window.grab_set()

    head = tkinter.Label(btn_window, text="Add Staff Form", font=('Courier New', 20, 'bold'), bg="bisque3")
    head.place(x=260, y=30)
    btn_window.update()
    pos_x = int((btn_window.winfo_width()/2)-(head.winfo_width()/2))
    pos_y = int((btn_window.winfo_height()/2)-(head.winfo_height()/2))/3
    head['fg'] = "black"
    head.place(x=pos_x, y=pos_y)
    btn_window.update()

    staffid_label = tkinter.Label(btn_window, text="Staff ID :", font=('Courier New', 15), bg="bisque3")
    staffid_input = tkinter.Entry(btn_window, width=10,  font=('Courier New', 15))
    iswarden_label = tkinter.Label(btn_window, text="Is Warden?", font=('Courier New', 15), bg="bisque3")
    iswarden_input = ttk.Combobox(btn_window, width=10, font=('Courier New', 15), values=['Yes', 'No'], state='readonly')

    name_label = tkinter.Label(btn_window, text="Name:", font=('Courier New', 15), bg="bisque3")
    name_input = tkinter.Entry(btn_window, font=('Courier New', 15), width=10)

    contact_label = tkinter.Label(btn_window, text="Contact:", font=('Courier New', 15), bg="bisque3")
    contact_input = tkinter.Entry(btn_window, font=('Courier New', 15), width=10)

    dob_label = tkinter.Label(btn_window, text="Birth Date:", font=('Courier New', 15), bg="bisque3")
    dob_input = DateEntry(btn_window, locale='en_US', date_pattern='dd/MM/yyyy', font=('Courier New', 15), width=9, state='readonly')
    gender_label = tkinter.Label(btn_window, text="Gender:", font=('Courier New', 15), bg="bisque3")
    gender_input = ttk.Combobox(btn_window, width = 10, font=('Courier New', 15), values=['Male', 'Female'], state='readonly')

    add_button = tkinter.Button(btn_window, text="Add Staff", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: pass_add_staff())
    exit_button = tkinter.Button(btn_window, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window))

    staffid_label.place(x=100, y=110)
    staffid_input.place(x=255, y=110)
    iswarden_label.place(x=400, y=110)
    iswarden_input.place(x=545, y=110)
    
    name_label.place(x=100, y=150)
    name_input.place(x=255, y=150)
    contact_label.place(x=400, y=150)
    contact_input.place(x=545, y=150)
    
    dob_label.place(x=100, y=190)
    dob_input.place(x=255, y=190)
    gender_label.place(x=400, y=190)
    gender_input.place(x=545, y=190)

    add_button.place(x=280, y=290)
    exit_button.place(x=440, y=290)

    btn_window.bind('<F5>', lambda event: ref())

def edit_staff():
    def pass_edit_staff(sid, name_input, contact_input):
        name = name_input.get()
        c_no = contact_input.get()
        values = [name, c_no]
        if "" in values:
            tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
        else:
            change_staff_details(sid, name, c_no)
            tkinter.messagebox.showinfo("RSGH - RMD", f"Staff details edited successfully!\nStaff ID: {sid}", parent=btn_window)
            btn_window.destroy()
            edit_staff()

    def con():
        sid = sid_input.get()
        values = [sid]
        if "" in values:
            tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
        else:
            sid_label.place_forget()
            sid_input.place_forget()
            con_button.place_forget()
            exit_button1.place_forget()
            staffid_label = tkinter.Label(btn_window, text="Staff ID :", font=('Courier New', 15), bg="bisque3")
            staffid_input = tkinter.Label(btn_window, text=sid, font=('Courier New', 15), bg="bisque3")

            staff_name = get_staff_name(sid)
            name_label = tkinter.Label(btn_window, text="Name:", font=('Courier New', 15), bg="bisque3")
            name_input = tkinter.Entry(btn_window, font=('Courier New', 15), width=10)
            name_input.insert(0, staff_name)

            staff_contact = get_staff_cont(sid)
            contact_label = tkinter.Label(btn_window, text="Contact:", font=('Courier New', 15), bg="bisque3")
            contact_input = tkinter.Entry(btn_window, font=('Courier New', 15), width=10)
            contact_input.insert(0, staff_contact)

            staff_gender = get_staff_gender(sid)
            staff_dob = get_staff_dob(sid)
            dob_label = tkinter.Label(btn_window, text="Birth Date:", font=('Courier New', 15), bg="bisque3")
            dob_input = tkinter.Label(btn_window, text=staff_dob, font=('Courier New', 15), bg="bisque3")
            gender_label = tkinter.Label(btn_window, text="Gender:", font=('Courier New', 15), bg="bisque3")
            gender_input = tkinter.Label(btn_window, text=staff_gender, font=('Courier New', 15), bg="bisque3")

            add_button = tkinter.Button(btn_window, text="Save Changes", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: pass_edit_staff(sid, name_input, contact_input))
            exit_button = tkinter.Button(btn_window, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window))

            staffid_label.place(x=100, y=110)
            staffid_input.place(x=255, y=110)
            
            name_label.place(x=100, y=150)
            name_input.place(x=255, y=150)
            contact_label.place(x=400, y=150)
            contact_input.place(x=545, y=150)
            
            dob_label.place(x=100, y=190)
            dob_input.place(x=255, y=190)
            gender_label.place(x=400, y=190)
            gender_input.place(x=545, y=190)

            add_button.place(x=280, y=290)
            exit_button.place(x=440, y=290)

            btn_window.bind('<F5>', lambda event: ref())
        
    btn_window = tkinter.Toplevel(root)
    btn_window.attributes("-topmost", "true")
    btn_window.resizable(False, False)
    btn_window.focus_set()
    btn_window.title("Edit Staff")
    windowWidth = 800
    windowHeight = int(root.winfo_screenheight())-400
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    btn_window.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")
    btn_window.configure(bg="bisque3")
    btn_window.grab_set()

    s_id_list = show_all_staff()
    head = tkinter.Label(btn_window, text="Edit Staff Form", font=('Courier New', 20, 'bold'), bg="bisque3")
    head.place(x=260, y=30)
    btn_window.update()
    pos_x = int((btn_window.winfo_width()/2)-(head.winfo_width()/2))
    pos_y = int((btn_window.winfo_height()/2)-(head.winfo_height()/2))/3
    head['fg'] = "black"
    head.place(x=pos_x, y=pos_y)
    btn_window.update()
    sid_label = tkinter.Label(btn_window, text="Staff ID :", font=('Courier New', 15), bg="bisque3")
    sid_input = ttk.Combobox(btn_window, width=10, font=('Courier New', 15), values=s_id_list, state='readonly')
    sid_label.place(x=250, y=165)
    sid_input.place(x=405, y=165)

    con_button = tkinter.Button(btn_window, text="Continue", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command= con)
    exit_button1 = tkinter.Button(btn_window, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window))

    con_button.place(x=300, y=290)
    exit_button1.place(x=440, y=290)

    btn_window.bind('<F5>', lambda event: ref())

def display_staff():
    def sing_disp_staff():
        def con():
            stid = stid_input.get()
            values = [stid]
            if "" in values:
                tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
            else:
                stid_label.place_forget()
                stid_input.place_forget()
                con_button.place_forget()
                exit_button1.place_forget()
                windowWidth = 800
                windowHeight = int(root.winfo_screenheight())-400
                positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
                positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
                btn_window1.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")

                is_warden = get_staff_pos(stid)
                staffid_label = tkinter.Label(btn_window1, text="Staff ID :", font=('Courier New', 15), bg="bisque3")
                staffid_input = tkinter.Label(btn_window1, text=stid, font=('Courier New', 15), bg="bisque3")
                iswarden_label = tkinter.Label(btn_window1, text="Is Warden?", font=('Courier New', 15), bg="bisque3")
                iswarden_input = tkinter.Label(btn_window1, text=is_warden, font=('Courier New', 15), bg="bisque3")

                staff_name = get_staff_name(stid)
                name_label = tkinter.Label(btn_window1, text="Name:", font=('Courier New', 15), bg="bisque3")
                name_input = tkinter.Label(btn_window1, text=staff_name, font=('Courier New', 15), bg="bisque3")

                staff_contact = get_staff_cont(stid)
                contact_label = tkinter.Label(btn_window1, text="Contact:", font=('Courier New', 15), bg="bisque3")
                contact_input = tkinter.Label(btn_window1, text=staff_contact, font=('Courier New', 15), bg="bisque3")

                staff_gender = get_staff_gender(stid)
                staff_dob = get_staff_dob(stid)
                dob_label = tkinter.Label(btn_window1, text="Birth Date:", font=('Courier New', 15), bg="bisque3")
                dob_input = tkinter.Label(btn_window1, text=staff_dob, font=('Courier New', 15), bg="bisque3")
                gender_label = tkinter.Label(btn_window1, text="Gender:", font=('Courier New', 15), bg="bisque3")
                gender_input = tkinter.Label(btn_window1, text=staff_gender, font=('Courier New', 15), bg="bisque3")

                exit_button = tkinter.Button(btn_window1, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window1))


                staffid_label.place(x=100, y=110)
                staffid_input.place(x=255, y=110)
                iswarden_label.place(x=400, y=110)
                iswarden_input.place(x=545, y=110)
                
                name_label.place(x=100, y=150)
                name_input.place(x=255, y=150)
                contact_label.place(x=400, y=150)
                contact_input.place(x=545, y=150)
                
                dob_label.place(x=100, y=190)
                dob_input.place(x=255, y=190)
                gender_label.place(x=400, y=190)
                gender_input.place(x=545, y=190)

                btn_window.bind('<F5>', lambda event: ref())
         
                exit_button.place(x=380, y=290)
        btn_window1 = tkinter.Toplevel(root)
        btn_window1.attributes("-topmost", "true")
        btn_window1.resizable(False, False)
        btn_window1.focus_set()
        btn_window1.title("Display Individual Staff Details")
        windowWidth = 800
        windowHeight = int(root.winfo_screenheight())-400
        positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
        btn_window1.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")
        btn_window1.configure(bg="bisque3")
        btn_window1.grab_set()

        s_id_list = show_all_staff()
        head = tkinter.Label(btn_window1, text="Display Individual Staff Details", font=('Courier New', 20, 'bold'), bg="bisque3")
        head.place(x=260, y=30)
        btn_window1.update()
        pos_x = int((btn_window1.winfo_width()/2)-(head.winfo_width()/2))
        pos_y = int((btn_window1.winfo_height()/2)-(head.winfo_height()/2))/3
        head['fg'] = "black"
        head.place(x=pos_x, y=pos_y)
        btn_window1.update()

        stid_label = tkinter.Label(btn_window1, text="Staff ID :", font=('Courier New', 15), bg="bisque3")
        stid_input = ttk.Combobox(btn_window1, width=10, font=('Courier New', 15), values=s_id_list, state='readonly')
        stid_label.place(x=250, y=165)
        stid_input.place(x=405, y=165)

        con_button = tkinter.Button(btn_window1, text="Continue", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command = lambda: con())
        exit_button1 = tkinter.Button(btn_window1, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window1))

        con_button.place(x=300, y=290)
        exit_button1.place(x=440, y=290)

        btn_window1.bind('<Return>', lambda event: con())
        btn_window1.bind('<Escape>', lambda event: btn_window.destroy())
        btn_window1.bind('<F5>', lambda event: ref())

    def all_disp_staff():
        try:
            path = os.path.join(sys.path[0], "details/")
            filename = 'staff_details.pdf'
            os.startfile(f"{path}{filename}")
        except OSError:
            tkinter.messagebox.showerror("RSGH - RMD", "The file/directory has been moved or does not exist! Please restart the application to fix this error!")

    btn_window = tkinter.Toplevel(root)
    btn_window.focus_set()
    btn_window.title("Display Staff Details")
    btn_window.resizable(False, False)
    windowWidth = 800
    windowHeight = int(root.winfo_screenheight())-400
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    btn_window.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")
    btn_window.configure(bg="bisque3")
    btn_window.grab_set()

    head = tkinter.Label(btn_window, text="Display Staff Details", font=('Courier New', 20, 'bold'), bg="bisque3")
    head.place(x=260, y=30)
    btn_window.update()
    pos_x = int((btn_window.winfo_width()/2)-(head.winfo_width()/2))
    pos_y = int((btn_window.winfo_height()/2)-(head.winfo_height()/2))/3
    head['fg'] = "black"
    head.place(x=pos_x, y=pos_y)
    btn_window.update()

    all_disp_button = tkinter.Button(btn_window, text="Display All Details", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=all_disp_staff)
    sing_disp_button = tkinter.Button(btn_window, text="Display Individual Staff Details", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=sing_disp_staff)


    all_disp_button.place(x=300, y=290)
    sing_disp_button.place(x=250, y=200)
    btn_window.update()
    pos_x_sdb = int((btn_window.winfo_width()/2)-(sing_disp_button.winfo_width()/2))
    pos_y_sdb = int((btn_window.winfo_height()/2)-(sing_disp_button.winfo_height()/2))
    pos_x_adb = int((btn_window.winfo_width()/2)-(all_disp_button.winfo_width()/2))
    pos_y_adb = int((btn_window.winfo_height()/2)-(all_disp_button.winfo_height()/2))+50
    sing_disp_button['fg'] = "black"
    all_disp_button['fg'] = "black"
    sing_disp_button.place(x=pos_x_sdb, y=pos_y_sdb)
    all_disp_button.place(x=pos_x_adb, y=pos_y_adb)
    btn_window.update()


def add_course():
    def pass_course():
        c_id = courseid_input.get()
        c_name = course_input.get()
        sems = sems_input.get()
        values = [c_id, c_name, sems]
        if "" in values:
            tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
        else:
            insert_course(c_id, c_name, sems, btn_window, add_course)
            
        

    btn_window = tkinter.Toplevel(root)
    btn_window.attributes("-topmost", "true")
    btn_window.resizable(False, False)
    btn_window.focus_set()
    btn_window.title("Add Course")
    windowWidth = 800
    windowHeight = int(root.winfo_screenheight())-450
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    btn_window.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")
    btn_window.configure(bg="bisque3")
    btn_window.grab_set()

    head = tkinter.Label(btn_window, text="Add Course", font=('Courier New', 20, 'bold'), bg="bisque3")
    head.place(x=260, y=30)
    btn_window.update()
    pos_x = int((btn_window.winfo_width()/2)-(head.winfo_width()/2))
    pos_y = int((btn_window.winfo_height()/2)-(head.winfo_height()/2))/3
    head['fg'] = "black"
    head.place(x=pos_x, y=pos_y)
    btn_window.update()
    
    courseid_label = tkinter.Label(btn_window, text="Course ID :", font=('Courier New', 15), bg="bisque3")
    courseid_input = tkinter.Entry(btn_window, width=10,  font=('Courier New', 15))
    course_label = tkinter.Label(btn_window, text="Course Name:", font=('Courier New', 15), bg="bisque3")
    course_input = ttk.Entry(btn_window, width=10, font=('Courier New', 15))
    
    sems_label = tkinter.Label(btn_window, text="Semesters:", font=('Courier New', 15), bg="bisque3")
    sems_input = ttk.Combobox(btn_window, width=8, font=('Courier New', 15), values=[4, 6, 8, 10, 12], state='readonly')
    
    add_button = tkinter.Button(btn_window, text="Add Course", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: pass_course())
    exit_button = tkinter.Button(btn_window, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window))

    courseid_label.place(x=100, y=110)
    courseid_input.place(x=255, y=110)
    course_label.place(x=400, y=110)
    course_input.place(x=555, y=110)
    
    sems_label.place(x=100, y=150)
    sems_input.place(x=255, y=150)

    add_button.place(x=300, y=230)
    exit_button.place(x=440, y=230)

    btn_window.bind('<F5>', lambda event: ref())

def all_disp_course():
    try:
        path = os.path.join(sys.path[0], "details/")
        filename = 'courses_details.pdf'
        os.startfile(f"{path}{filename}")
    except OSError:
        tkinter.messagebox.showerror("RSGH - RMD", "The file/directory has been moved or does not exist! Please restart the application to fix this error!")

def pay_fees():
    def pass_pay_fees(s_id):
        try:
            transaction(s_id)
            tkinter.messagebox.showinfo("RSGH - RMD", f"Fees paid successfully!", parent=btn_window)
            btn_window.destroy()
            pay_fees()
        except:
            tkinter.messagebox.showerror("RSGH - RMD", f"There occurred a problem while paying fees! Please try again later.", parent=btn_window)

    def con():
        sid = sid_input.get()

        values = [sid]
        if "" in values:
            tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
        else:
            sid_label.place_forget()
            sid_input.place_forget()
            con_button.place_forget()
            exit_button1.place_forget()
            studid_label = tkinter.Label(btn_window, text="Student ID :", font=('Courier New', 15), bg="bisque3")
            studid_input = tkinter.Label(btn_window, text=sid, font=('Courier New', 15), bg="bisque3")

            name = get_stu_name(sid)
            sname_label = tkinter.Label(btn_window, text="Name:", font=('Courier New', 15), bg="bisque3")
            sname_input = tkinter.Label(btn_window, text=f"{name}", font=('Courier New', 15), bg="bisque3")

            room_charges, mess_charges, add_charges, total_charge = get_fee_details(sid)

            roomcharges_label = tkinter.Label(btn_window, text="Bed Charges:", font=('Courier New', 15), bg="bisque3")
            roomcharges_input = tkinter.Label(btn_window, text=f"₹ {room_charges}", font=('Courier New', 15), bg="bisque3")

            messcharges_label = tkinter.Label(btn_window, text="Mess Charges:", font=('Courier New', 15), bg="bisque3")
            messcharges_input = tkinter.Label(btn_window, text=f"₹ {mess_charges}", font=('Courier New', 15), bg="bisque3")
            
            additional_label = tkinter.Label(btn_window, text="Addn. Charges:", font=('Courier New', 15), bg="bisque3")
            additional_input = tkinter.Label(btn_window, text=f"₹ {add_charges}", font=('Courier New', 15), bg="bisque3")
        
            total_label = tkinter.Label(btn_window, text="Total:", font=('Courier New', 15), bg="bisque3")
            total_input = tkinter.Label(btn_window, text=f"₹ {total_charge}", font=('Courier New', 15), bg="bisque3")

            add_button = tkinter.Button(btn_window, text="Pay Fees", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: pass_pay_fees(sid))
            exit_button = tkinter.Button(btn_window, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window))

            studid_label.place(x=100, y=110)
            studid_input.place(x=255, y=110)
            sname_label.place(x=400, y=110)
            sname_input.place(x=545, y=110)

            roomcharges_label.place(x=100, y=150)
            roomcharges_input.place(x=270, y=150)

            messcharges_label.place(x=400, y=150)
            messcharges_input.place(x=565, y=150)

            additional_label.place(x=100, y=190)
            additional_input.place(x=270, y=190)

            total_label.place(x=400, y=190)
            total_input.place(x=565, y=190)

            add_button.place(x=310, y=290)
            exit_button.place(x=430, y=290)
        
            btn_window.bind('<F5>', lambda event: ref())



    btn_window = tkinter.Toplevel(root)
    btn_window.attributes("-topmost", "true")
    btn_window.resizable(False, False)
    btn_window.focus_set()
    btn_window.title("Pay Fees")
    windowWidth = 800
    windowHeight = int(root.winfo_screenheight())-400
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    btn_window.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")
    btn_window.configure(bg="bisque3")
    btn_window.grab_set()

    head = tkinter.Label(btn_window, text="Pay Fees", font=('Courier New', 20, 'bold'), bg="bisque3", fg="bisque3")
    head.place(x=260, y=30)
    btn_window.update()
    pos_x = int((btn_window.winfo_width()/2)-(head.winfo_width()/2))
    pos_y = int((btn_window.winfo_height()/2)-(head.winfo_height()/2))/3
    head['fg'] = "black"
    head.place(x=pos_x, y=pos_y)
    btn_window.update()

    s_list = show_all_stu()
    sid_label = tkinter.Label(btn_window, text="Student ID :", font=('Courier New', 15), bg="bisque3")
    sid_input = ttk.Combobox(btn_window, width=10, font=('Courier New', 15), values=s_list, state='readonly')
    sid_label.place(x=250, y=165)
    sid_input.place(x=405, y=165)

    con_button = tkinter.Button(btn_window, text="Continue", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=con)
    exit_button1 = tkinter.Button(btn_window, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window))

    con_button.place(x=300, y=290)
    exit_button1.place(x=440, y=290)

    btn_window.bind('<F5>', lambda event: ref())



def addn_charges():
    def pass_add_charges(sid, charges_input):
        amount = charges_input.get()
        values = [amount]
        if "" in values:
            tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
        else:
            give_add_charges(sid, amount)
            tkinter.messagebox.showinfo("RSGH - RMD", "Additional Charges added successfully to monthly fees!", parent=btn_window)
            btn_window.destroy()
            addn_charges()

    def con():
        sid = sid_input.get()

        values = [sid]
        if "" in values:
            tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
        else:
            sid_label.place_forget()
            sid_input.place_forget()
            con_button.place_forget()
            exit_button1.place_forget()

            studid_label = tkinter.Label(btn_window, text="Student ID :", font=('Courier New', 15), bg="bisque3")
            studid_input = tkinter.Label(btn_window, text=sid, font=('Courier New', 15), bg="bisque3")

            name = get_stu_name(sid)
            sname_label = tkinter.Label(btn_window, text="Name:", font=('Courier New', 15), bg="bisque3")
            sname_input = tkinter.Label(btn_window, text=name, font=('Courier New', 15), bg="bisque3")

            room = get_stu_room(sid)
            roomid_label = tkinter.Label(btn_window, text="Room ID:", font=('Courier New', 15), bg="bisque3")
            roomid_input = tkinter.Label(btn_window, text=room, font=('Courier New', 15), bg="bisque3")

            charges_label = tkinter.Label(btn_window, text="Charges(in ₹):", font=('Courier New', 15), bg="bisque3")
            charges_input = tkinter.Entry(btn_window, width=10, font=('Courier New', 15))
            
            add_button = tkinter.Button(btn_window, text="Add Charges", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: pass_add_charges(sid, charges_input))
            exit_button = tkinter.Button(btn_window, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window))

            studid_label.place(x=100, y=110)
            studid_input.place(x=255, y=110)
            sname_label.place(x=400, y=110)
            sname_input.place(x=545, y=110)

            roomid_label.place(x=100, y=150)
            roomid_input.place(x=270, y=150)

            charges_label.place(x=400, y=150)
            charges_input.place(x=575, y=150)

            add_button.place(x=280, y=290)
            exit_button.place(x=440, y=290)
        

            btn_window.bind('<F5>', lambda event: ref())



    btn_window = tkinter.Toplevel(root)
    btn_window.attributes("-topmost", "true")
    btn_window.resizable(False, False)
    btn_window.focus_set()
    btn_window.title("Additional Charges")
    windowWidth = 800
    windowHeight = int(root.winfo_screenheight())-400
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    btn_window.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")
    btn_window.configure(bg="bisque3")
    btn_window.grab_set()

    head = tkinter.Label(btn_window, text="Additional Charges", font=('Courier New', 20, 'bold'), bg="bisque3", fg="bisque3")
    head.place(x=260, y=30)
    btn_window.update()
    pos_x = int((btn_window.winfo_width()/2)-(head.winfo_width()/2))
    pos_y = int((btn_window.winfo_height()/2)-(head.winfo_height()/2))/3
    head['fg'] = "black"
    head.place(x=pos_x, y=pos_y)
    btn_window.update()

    stu_id_values = show_all_stu()
    sid_label = tkinter.Label(btn_window, text="Student ID :", font=('Courier New', 15), bg="bisque3")
    sid_input = ttk.Combobox(btn_window, width=10, font=('Courier New', 15), values=stu_id_values, state='readonly')
    sid_label.place(x=250, y=165)
    sid_input.place(x=405, y=165)

    con_button = tkinter.Button(btn_window, text="Continue", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=con)
    exit_button1 = tkinter.Button(btn_window, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window))

    con_button.place(x=300, y=290)
    exit_button1.place(x=440, y=290)

    btn_window.bind('<F5>', lambda event: ref())


def monthly_bill():
    def generate():
        sid = sid_input.get()
        tmonth = t_month_input.get()
        values = [sid, tmonth]
        if "" in values:
            tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
        else:
            tid = get_tmonth(sid, tmonth)
            gen_monthly_bill(sid, tid)
            btn_window.destroy()
            monthly_bill()

    def updatesid():
        sid = sid_input.get()
        trans = get_tranid(sid)
        month_list = [data[1] for data in trans]
        t_month_input['values'] = month_list
        t_month_input['state'] = 'readonly'

    btn_window = tkinter.Toplevel(root)
    btn_window.focus_set()
    btn_window.resizable(False, False)
    btn_window.title("Monthly Bill")
    windowWidth = 800
    windowHeight = int(root.winfo_screenheight())-450
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    btn_window.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")
    btn_window.configure(bg="bisque3")
    btn_window.grab_set()

    head = tkinter.Label(btn_window, text="Generate Bill", font=('Courier New', 20, 'bold'), bg="bisque3", fg="bisque3")
    head.place(x=260, y=30)
    btn_window.update()
    pos_x = int((btn_window.winfo_width()/2)-(head.winfo_width()/2))
    pos_y = int((btn_window.winfo_height()/2)-(head.winfo_height()/2))/3
    head['fg'] = "black"
    head.place(x=pos_x, y=pos_y)
    btn_window.update()

    s_list = list_stu_paid()
    sid_label = tkinter.Label(btn_window, text="Student ID:", font=('Courier New', 15), bg="bisque3")
    sid_input = ttk.Combobox(btn_window, width=10, font=('Courier New', 15), values=s_list, state='readonly')

    t_month_label = tkinter.Label(btn_window, text="Month:", font=('Courier New', 15), bg="bisque3")
    t_month_input = ttk.Combobox(btn_window, width=10, font=('Courier New', 15), state=DISABLED)

    sid_label.place(x=250, y=125)
    sid_input.place(x=405, y=125)
    t_month_label.place(x=250, y=170)
    t_month_input.place(x=405, y=170)

    gen_btn = tkinter.Button(btn_window, text="Generate", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: generate())
    exit_button1 = tkinter.Button(btn_window, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window))

    gen_btn.place(x=300, y=250)
    exit_button1.place(x=440, y=250)

    btn_window.bind('<F5>', lambda event: ref())
    sid_input.bind("<<ComboboxSelected>>", lambda event: updatesid())


def delete_student():
    def pass_del_stu():
        sid = studentid_input.get()
        values = [sid]
        if "" in values:
            tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
        else:
            name = get_stu_name(sid)
            course = get_stu_course(sid)
            result = tkinter.messagebox.askyesno("RSGH - RMD", f"Please confirm your request. These changes cannot be reverted!\n\nYou have requested to remove all records of the following candidate:\n\nID: {sid}\nName: {name}\nCourse: {course}\n\nDelete records?", parent=btn_window)
            if result == True:
                del_stu(sid, btn_window)
                btn_window.destroy()
                delete_student()

    btn_window = tkinter.Toplevel(root)
    btn_window.attributes("-topmost", "true")
    btn_window.resizable(False, False)
    btn_window.focus_set()
    btn_window.title("Delete Student")
    windowWidth = 800
    windowHeight = int(root.winfo_screenheight())-400
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    btn_window.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")
    btn_window.configure(bg="bisque3")
    btn_window.grab_set()

    head = tkinter.Label(btn_window, text="Delete Student", font=('Courier New', 20, 'bold'), bg="bisque3")
    head.place(x=260, y=30)
    btn_window.update()
    pos_x = int((btn_window.winfo_width()/2)-(head.winfo_width()/2))
    pos_y = int((btn_window.winfo_height()/2)-(head.winfo_height()/2))/3
    head['fg'] = "black"
    head.place(x=pos_x, y=pos_y)
    btn_window.update()

    s_id_list = show_all_stu()
    studentid_label = tkinter.Label(btn_window, text="Student ID :", font=('Courier New', 15), bg="bisque3")
    studentid_input = ttk.Combobox(btn_window, width=10, font=('Courier New', 15), values=s_id_list, state='readonly')
    studentid_label.place(x=250, y=165)
    studentid_input.place(x=405, y=165)

    delete_button = tkinter.Button(btn_window, text="Delete information", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: pass_del_stu())
    exit_button = tkinter.Button(btn_window, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window))

    delete_button.place(x=250, y=290)
    exit_button.place(x=470, y=290)
    
    btn_window.bind('<F5>', lambda event: ref())

def delete_staff():
    def pass_del_staff():
        sid = staffid_input.get()
        values = [sid]
        if "" in values:
            tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
        else:
            name = get_staff_name(sid)
            gender = get_staff_gender(sid)
            result = tkinter.messagebox.askyesno("RSGH - RMD", f"Please confirm your request. These changes cannot be reverted!\n\nYou have requested to remove all records of the following staff:\n\nID: {sid}\nName: {name}\nGender: {gender}\n\nDelete records?", parent=btn_window)
            if result == True:
                del_staff(sid, btn_window)
                btn_window.destroy()
                delete_staff()
                
    btn_window = tkinter.Toplevel(root)
    btn_window.attributes("-topmost", "true")
    btn_window.resizable(False, False)
    btn_window.focus_set()
    btn_window.title("Remove Staff")
    windowWidth = 800
    windowHeight = int(root.winfo_screenheight())-400
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    btn_window.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")
    btn_window.configure(bg="bisque3")
    btn_window.grab_set()

    head = tkinter.Label(btn_window, text="Remove Staff", font=('Courier New', 20, 'bold'), bg="bisque3")
    head.place(x=260, y=30)
    btn_window.update()
    pos_x = int((btn_window.winfo_width()/2)-(head.winfo_width()/2))
    pos_y = int((btn_window.winfo_height()/2)-(head.winfo_height()/2))/3
    head['fg'] = "black"
    head.place(x=pos_x, y=pos_y)
    btn_window.update()

    s_id_list = show_all_staff()
    staffid_label = tkinter.Label(btn_window, text="Staff ID :", font=('Courier New', 15), bg="bisque3")
    staffid_input = ttk.Combobox(btn_window, width=10, font=('Courier New', 15), values=s_id_list, state= 'readonly')
    staffid_label.place(x=250, y=165)
    staffid_input.place(x=405, y=165)

    delete_button = tkinter.Button(btn_window, text="Delete information", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: pass_del_staff())
    exit_button = tkinter.Button(btn_window, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window))

    delete_button.place(x=250, y=290)
    exit_button.place(x=470, y=290)
    
    btn_window.bind('<F5>', lambda event: ref())

def delete_block():
    def pass_del_block():
        bid = blockid_input.get()
        values = [bid]
        if "" in values:
            tkinter.messagebox.showerror("RSGH - RMD", "Please fill up all details!", parent=btn_window)
        else:
            name = get_block_type(bid)
            gender = get_block_gender(bid)
            result = tkinter.messagebox.askyesno("RSGH - RMD", f"Please confirm your request. These changes cannot be reverted!\n\nYou have requested to remove all records of the following staff:\n\nID: {bid}\nName: {name}\nGender: {gender}\n\nDelete records?", parent=btn_window)
            if result == True:
                del_block(bid, btn_window)
                btn_window.destroy()
                delete_block() 
                     

    btn_window = tkinter.Toplevel(root)
    btn_window.attributes("-topmost", "true")
    btn_window.resizable(False, False)
    btn_window.focus_set()
    btn_window.title("Remove Block")
    windowWidth = 800
    windowHeight = int(root.winfo_screenheight())-400
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    btn_window.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")
    btn_window.configure(bg="bisque3")
    btn_window.grab_set()

    head = tkinter.Label(btn_window, text="Remove Block", font=('Courier New', 20, 'bold'), bg="bisque3")
    head.place(x=260, y=30)
    btn_window.update()
    pos_x = int((btn_window.winfo_width()/2)-(head.winfo_width()/2))
    pos_y = int((btn_window.winfo_height()/2)-(head.winfo_height()/2))/3
    head['fg'] = "black"
    head.place(x=pos_x, y=pos_y)
    btn_window.update()

    b_id_list = show_all_blocks()
    blockid_label = tkinter.Label(btn_window, text="Block ID :", font=('Courier New', 15), bg="bisque3")
    blockid_input = ttk.Combobox(btn_window, width=10, font=('Courier New', 15), values=b_id_list, state= 'readonly')
    blockid_label.place(x=250, y=165)
    blockid_input.place(x=405, y=165)

    delete_button = tkinter.Button(btn_window, text="Delete information", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: pass_del_block())
    exit_button = tkinter.Button(btn_window, text="Exit", bg="bisque4", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", command=lambda: btn_exit(btn_window))

    delete_button.place(x=250, y=290)
    exit_button.place(x=470, y=290)
    
    btn_window.bind('<F5>', lambda event: ref())