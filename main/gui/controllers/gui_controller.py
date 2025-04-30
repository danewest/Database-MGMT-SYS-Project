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

# Output of DB operations
output_frame = ttk.Frame(content_frame)

# Input for the DB operations
input_frame = ttk.Frame(content_frame)

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
text_output = tk.Text(output_frame, font=('Courier New', 14), bg='#FFE4C4', fg='#556B2F')
text_output.insert(tk.END, 'OUTPUTED TEXT WILL GO HERE!!')
text_output.config(state='disabled')
text_output.pack(side='left', expand=True, fill='both')

"""
INPUT SUBFRAME WIDGETS
"""
# Idle Widgets
# Initial subframe of widgets to be displayed when opening the app
def init_idle_widget():
    pass

# Generating Report Widgets
def init_generate_widget():
    pass
# Adding Representative Widgets
def init_add_rep_widget():
    pass

# Updating Customer Credit Limit Widgets
def init_update_credit_widget():
    pass

"""
PACKING SUBFRAMES TO THE CONTENT FRAME
"""
menu_frame.pack(side='left', expand=True, fill='both')
output_frame.pack(side='left', expand=True, fill='both')

"""
PACKING CONTENT FRAME TO THE ROOT WINDOW
"""
content_frame.pack(fill='both', expand=True)

"""
RUN THE APPLICATION
"""
root.mainloop()