import tkinter
from hostel_mgmt import root
from hostel_mgmt.design import center_frame


home_text = tkinter.Label(center_frame, text="RISING STAR GROUP OF HOSTELS\nRECORDS MANAGEMENT DATABASE", bg="bisque3", fg="bisque3", font=('Courier New', 30))
home_text.place(x=100, y=100)
root.update()
pos_x = int((center_frame.winfo_width()/2)-(home_text.winfo_width()/2))
pos_y = int((center_frame.winfo_height()/2)-(home_text.winfo_height()/2))
home_text['fg'] = "bisque4"
home_text.place(x=pos_x, y=pos_y)
root.update(
