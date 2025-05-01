"""
GUI LAYOUT AND WIDGET
"""
import tkinter as tk
from tkinter import ttk

"""
GLOBAL VARIABLES
"""
# String values that are allowed for the current app state
ALLOWED_APP_STATES = {'GENERATE', 'MANAGE', 'IDLE', 'CONNECTING'}
# Current app state: initially set to idle
CURRENT_STATE = 'IDLE'

"""
EVENT HANDLERS
"""

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
# This subframe will be added to the window initially, instead of other input subframes
input_idle_frame = ttk.Frame(io_frame)
current_io_frame = input_idle_frame # Keeps track of the current IO frame: IDLE at start
input_idle_frame.pack(side='top', expand=True, fill='x', ipady=30)
# Label widget
label_idle = tk.Label(input_idle_frame, text='CLICK ON THE LEFT BUTTONS TO CHOOSE AN ACTION!', font=('Courier New', 14), bg='#DEB887', fg='#556B2F', width=120)
label_idle.pack(side='top', expand=True, fill='both')

# Generating Report Widgets
# Report generator subframe (does not get packed at init)
input_generate_frame = ttk.Frame(io_frame)
# Report labels
label_reporttype = tk.Label(input_generate_frame, text='REPORT TYPE', font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
label_fname = tk.Label(input_generate_frame, text='FIRST NAME', font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
label_lname = tk.Label(input_generate_frame, text='LAST NAME', font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
# Report input widgets
listbox_reporttype = tk.Listbox(input_generate_frame, font=('Courier New', 14), bg='#DEB887', fg='#556B2F', selectmode='single')
listbox_reporttype.insert(0, 'Representative')
listbox_reporttype.insert(1, 'Customer')
entry_fname = tk.Entry(input_generate_frame, width=40, font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
entry_lname = tk.Entry(input_generate_frame, width=40, font=('Courier New', 14), bg='#DEB887', fg='#556B2F')


# Adding Representative Widgets


# Updating Customer Credit Limit Widgets


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