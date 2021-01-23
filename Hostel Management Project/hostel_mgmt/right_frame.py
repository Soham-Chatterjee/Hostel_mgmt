import tkinter
from hostel_mgmt import root
from PIL import Image, ImageTk
from hostel_mgmt.design import right_frame

def on_enter(btn):
    btn['bg'] = "bisque"

def on_leave(btn):
    btn['bg'] = "bisque3"

image_load = Image.open("./Fee Chart.png")
image_render = ImageTk.PhotoImage(image_load)


pos = {'x': 12, 'btn1': 10, 'btn2': 60, 'btn3': 110, 'btn4': 160, 'btn5': 210, 'btn6': 260, 'btn7':310}

btn1 = tkinter.Button(right_frame, text="Button 1", bg="bisque3", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", width=26)

btn2 = tkinter.Button(right_frame, text="Button 2", bg="bisque3", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", width=26)

btn3 = tkinter.Button(right_frame, text="Button 3", bg="bisque3", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", width=26)


btn4 = tkinter.Button(right_frame, text="Button 4", bg="bisque3", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", width=26)

btn5 = tkinter.Button(right_frame, text="Button 4", bg="bisque3", activebackground="bisque3", relief="flat", font=("Courier New", 12), cursor="hand2", width=26)

img = tkinter.Label(right_frame, image=image_render)
img.image = image_render
img.config(bg='bisque4')
img.place(x=5, y=435)

btn_list = [btn1, btn2, btn3, btn4, btn5]

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



