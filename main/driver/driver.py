import tkinter as tk
from errno import errorcode
from importlib.metadata import entry_points
from tkinter import ttk, messagebox
import main.database.connection.connection as connector
from main.database.scripts.update_customer import update_customer_credit
from main.database.scripts.add_representative import add_representative

class AppState:
    """Manages the application's state."""
    ALLOWED_UI_STATES = {
        'GENERATE',   # Generating a customer or representative report
        'ADD',        # Adding a new representative to the database
        'UPDATE',     # Updating a customer's credit limit in the database
        'IDLE',       # No current operations
    }

    # Constructor for the appstate object
    def __init__(self, initial_ui_state='IDLE'):
        if initial_ui_state not in self.ALLOWED_UI_STATES:
            raise ValueError(f"Invalid initial state: {initial_ui_state}")
        self._current_state = initial_ui_state

    @property
    def current(self):
        return self._current_state

    @current.setter
    def current(self, new_state):
        if new_state not in self.ALLOWED_UI_STATES:
            raise ValueError(f"Invalid state: {new_state}")
        self._current_state = new_state
        print(f"Application state changed to: {self._current_state}") # For debugging

class DatabaseState:
    """Manages the database's state."""
    ALLOWED_DB_STATES = {
        'CONNECTING',       # Currently connecting to the database
        'CONNECTED',        # Currently connected to the database
        'DISCONNECTED'      # Currently disconnected from the database
    }

    # Constructor for the state of the database
    def __init__(self, initial_db_state='DISCONNECTED'):
        if initial_db_state not in self.ALLOWED_DB_STATES:
            raise ValueError(f"Invalid initial state: {initial_db_state}")
        self._current_state = initial_db_state

    @property
    def current(self):
        return self._current_state

    @current.setter
    def current(self, new_state):
        if new_state not in self.ALLOWED_DB_STATES:
            raise ValueError(f"Invalid state: {new_state}")
        self._current_state = new_state
        print(f"Application state changed to: {self._current_state}") # For debugging

class IOFrame(ttk.Frame):
    """
    Manages the input/output area of the application.
    Outputs the reports in the center of the screen.
    Takes input dependent on the current app state on the right side of the screen.
    """
    # Constructor for the input/output frame
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.text_output = self._create_output_area()
        self.input_idle_frame = self._create_idle_input_frame()
        self.input_generate_frame = self._create_generate_input_frame()
        self.input_add_rep_frame = self._create_add_rep_input_frame()
        self.input_update_customer_frame = self._create_update_customer_input_frame()
        self.current_input_frame = self.input_idle_frame # Tracks the currently displayed input frame
        self.show_frame(self.current_input_frame)

    # Initializes the frame for the program output
    def _create_output_area(self):
        text_output = tk.Text(self, font=('Courier New', 14), width=100, bg='#FFE4C4', fg='#556B2F')
        text_output.insert(tk.END, 'OUTPUT TEXT WILL GO HERE!!')
        text_output.config(state='disabled')
        text_output.pack(side='left', expand=True, fill='both')
        return text_output

    # Input frame for when the appstate is set to IDLE
    def _create_idle_input_frame(self):
        frame = ttk.Frame(self)
        label = tk.Label(frame,
                         text='CLICK ON THE LEFT BUTTONS TO CHOOSE AN ACTION!', font=('Courier New', 14), bg='#DEB887',
                         fg='#556B2F', wraplength=280, justify='center')
        label.pack(side='top', expand=True, fill='both', ipady=30)
        frame.pack(side='top', expand=True, fill='y', ipady=30)
        return frame

    # Input frame for when the appstate is set to GENERATE
    # Takes the type of report as input and generates a report for either a specific customer or all reps
    def _create_generate_input_frame(self):
        frame = ttk.Frame(self)
        # Report labels
        label_reporttype = tk.Label(frame, text='REPORT TYPE', font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        label_fname = tk.Label(frame, text='CUSTOMER NAME', font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        #label_lname = tk.Label(frame, text='LAST NAME', font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        # Report input widgets
        self.listbox_reporttype = tk.Listbox(frame, font=('Courier New', 14), bg='#DEB887', fg='#556B2F', selectmode='single')
        self.listbox_reporttype.insert(0, 'Representative')
        self.listbox_reporttype.insert(1, 'Customer')
        self.report_entry_fname = tk.Entry(frame, width=30, font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        #self.report_entry_lname = tk.Entry(frame, width=30, font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        self.button_report_submit = tk.Button(frame, text='SUBMIT', font=('Courier New', 14), bg='#DEB887', fg='#556B2F',
                                    activebackground='#556B2F', activeforeground='#DEB887',
                                    command=self._handle_report_submit)
        # Pack input labels and widgets
        # Report type
        label_reporttype.pack(side='top', expand=True, fill='both')
        self.listbox_reporttype.pack(side='top', expand=True,fill='both')
        # First name
        label_fname.pack(side='top', expand=True,fill='both')
        self.report_entry_fname.pack(side='top', expand=True,fill='both')
        # Last name
        #label_lname.pack(side='top', expand=True,fill='both')
        #self.report_entry_lname.pack(side='top', expand=True,fill='both')
        # Submit buttons
        self.button_report_submit.pack(side='top', expand=True, fill='both')

        # Bind the selection event to a handler function
        self.listbox_reporttype.bind('<<ListboxSelect>>', self._handle_report_type_selection)
        return frame

    # Action event listener for selecting a report type
    # Used in the GENERATE appstate
    def _handle_report_type_selection(self, event):
        """Handles the selection change in the report type listbox."""
        selected_indices = self.listbox_reporttype.curselection()
        if selected_indices:
            selected_report = self.listbox_reporttype.get(selected_indices[0])
            if selected_report == 'Representative':
                self.report_entry_fname.config(state='disabled', disabledbackground='#DEB887')
                #self.report_entry_lname.config(state='disabled', disabledbackground='#DEB887')
            else:
                self.report_entry_fname.config(state='normal', bg='#DEB887')
                #self.report_entry_lname.config(state='normal', bg='#DEB887')

    # Action event listener for the submit button
    # Used in the GENERATE appstate
    def _handle_report_submit(self):
        # Clear output area
        self.text_output.config(state='normal')
        self.text_output.delete('1.0', tk.END)

        selected_indices = self.listbox_reporttype.curselection()
        if not selected_indices:
            self.text_output.insert(tk.END, "Please select a report type.\n")
            self.text_output.config(state='disabled')
            return

        report_type = self.listbox_reporttype.get(selected_indices[0])

        if report_type == 'Representative':
            from main.database.scripts.reports import generate_representative_report
            try:
                report = generate_representative_report()
                self.text_output.insert(tk.END, report)
            except Exception as e:
                self.text_output.insert(tk.END, f"Error generating representative report:\n{e}")
        elif report_type == 'Customer':
            from main.database.scripts.reports import generate_customer_report
            name = self.report_entry_fname.get().strip()
            if not name:
                self.text_output.insert(tk.END, "Please enter a customer name.\n")
            else:
                try:
                    report = generate_customer_report(name)
                    self.text_output.insert(tk.END, report)
                except Exception as e:
                    self.text_output.insert(tk.END, f"Error generating customer report:\n{e}")

        self.text_output.config(state='disabled')

    # Input frame for when the appstate is set to ADD
    # Takes input to create a new Rep in the database
    def _create_add_rep_input_frame(self):
        frame = tk.Frame(self)
        # Representative input labels
        label_fname = tk.Label(frame, text='FIRST NAME', font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        label_lname = tk.Label(frame, text='LAST NAME', font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        label_street = tk.Label(frame, text='STREET', font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        label_city = tk.Label(frame, text='CITY', font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        label_state = tk.Label(frame, text='STATE', font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        label_postalcode = tk.Label(frame, text='POSTAL CODE', font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        label_commission = tk.Label(frame, text='COMMISSION($)', font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        label_rate = tk.Label(frame, text='RATE(%)', font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        # Representative input entries
        self.entry_fname = tk.Entry(frame, font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        self.entry_lname = tk.Entry(frame, font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        self.entry_street = tk.Entry(frame, font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        self.entry_city = tk.Entry(frame, font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        self.entry_state = tk.Entry(frame, font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        self.entry_postalcode = tk.Entry(frame, font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        self.entry_commission = tk.Entry(frame, font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        self.entry_rate = tk.Entry(frame, font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        # Button for submitting the changes to the database
        self.button_add_submit = tk.Button(frame, text='SUBMIT', font=('Courier New', 14), bg='#DEB887', fg='#556B2F',
                                  activebackground='#556B2F', activeforeground='#DEB887',
                                  command=self._handle_add_submit)
        # Packing the add_rep widgets
        label_fname.pack(side='top', expand=True, fill='both')
        self.entry_fname.pack(side='top', expand=True, fill='both')
        label_lname.pack(side='top', expand=True, fill='both')
        self.entry_lname.pack(side='top', expand=True, fill='both')
        label_street.pack(side='top', expand=True, fill='both')
        self.entry_street.pack(side='top', expand=True, fill='both')
        label_city.pack(side='top', expand=True, fill='both')
        self.entry_city.pack(side='top', expand=True, fill='both')
        label_state.pack(side='top', expand=True, fill='both')
        self.entry_state.pack(side='top', expand=True, fill='both')
        label_postalcode.pack(side='top', expand=True, fill='both')
        self.entry_postalcode.pack(side='top', expand=True, fill='both')
        label_commission.pack(side='top', expand=True, fill='both')
        self.entry_commission.pack(side='top', expand=True, fill='both')
        label_rate.pack(side='top', expand=True, fill='both')
        self.entry_rate.pack(side='top', expand=True, fill='both')
        self.button_add_submit.pack(side='top', expand=True, fill='both')

        return frame

    # Action event listener for the submit button
    # Used when the appstate is set to ADD
    def _handle_add_submit(self):
        try:
            # collect input values
            first_name = self.entry_fname.get()
            last_name = self.entry_lname.get()
            street = self.entry_street.get()
            city = self.entry_city.get()
            state = self.entry_state.get()
            postal_code = self.entry_postalcode.get()
            commission = self.entry_commission.get()
            rate = self.entry_rate.get()

            # try to convert numeric fields
            postal_code = int(postal_code) if postal_code else None
            commission = float(commission) if commission else None
            rate = float(rate) if rate else None

            # call add_representative
            result = add_representative(connector.conn, first_name, last_name, street, city, state, postal_code, commission, rate)

            # display result in popup
            if result == "Representative Added":
                messagebox.showinfo("Success", result)
            else:
                messagebox.showerror("Error", result)

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid numeric input: {e}")

    # Input frame for when the appstate is UPDATE
    # Takes input to update a customer's credit limit in the database
    def _create_update_customer_input_frame(self):
        frame = tk.Frame(self)
        # Labels
        label_customer_name = tk.Label(frame, text='CUSTOMER NAME', font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        label_customer_credit = tk.Label(frame, text='NEW CREDIT LIMIT ($)', font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        # Entries
        self.entry_customer_name = tk.Entry(frame, font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        self.entry_customer_credit = tk.Entry(frame, font=('Courier New', 14), bg='#DEB887', fg='#556B2F')
        # Sumbit button
        self.button_update_submit = tk.Button(frame, text='UPDATE', font=('Courier New', 14), bg='#DEB887', fg='#556B2F',
                                  activebackground='#556B2F', activeforeground='#DEB887',
                                  command=self._handle_update_submit)
        # Pack all widgets
        label_customer_name.pack(side='top', expand=True, fill='both')
        self.entry_customer_name.pack(side='top', expand=True, fill='both')
        label_customer_credit.pack(side='top', expand=True, fill='both')
        self.entry_customer_credit.pack(side='top', expand=True, fill='both')
        self.button_update_submit.pack(side='top', expand=True, fill='both')

        return frame

    # Action event listener for the submit button
    # Used when the appstate is set to UPDATE
    def _handle_update_submit(self):
        input_name = None
        input_limit = None

        try:
            input_name = str(self.entry_customer_name.get())
            input_limit = int(self.entry_customer_credit.get())
        except ValueError:
            tk.messagebox.showerror('Invalid input', 'Please enter the correct kind of input.')
            return

        if input_name == None or input_limit == None:
            tk.messagebox.showerror('Error', 'Please enter your customer name and/or credit limit.')
        else:
            try:
                update_customer_credit(connector.conn, input_name, input_limit)
                tk.messagebox.showinfo('Success', 'Customer limit has been updated.')
            except Exception as e:
                tk.messagebox.showerror('Error', 'Either a customer with that name doesnt exist or you entered an invalid credit limit.')
                print(e)

    # Changes the input frame dependent on the current appstate
    def show_frame(self, target_frame):
        """Brings the specified input frame to the front."""
        if self.current_input_frame:
            self.current_input_frame.pack_forget()
        target_frame.pack(side='top', expand=True, fill='both')
        self.current_input_frame = target_frame

    # Changes the text displayed in the output frame
    def set_output_text(self, message):
        """Sets the content of the output text area."""
        self.text_output.config(state='normal')  # Enable editing
        self.text_output.delete('1.0', tk.END)  # Clear existing content
        self.text_output.insert(tk.END, message)  # Insert new message
        self.text_output.config(state='disabled')  # Disable editing again


class MenuFrame(ttk.Frame):
    """Manages the sidebar menu buttons."""
    # Constuctor for the menu frame on the left side of the app
    def __init__(self, parent, io_frame, app_state, db_state, **kwargs):
        super().__init__(parent, **kwargs)
        self.io_frame = io_frame
        self.app_state = app_state
        self.db_state = db_state
        self._create_buttons()

    # Creates the menu buttons and sets their events
    def _create_buttons(self):
        button_config = [
            {'text': 'CONNECT', 'command': self._handle_connect},
            {'text': 'GENERATE', 'command': self._handle_generate},
            {'text': 'ADD', 'command': self._handle_add_rep},
            {'text': 'UPDATE', 'command': self._handle_update_customer},
            {'text': 'EXIT', 'command': self._handle_exit}
        ]
        for config in button_config:
            button = tk.Button(self, text=config['text'], font=('Courier New', 24, 'bold'),
                               bg='#DEB887', fg='#556B2F', activebackground='#556B2F',
                               activeforeground='#DEB887', command=config['command'])
            button.pack(side='top', expand=True, fill='both')

    # Action event handler for the CONNECT menu button
    # Attempts to connect to the database
    # Shows a message that states whether the connection was successful or unsuccessful
    def _handle_connect(self):
        if self.db_state.current != 'CONNECTING' or self.app_state.current != 'CONNECTED':
            self.db_state.current = 'CONNECTING'
            if (connector.connect()):
                self._create_messagebox('info', 'Connected', 'Successfully established connection.')
                self.db_state.current = 'CONNECTED'
            else:
                messagebox.showerror('Connection Error', 'Failed to connect to MySQL database')
                self.db_state.current = 'DISCONNECTED'
        else:
            print("Already connecting...")

    # Action event handler for the GENERATE menu button
    # Changes the appstate to GENERATE
    def _handle_generate(self):
        if self.app_state.current != 'GENERATE':
            self.app_state.current = 'GENERATE'
            self.io_frame.show_frame(self.io_frame.input_generate_frame)
        else:
            print("Already in GENERATE state.")

    # Action event handler for the ADD menu button
    # Changes the appstate to ADD
    def _handle_add_rep(self):
        if self.app_state.current != 'ADD':
            self.app_state.current = 'ADD'
            self.io_frame.show_frame(self.io_frame.input_add_rep_frame)
        else:
            print("Already in ADD state.")

    # Action event handler for the UPDATE menu button
    # Changes the appstate to UPDATE
    def _handle_update_customer(self):
        if self.app_state.current != 'UPDATE':
            self.app_state.current = 'UPDATE'
            self.io_frame.show_frame(self.io_frame.input_update_customer_frame)
        else:
            print("Already in UPDATE state.")

    # Action event handler for the EXIT menu button
    # Closes the program
    def _handle_exit(self):
        root.destroy()

    # Creates a messagebox with variable types
    def _create_messagebox(self, type, title, message):
        if (type == 'error'):
            messagebox.showerror(title, message)
        elif (type == 'info'):
            messagebox.showinfo(title, message)
        elif (type == 'warning'):
            messagebox.showwarning(title, message)
        else:
            messagebox.showerror(title, message)

class ContentFrame(tk.Frame):
    """Manages the main content area, holding the menu and IO frames."""
    # Constuctor for the ContentFrame object
    def __init__(self, parent, app_state, db_state, **kwargs):
        super().__init__(parent, **kwargs)
        self.app_state = app_state
        self.db_state = db_state
        self.io_frame = IOFrame(self)
        self.menu_frame = MenuFrame(self, self.io_frame, self.app_state, self.db_state)
        self._layout()

    # Defines the layout of the app
    def _layout(self):
        self.menu_frame.pack(side='left', expand=True, fill='both')
        self.io_frame.pack(side='left', expand=True, fill='both')

class DatabaseApp(tk.Tk):
    """The main application window."""
    # Constructor for the application object
    def __init__(self):
        super().__init__()
        self.title('CFG DATABASE APPLICATION')
        self.state('zoomed') # Makes the window start as a windowed fullscreen app
        self.app_state = AppState()
        self.db_state = DatabaseState()
        self.content_frame = ContentFrame(self, self.app_state, self.db_state)
        self.content_frame.pack(fill='both', expand=True)

"""RUNNING THE PROJECT"""
if __name__ == "__main__":
    root = DatabaseApp()
    root.mainloop()