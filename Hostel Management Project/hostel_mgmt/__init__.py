import tkinter
import tkinter.messagebox
import pickle


with open("pvt.dat", "rb") as pvt_file:
    pswd_correct = pickle.load(pvt_file)

def on_close():
    result = tkinter.messagebox.askyesno("RSGH - RMD", "Do you want to exit the database?")
    if result == True:
        quit()


root = tkinter.Tk()


w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("RSGH - Records Management Database - Administrator")


import hostel_mgmt.auth

import hostel_mgmt.design

root.protocol('WM_DELETE_WINDOW', on_close)

root.mainloop()