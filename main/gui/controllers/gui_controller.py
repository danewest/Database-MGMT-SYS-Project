"""
GUI LAYOUT AND WIDGET
"""

import tkinter as tk
from tkinter import ttk

"""
ROOT WINDOW INIT
"""
root = tk.Tk()
root.title('CFG DATABASE APPLICATION')
root.geometry('960x540')

"""
CONTENT FRAME INIT
"""
content_frame = tk.Frame(root)

"""
SUBFRAME LAYOUTS
"""
# Sidebar menu
menu_frame = ttk.Frame(content_frame)

# Input and Output of DB operations
io_frame = ttk.Frame(content_frame)

"""
MENU SUBFRAME WIDGETS
"""
# Connect to DB button
button_connection = tk.Button(menu_frame, text='CONNECT', font=('Courier New', 24, 'bold'), bg='#DEB887', fg='#556B2F', activebackground='#556B2F', activeforeground='#DEB887')
button_connection.pack(side='top', expand=True, fill='both')

# Generate reports button
button_generate_report = tk.Button(menu_frame, text='GENERATE', font=('Courier New', 24, 'bold'), bg='#DEB887', fg='#556B2F', activebackground='#556B2F', activeforeground='#DEB887')
button_generate_report.pack(side='top', expand=True, fill='both')

# Manage button
button_manage = tk.Button(menu_frame, text='MANAGE', font=('Courier New', 24, 'bold'), bg='#DEB887', fg='#556B2F', activebackground='#556B2F', activeforeground='#DEB887')
button_manage.pack(side='top', expand=True, fill='both')

# Exit button
button_exit = tk.Button(menu_frame, text='EXIT', font=('Courier New', 24, 'bold'), bg='#DEB887', fg='#556B2F', activebackground='#556B2F', activeforeground='#DEB887')
button_exit.pack(side='top', expand=True, fill='both')

"""
OUTPUT SUBFRAME WIDGETS
"""
# Text output
# Used to store the generated reports
text_output = tk.Text(io_frame, font=('Courier New', 14), bg='#FFE4C4', fg='#556B2F')
text_output.insert(tk.END, 'OUTPUT TEXT WILL GO HERE!!')
text_output.config(state='disabled')
text_output.pack(side='top', expand=True, fill='both')

"""
INPUT SUBFRAME WIDGETS
"""
# Idle Widgets
# Initial subframe of widgets to be displayed when opening the app
input_idle_frame = ttk.Frame(io_frame)
input_idle_frame.pack(side='top', expand=True, fill='x', ipady=30)
# Label widget
label_input_idle = tk.Label(input_idle_frame, text='CLICK ON THE LEFT BUTTONS TO CHOOSE AN ACTION!', font=('Courier New', 14), bg='#DEB887', fg='#556B2F', width=120)
label_input_idle.pack(side='top', expand=True, fill='both')

# Generating Report Widgets


# Adding Representative Widgets


# Updating Customer Credit Limit Widgets


"""
PACKING SUBFRAMES TO THE CONTENT FRAME
"""
menu_frame.pack(side='left', expand=True, fill='both')
io_frame.pack(side='left', expand=True, fill='both')

"""
PACKING CONTENT FRAME TO THE ROOT WINDOW
"""
content_frame.pack(fill='both', expand=True)

"""
RUN THE APPLICATION
"""
root.mainloop()