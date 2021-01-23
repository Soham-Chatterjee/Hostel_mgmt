import tkinter
import tkinter.messagebox
import pickle
from passlib.hash import pbkdf2_sha256
from hostel_mgmt import root, pswd_correct, design
from hostel_mgmt.right_frame import pos, btn_list
from hostel_mgmt.right_frame_func import *

def chng1():
    text = ["Add Student", "Edit Student", "Change rooms", "Display Student Details"]
    command_list = [add_stu, edit_stu, change_rooms, display_stu]
    for btn in btn_list:
        btn.place_forget()
    for i in range(1,5):
        btn_list[i-1]['text'] = text[i-1]
        btn_list[i-1]['command'] = command_list[i-1]
        btn_list[i-1].place(x=pos['x'], y=pos[f'btn{i}'])

        
        
            

def chng2():
    text = ["Add Block", "Extend Block", "Change Warden", "Display Block Details", "Display Room Details"]
    command_list = [add_block, edit_block, changewarden, display_block, all_disp_room]
    for btn in btn_list:
        btn.place_forget()
    for i in range(1,6):
        btn_list[i-1]['text'] = text[i-1]
        btn_list[i-1]['command'] = command_list[i-1]
        btn_list[i-1].place(x=pos['x'], y=pos[f'btn{i}'])


def chng3():
    text = ["Add Mess", "Display Mess Details"]
    command_list = [add_mess, all_disp_mess]
    for btn in btn_list:
        btn.place_forget()
    for i in range(1,3):
        btn_list[i-1]['text'] = text[i-1]
        btn_list[i-1]['command'] = command_list[i-1]
        btn_list[i-1].place(x=pos['x'], y=pos[f'btn{i}'])


def chng4():
    text = ["Add Staff", "Edit Staff", "Display Staff Details"]
    command_list = [add_staff, edit_staff, display_staff]
    for btn in btn_list:
        btn.place_forget()
    for i in range(1,4):
        btn_list[i-1]['text'] = text[i-1]
        btn_list[i-1]['command'] = command_list[i-1]
        btn_list[i-1].place(x=pos['x'], y=pos[f'btn{i}'])

def chng5():
    text = ["Add Course", "Display Courses"]
    command_list = [add_course, all_disp_course]
    for btn in btn_list:
        btn.place_forget()
    for i in range(1,3):
        btn_list[i-1]['text'] = text[i-1]
        btn_list[i-1]['command'] = command_list[i-1]
        btn_list[i-1].place(x=pos['x'], y=pos[f'btn{i}'])

def chng6():
    text = ["Fee Payment", "Add Additional Charges"]
    command_list = [pay_fees, addn_charges]
    for btn in btn_list:
        btn.place_forget()
    for i in range(1,3):
        btn_list[i-1]['text'] = text[i-1]
        btn_list[i-1]['command'] = command_list[i-1]
        btn_list[i-1].place(x=pos['x'], y=pos[f'btn{i}'])

def chng7():
    text = ["Generate Monthly Bill"]
    command_list = [monthly_bill]
    for btn in btn_list:
        btn.place_forget()
    for i in range(1,2):
        btn_list[i-1]['text'] = text[i-1]
        btn_list[i-1]['command'] = command_list[i-1]
        btn_list[i-1].place(x=pos['x'], y=pos[f'btn{i}'])

def chng8():
    text = ["Delete Student", "Delete Block", "Remove Staff"]
    command_list = [delete_student, delete_block, delete_staff]
    for btn in btn_list:
        btn.place_forget()
    for i in range(1,4):
        btn_list[i-1]['text'] = text[i-1]
        btn_list[i-1]['command'] = command_list[i-1]
        btn_list[i-1].place(x=pos['x'], y=pos[f'btn{i}'])

def _exit():
    result = tkinter.messagebox.askyesno("RSGH - RMD", "Do you want to exit the database?")
    if result == True:
        quit()
    else:
        pass

def chg_pswd():
    def backend_pswd_change():
        old_pswd = old_pswd_input.get()
        new_pswd = new_pswd_input.get()
        if pbkdf2_sha256.verify(old_pswd, pswd_correct):
            if new_pswd != '' and new_pswd == new_pswd_confrm_input.get():
                with open("pvt.dat", "wb") as f_in:
                    pswd = new_pswd_input.get()
                    hashed_pass = pbkdf2_sha256.hash(pswd)
                    pickle.dump(hashed_pass, f_in)
                pswd_chng.destroy()
                tkinter.messagebox.showinfo("RSGH - RMD", "Password changed successfully!")  
            elif new_pswd == '':
                tkinter.Label(pswd_chng, text= "Password Cannot be blank", fg="white", bg="bisque4", font=("Courier New", 12)).place(x=125, y=40)
                pswd_chng.update()
            else:
                tkinter.Label(pswd_chng, text= "Passwords do not match!", fg="white", bg="bisque4", font=("Courier New", 12)).place(x=125, y=40)
                pswd_chng.update()
        else:
            tkinter.Label(pswd_chng, text= "Incorrect old password!", fg="white", bg="bisque4", font=("Courier New", 12)).place(x=125, y=40)
            pswd_chng.update()




    def exit_pswd():
        pswd_chng.destroy()

    for widget in root.winfo_children():
        if isinstance(widget, tkinter.Toplevel):
            widget.destroy()
    for btn in btn_list:
        btn.place_forget()

    pswd_chng = tkinter.Toplevel(root)
    pswd_chng.attributes("-topmost", "true")
    pswd_chng.focus_set()
    pswd_chng.overrideredirect(True)
    windowWidth = 500
    windowHeight = 300
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    pswd_chng.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionDown}")
    pswd_chng.configure(bg="bisque4")
    pswd_chng.grab_set()

    old_pswd_input_label = tkinter.Label(pswd_chng, text="Old Password :", font=('Courier New', 15), bg="bisque4", fg="white")
    old_pswd_input = tkinter.Entry(pswd_chng, show='*', width=15,  font=('Courier New', 15))
    new_pswd_input_label = tkinter.Label(pswd_chng, text="New Password :", font=('Courier New', 15), bg="bisque4", fg="white")
    new_pswd_input = tkinter.Entry(pswd_chng, show="*", width=15,  font=('Courier New', 15))
    new_pswd_confrm_input_label = tkinter.Label(pswd_chng, text="Confirm Password :", font=('Courier New', 15), bg="bisque4", fg="white")
    new_pswd_confrm_input = tkinter.Entry(pswd_chng, show="*", width=15,  font=('Courier New', 15))
    change_btn = tkinter.Button(pswd_chng, text="Change", bg="bisque3", activebackground="bisque4", relief="flat", font=("Courier New", 12), cursor="hand2", command=backend_pswd_change)
    exit_button = tkinter.Button(pswd_chng, text="Exit", bg="bisque3", activebackground="bisque4", relief="flat", font=("Courier New", 12), cursor="hand2", command=exit_pswd)


    old_pswd_input_label.place(x=70, y=80)
    old_pswd_input.place(x=250, y=80)
    new_pswd_input_label.place(x=70, y=130)
    new_pswd_input.place(x=250, y=130)
    new_pswd_confrm_input_label.place(x=40, y=180)
    new_pswd_confrm_input.place(x=270, y=180)
    change_btn.place(x=180, y=250)
    exit_button.place(x=260, y=250)


    pswd_chng.bind('<Return>', lambda event: backend_pswd_change())
    pswd_chng.bind('<Escape>', lambda event: exit_pswd())

