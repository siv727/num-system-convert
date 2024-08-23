from tkinter import *
from PIL import Image, ImageTk
import customtkinter as ct
import backend as ft

window = ct.CTk()
window.resizable(0,0)

# GLOBAL VARIABLES
out_string = ""
twos = ""

# FUNCTIONS
def check_convert():
    """ 
        Checks for errors before converting the inputted values 
        with the help of backend functions
    """
    user_output.configure(state='normal')
    user_twos_output.configure(state='normal')
    base1 = base_from.get()
    base2 = base_to.get()
    input_string = user_input.get()
    if ft.base_from_input(base1) == False or ft.base_to_input(base2) == False:
        error_label = ct.CTkLabel(master=input_frame, 
                    text="Error: Invalid input! Limit base from 2 to 36 only.",
                    text_color="#ff0000",
                    fg_color="#222831",
                    font=('Courier New', 16, 'bold'),
                    padx=5,
                    pady=5)
        error_label.pack(fill="both", expand=1, anchor='w', pady=(10,0))
        error_label.after(3000, error_label.destroy)
    elif ft.user_input(input_string, int(base1)) == False:
        error_label = ct.CTkLabel(master=input_frame, 
                    text="Error: Invalid characters for base %d" %int(base1),
                    text_color="#ff0000",
                    fg_color="#222831",
                    font=('Courier New', 16, 'bold'),
                    padx=5,
                    pady=5)
        error_label.pack(fill="both", expand=1, anchor='w', pady=(10,0))
        error_label.after(3000, error_label.destroy)
    else:
        int_base1 = int(base1)
        int_base2 = int(base2)
        convert(int_base1, int_base2, input_string)

def convert(base1, base2, input_string):
    """
        Converts the inputted value to the base inputted by the user
    """
    if not input_string.find("-") == -1:
        n_int, n_float = ft.convert_process(base1, base2, input_string)
        out_string = ft.string_return(input_string, n_int, n_float, base1)
        if base1 == 10 and base2 == 2:
            twos = ft.twos_complement(input_string, n_int, base1)
        else:
            twos = "N/A"
    else:
        n_int, n_float = ft.convert_process(base1, base2, input_string)
        twos = "N/A"
        out_string = ft.string_return(input_string, n_int, n_float, base1)
    user_output.delete(0, END)
    user_output.insert(0, out_string)
    user_output.configure(state='disabled')

    user_twos_output.delete(0, END)
    user_twos_output.insert(0, twos)
    user_twos_output.configure(state='disabled')

def switch():
    """
        Switches the values of base1 (from base) and base2 (to base) 
        Switches the values of user input and the output
    """
    user_output.configure(state='normal')
    user_twos_output.configure(state='normal')
    values = [user_output.get(), user_input.get(), base_from.get(), base_to.get()]
    if any(value for value in values):
        swap_values(user_output, user_input)
        swap_values(base_from, base_to)
        user_twos_output._activate_placeholder()
        activate_placeholders_if_empty(values)
    else:
        clear()
    user_input.master.focus()

def clear():
    """
        Clears everything that has been inputted by the user
    """
    for widget in [user_output, user_twos_output, user_input, base_from, base_to]:
        widget.configure(state='normal')
        widget.delete(0, END)
        widget._activate_placeholder()
    user_input.master.focus()

def swap_values(widget1, widget2):
    """
        Swaps the values contained between the 2 widgets
    """
    value1 = widget1.get()
    widget1.delete(0, END)
    widget1.insert(0, widget2.get())
    widget2.delete(0, END)
    widget2.insert(0, value1)

def activate_placeholders_if_empty(values):
    """
        Activates the placeholder text if there is nothing that has been inputted by the user
    """
    for widget, value in zip([user_output, user_input, base_from, base_to], values):
        if not value:
            widget._activate_placeholder()

def convert_when_enter(entry):
    """
        Triggers the conversion when pressing the enter key
    """
    check_convert()


# WINDOW SIZE, TITLE, AND BACKGROUND COLOR
window.geometry("800x500")
window.title("Number System Converter")
window.config(background="#222831")
window.iconbitmap("logo.ico")

# CENTERING THE WINDOW
app_width = 900
app_height = 600

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width/2) - (app_width/2) + 100
y = (screen_height/2) - (app_height/2)

window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

# IMAGE RESIZE
# Read the Image
image = Image.open("logo.png")
# Resize the image using resize() method
resize_image = image.resize((55, 55))
# Accessing resized image and assigning it to photo_1 variable
photo_1 = ImageTk.PhotoImage(resize_image)

# TITLE
label = ct.CTkLabel(window, 
                    text="Number System Converter",
                    text_color="#EEEEEE",
                    fg_color="#222831",
                    font=('Courier New', 45, 'bold'),
                    justify="center",
                    padx=10,
                    image=photo_1,
                    compound='left')
label.pack(anchor="center", pady=(22, 0), padx=(0,0))

# FRAME 1
base_frame = ct.CTkFrame(master=window, fg_color='#222831')
base_frame.pack(fill="both", expand=1, anchor="w", pady=(20, 0), padx=50)

# BASE FROM INPUT
base_from = ct.CTkEntry(master=base_frame,
                        placeholder_text="Base",
                        # height = 40,
                        fg_color = '#31363F',
                        text_color = '#EEEEEE',
                        font = ('Consolas', 28))
base_from.pack(fill='both', expand=1, side="left")
base_from.bind("<Return>", convert_when_enter)

# WORD "TO"
to = ct.CTkLabel(master=base_frame,
                text="to",
                text_color="#EEEEEE",
                fg_color="#222831",
                font=('Courier New', 25, 'bold'),
                padx=10)
to.pack(fill='y', side="left", ipadx=20)

# BASE TO INPUT
base_to = ct.CTkEntry(master=base_frame,
                      placeholder_text="Base",
                    #   height = 40,
                      fg_color = '#31363F',
                      text_color = '#EEEEEE',
                      font = ('Consolas', 28))
base_to.pack(fill='both', expand=1, side="left")
base_to.bind("<Return>", convert_when_enter)

# FRAME 2
input_frame = ct.CTkFrame(master=window, fg_color='#222831')
input_frame.pack(fill="both", expand=1, anchor="w", pady=(20, 0), padx=50)
# VALUE TO BE CONVERTED INPUT
user_input = ct.CTkEntry(master=input_frame,
                         placeholder_text="Enter a value to be converted",
                        #  width = 675,
                        #  height = 60,
                         fg_color = '#31363F',
                         text_color = '#EEEEEE',
                         font = ('Consolas', 28))
user_input.pack(fill="both", expand=1, anchor="w")
user_input.bind("<Return>", convert_when_enter)

# FRAME 3
button_frame = ct.CTkFrame(master=window, fg_color='#222831')
button_frame.pack(fill="both", expand=1, anchor="w", pady=(20, 0), padx=50)

# CONVERT BUTTON
convert_button = ct.CTkButton(master=button_frame,
                       text="Convert",
                       height = 40,
                       fg_color='#76ABAE',
                       text_color = '#EEEEEE',
                       font = ('Consolas', 35, 'bold'),
                       anchor="center",
                       command=check_convert)
convert_button.pack(fill='both', expand=1, side="left")

# SPACE IN BETWEEN
space1 = ct.CTkLabel(master=button_frame,
                     text="",
                    fg_color="#222831",
                    padx=10)
space1.pack(fill="y", side="left")

# SWITCH BUTTON
switch_button = ct.CTkButton(master=button_frame,
                      text="Switch",
                       height = 40,
                       fg_color='#76ABAE',
                       text_color = '#EEEEEE',
                       font = ('Consolas', 35, 'bold'),
                       anchor="center",
                       command=switch)
switch_button.pack(fill='both', expand=1, side="left")

# SPACE IN BETWEEN
space2 = ct.CTkLabel(master=button_frame,
                     text="",
                    fg_color="#222831",
                    padx=10)
space2.pack(fill="y", side="left")

# CLEAR BUTTON
clear_button = ct.CTkButton(master=button_frame,
                      text="Clear",
                       height = 40,
                       fg_color='#76ABAE',
                       text_color = '#EEEEEE',
                       font = ('Consolas', 35, 'bold'),
                       anchor="center",
                       command=clear)
clear_button.pack(fill='both', expand=1, side="left")

# OUTPUT 
user_output = ct.CTkEntry(window,
                          placeholder_text="Converted Value", 
                          width = 675,
                          height = 60,
                          fg_color = '#31363F',
                          text_color = '#EEEEEE',
                          font = ('Consolas', 28))
user_output.pack(fill="both", expand=1, anchor="w", pady=(20, 0), padx=50)

# TWOS COMPLEMENT OUTPUT (IF APPLICABLE)
user_twos_output = ct.CTkEntry(window, 
                                width = 675,
                                placeholder_text="Twos Complement Value",
                                height = 60,
                                fg_color = '#31363F',
                                text_color = '#EEEEEE',
                                font = ('Consolas', 28))
user_twos_output.pack(fill="both", expand=1, anchor="w", pady=(15, 10), padx=50)

# IMAGE RESIZE FOR COPYRIGHT ICON
image_1 = Image.open("logo3.png")
resize_image_1 = image_1.resize((30, 30))
photo_2 = ImageTk.PhotoImage(resize_image_1)

# PROGRAM OWNER
label = ct.CTkLabel(window, 
                    text="Ervin Louis Villas",
                    text_color="#EEEEEE",
                    fg_color="#222831",
                    font=('Courier New', 13, 'bold'),
                    justify="center",
                    padx=10,
                    image=photo_2,
                    compound='left')
label.pack(fill='y', anchor="center", ipady=8)

window.mainloop()