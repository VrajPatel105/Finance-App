from tkinter import *
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
            messagebox.showinfo('Success', 'Login Successful')
            self.home_gui()
        else:
            messagebox.showerror('Error', 'Incorrect Email/Password')


    # since we have to clean the gui a lot of times, we are creating a function.
    def clear_gui(self):
        for i in self.root.pack_slaves():
            i.destroy()


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

    def home_gui(self):
        self.clear_gui()

        
    
FinanceApp()