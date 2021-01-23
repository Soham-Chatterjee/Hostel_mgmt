import tkinter
from hostel_mgmt import root
from hostel_mgmt.design import left_frame
from hostel_mgmt.left_frame_func import chng1, chng2, chng3, chng4, chng5, chng6, chng7, chng8, ref, chg_pswd, _exit

def on_enter(btn):
    btn['bg'] = "bisque"

def on_leave(btn):
    btn['bg'] = "bisque3"


btn1 = tkinter.Button(left_frame, text="Student Details", bg="bisque3", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", width=27, command=chng1)
btn1.place(x=10, y=10)

btn2 = tkinter.Button(left_frame, text="Block/Room Details", bg="bisque3", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", width=27, command=chng2)
btn2.place(x=10, y=60)

btn3 = tkinter.Button(left_frame, text="Mess", bg="bisque3", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", width=27, command=chng3)
btn3.place(x=10, y=110)

btn4 = tkinter.Button(left_frame, text="Staff", bg="bisque3", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", width=27, command=chng4)
btn4.place(x=10, y=160)

btn5 = tkinter.Button(left_frame, text="Courses", bg="bisque3", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", width=27, command=chng5)
btn5.place(x=10, y=210)

btn6 = tkinter.Button(left_frame, text="Fee Payment", bg="bisque3", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", width=27, command=chng6)
btn6.place(x=10, y=260)

btn7 = tkinter.Button(left_frame, text="Billing", bg="bisque3", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", width=27, command=chng7)
btn7.place(x=10, y=310)

btn8 = tkinter.Button(left_frame, text="Delete record(s)", bg="bisque3", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", width=27, command=chng8)
btn8.place(x=10, y=360)

refresh = tkinter.Button(left_frame, text="Refresh", bg="bisque3", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", width=27, command=ref)
refresh.place(x=10, y=410)

chng_pswd = tkinter.Button(left_frame, text="Change Password", bg="bisque3", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", width=27, command=chg_pswd)
chng_pswd.place(x=10, y=460)

exit_btn = tkinter.Button(left_frame, text="Exit", bg="bisque3", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", width=27, command=_exit)
exit_btn.place(x=10, y=510)

btn1.bind("<Enter>", lambda event: on_enter(btn1))
btn1.bind("<Leave>", lambda event: on_leave(btn1))
btn2.bind("<Enter>", lambda event: on_enter(btn2))
btn2.bind("<Leave>", lambda event: on_leave(btn2))
btn3.bind("<Enter>", lambda event: on_enter(btn3))
btn3.bind("<Leave>", lambda event: on_leave(btn3))
btn4.bind("<Enter>", lambda event: on_enter(btn4))
btn4.bind("<Leave>", lambda event: on_leave(btn4))
btn5.bind("<Enter>", lambda event: on_enter(btn5))
btn5.bind("<Leave>", lambda event: on_leave(btn5))
btn6.bind("<Enter>", lambda event: on_enter(btn6))
btn6.bind("<Leave>", lambda event: on_leave(btn6))
btn7.bind("<Enter>", lambda event: on_enter(btn7))
btn7.bind("<Leave>", lambda event: on_leave(btn7))
btn8.bind("<Enter>", lambda event: on_enter(btn8))
btn8.bind("<Leave>", lambda event: on_leave(btn8))
refresh.bind("<Enter>", lambda event: on_enter(refresh))
refresh.bind("<Leave>", lambda event: on_leave(refresh))
chng_pswd.bind("<Enter>", lambda event: on_enter(chng_pswd))
chng_pswd.bind("<Leave>", lambda event: on_leave(chng_pswd))
exit_btn.bind("<Enter>", lambda event: on_enter(exit_btn))
exit_btn.bind("<Leave>", lambda event: on_leave(exit_btn))