from tkinter import *
import tkinter as tk
from tkinter import messagebox
from mydatabase import Database
from app import App



class FinanceApp:

    def __init__(self):

        self.dbo = Database()
        self.app = App() # Rhs value
        self.root = Tk()
        self.root.title('Algorithmic Trading')
        self.root.iconbitmap('resources/financeapp.ico')
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#2c3e50')  # Dark background for contrast

        self.login_gui()

        self.root.mainloop()

    def login_gui(self):
        self.clear_gui()

        # Frame for centering the login GUI
        frame = Frame(self.root, bg='#34495e', padx=40, pady=40)
        frame.place(relx=0.5, rely=0.5, anchor='center')  # Center the frame


        # Heading
        heading = Label(
            frame, text='Algo Trading', bg='#34495e', fg='#ecf0f1',
            font=('Verdana', 24, 'bold'))
        heading.pack(pady=(10, 20))

        # Email Input
        label1 = Label(
            frame, text='Enter Email', bg='#34495e', fg='#ecf0f1',
            font=('Verdana', 12))
        label1.pack(pady=(10, 5))
        self.email_input = Entry(frame, width=40, font=('Verdana', 12))
        self.email_input.pack(pady=(5, 10), ipady=5)

        # Password Input
        label2 = Label(
            frame, text='Enter Password', bg='#34495e', fg='#ecf0f1',
            font=('Verdana', 12))
        label2.pack(pady=(10, 5))
        self.password_input = Entry(frame, width=40, font=('Verdana', 12), show='*')
        self.password_input.pack(pady=(5, 10), ipady=5)

        # Login Button
        login_button = Button(
            frame, text='Login', bg='#27ae60', fg='white',
            font=('Verdana', 12, 'bold'), width=15, height=1,
            command=self.perform_login)
        login_button.pack(pady=(15, 10))

        # Register Section
        label3 = Label(
            frame, text='Not a member?', bg='#34495e', fg='#ecf0f1',
            font=('Verdana', 10))
        label3.pack(pady=(10, 5))

        redirect_button = Button(
            frame, text='Register Now', bg='#2980b9', fg='white',
            font=('Verdana', 10, 'bold'), command=self.register_gui)
        redirect_button.pack(pady=(5, 10))

        quit_button = Button(
            frame, text='Quit', bg='#e74c3c', fg='white',
            font=('Verdana', 10, 'bold'), command=self.root.destroy)
        quit_button.pack(pady=(5, 10))



    def register_gui(self):
        frame = Frame(self.root, bg='#34495e', padx=40, pady=40)
        frame.place(relx=0.5, rely=0.5, anchor='center')  # Center the frame

        # Heading
        heading = Label(
            frame, text='Algo Trading', bg='#34495e', fg='#ecf0f1',
            font=('Verdana', 24, 'bold'))
        heading.pack(pady=(10, 20))

        # Name Input
        label0 = Label(
            frame, text='Enter Name', bg='#34495e', fg='#ecf0f1',
            font=('Verdana', 12))
        label0.pack(pady=(10, 5))
        self.name_input = Entry(frame, width=40, font=('Verdana', 12))
        self.name_input.pack(pady=(5, 10), ipady=5)

        # Email Input
        label1 = Label(
            frame, text='Enter Email', bg='#34495e', fg='#ecf0f1',
            font=('Verdana', 12))
        label1.pack(pady=(10, 5))
        self.email_input = Entry(frame, width=40, font=('Verdana', 12))
        self.email_input.pack(pady=(5, 10), ipady=5)

        # Password Input
        label2 = Label(
            frame, text='Enter Password', bg='#34495e', fg='#ecf0f1',
            font=('Verdana', 12))
        label2.pack(pady=(10, 5))
        self.password_input = Entry(frame, width=40, font=('Verdana', 12), show='*')
        self.password_input.pack(pady=(5, 10), ipady=5)

        label3 = Label(
            frame, text='Confirm Password', bg='#34495e', fg='#ecf0f1',
            font=('Verdana', 12))
        label3.pack(pady=(10, 5))
        self.confirm_password_input = Entry(frame, width=40, font=('Verdana', 12), show='*')
        self.confirm_password_input.pack(pady=(5, 10), ipady=5)
        
        register_button = Button(
            frame, text='Register', bg='#27ae60', fg='white',
            font=('Verdana', 12, 'bold'), width=15, height=1,
            command=self.perform_registration)
        register_button.pack(pady=(15, 10))

        quit_button = Button(
            frame, text='Quit', bg='#e74c3c', fg='white',
            font=('Verdana', 10, 'bold'), command=self.root.destroy)
        quit_button.pack(pady=(5, 10))

        

    def perform_login(self):
        email = self.email_input.get()
        password = self.password_input.get()
        
        rhs_response = self.dbo.search_rhs_value(email)
        response = self.dbo.search(rhs_response,password)
        
        if response:
            #messagebox.showinfo('Success', 'Login Successful')
            self.home_gui()
        else:
            messagebox.showerror('Error', 'Incorrect Email/Password')



    # since we have to clean the gui a lot of times, we are creating a function.
    def clear_gui(self, container=None):
        if container is None:
            container = self.root
        for widget in container.pack_slaves():
            widget.destroy()


    def perform_registration(self):
        name = self.name_input.get()
        email = self.email_input.get()
        password = self.password_input.get()
        confirm_password = self.confirm_password_input.get()
        rhs_value = self.app.rhs_number()

        response = self.dbo.add_data(name,password,confirm_password,rhs_value)
        response_rhs_val = self.dbo.add_rhs_val(email,rhs_value)

        if response:
            messagebox.showinfo('Success',f'Registration Sucessfull. Your RHS Number is: {response_rhs_val}')
            self.login_gui()
        else:
            messagebox.showerror('Error','User already exists or the entered password dosent match')

    def logout(self):
        # Close the home window and show the login window again
        self.home_window.destroy()
        self.root.deiconify()
        self.login_gui()

    def create_sidebar(self):
        # Sidebar frame
        sidebar = tk.Frame(self.root, bg='#1a237e', width=250)
        sidebar.grid(row=0, column=0, sticky='nsew', rowspan=2)
        sidebar.grid_propagate(False)
        
        # User profile section
        profile_frame = tk.Frame(sidebar, bg='#1a237e')
        profile_frame.pack(pady=20, padx=10, fill='x')
        
        tk.Label(profile_frame, text="Welcome, Trader", 
                fg='white', bg='#1a237e', font=('Helvetica', 14, 'bold')).pack()
        tk.Label(profile_frame, text="Balance: $100,000", 
                fg='#90caf9', bg='#1a237e', font=('Helvetica', 12)).pack()
        
        # Navigation buttons
        nav_buttons = [
            ("Dashboard", "🏠"),
            ("Portfolio", "📊"),
            ("Trade", "💱"),
            ("Analytics", "📈"),
            ("Settings", "⚙️")
        ]
        
        for text, icon in nav_buttons:
            btn = tk.Button(sidebar, text=f"{icon} {text}", 
                          bg='#283593', fg='white',
                          font=('Helvetica', 12),
                          bd=0, pady=10, width=20)
            btn.pack(pady=5, padx=10)

    def home_gui(self):

        self.root.withdraw()
        self.create_sidebar()

        # Home GUI in a new Toplevel window
        self.home_window = tk.Toplevel()
        self.home_window.title("Home")
        self.home_window.configure(bg='#2c3e50')

        # Set fullscreen attribute
        self.home_window.attributes('-fullscreen', True)

        tk.Label(self.home_window, text="Welcome to the Home Page!", bg='#2c3e50', fg='#ecf0f1',
                font=('Verdana', 24, 'bold')).pack(pady=20)

        # Button to log out and return to the login screen
        tk.Button(self.home_window, text='Logout', command=self.logout, bg='#c0392b', fg='white',
                font=('Verdana', 12, 'bold')).pack(pady=10)

        
    
FinanceApp()