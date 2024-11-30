from tkinter import *

from PIL import Image, ImageTk  # Import Image and ImageTk from Pillow

class QuizSocApp:

    def __init__(self, root):

        self.root = root

        self.root.title("Quiz Soc")

        self.root.config(background="#FFCCCC")


        # Set window size to fill the screen

        screen_width = self.root.winfo_screenwidth()

        screen_height = self.root.winfo_screenheight()

        self.root.geometry(f"{screen_width}x{screen_height}")


        # Initialize the interface

        self.go_to_main_interface()


   

    def go_to_main_interface(self):

        # Clear the current interface

        for widget in self.root.winfo_children():

            widget.pack_forget()


        # Create a frame to center the buttons

        frame = Frame(self.root, background="#FFCCCC")

        frame.pack(expand=True)  # Center the frame vertically and horizontally


        # Add buttons to the frame

        button1 = Button(frame, text="SIGN IN", font=("Calibri", 30), width=15, height=2, command=self.go_to_third_interface, fg="skyblue", bg="yellow")

        button2 = Button(frame, text="SIGN UP", font=("Calibri", 30), width=15, height=2, command=self.go_to_second_interface, fg="skyblue", bg="yellow")


        button1.pack(pady=10)  # Add padding for spacing

        button2.pack(pady=10)


        # Resize and display the welcome image

        icon_path = r'C:\Users\Yagneswar\OneDrive\Desktop\VS_CODE\PYTHON\Project\logo.png'

        try:

            img = Image.open(icon_path)  # Open image using Pillow

            img = img.resize((200, 200))  # Resize image (width, height) to desired size

            icon = ImageTk.PhotoImage(img)  # Convert to Tkinter format


            self.root.iconphoto(True, icon)  # Set window icon

            label = Label(self.root, image=icon, text="WELCOME", compound="top", pady=10, font=("Calibri", 24), bg="#FFCCCC")

            label.image = icon  # Keep a reference to prevent garbage collection

            label.pack()

        except Exception as e:

            print(f"Error loading image: {e}")  # Debugging output

            label = Label(self.root, text="Image not found!", font=("Calibri", 20), bg="#FFCCCC")

            label.pack(pady=50)


    def go_to_second_interface(self):

        # Clear the current interface

        for widget in self.root.winfo_children():

            widget.pack_forget()


        # Add a label indicating the current interface

        label = Label(self.root, text="Sign Up - Enter your credentials:", font=("Calibri", 30), bg="#FFCCCC")

        label.pack(pady=20)


        # Add entry widgets for username and password

        self.signup_username = Entry(self.root, width=50, font=("Calibri", 14))

        self.signup_username.pack(pady=10, padx=40)

        self.signup_password = Entry(self.root, width=50, font=("Calibri", 14), show="*")

        self.signup_password.pack(pady=10, padx=40)


        # Add a Submit button for sign-up

        submit_button = Button(self.root, text="Sign Up", font=("Calibri", 14), command=self.save_signup_details, bg="#4CAF50", fg="white")

        submit_button.pack(pady=10)


        # Label for confirmation message

        self.signup_confirmation_label = Label(self.root, text="", font=("Calibri", 12), bg="#FFCCCC")

        self.signup_confirmation_label.pack(pady=5)


        # Add a back button

        back_button = Button(self.root, text="Back", font=("Calibri", 14), command=self.go_to_main_interface, bg="#f44336", fg="white")

        back_button.pack(pady=10)


    def save_signup_details(self):

        username = self.signup_username.get().strip()

        password = self.signup_password.get().strip()


        # Validate username format (must contain '@' and '.com')

        if "@" not in username or ".com" not in username:

            self.signup_confirmation_label.config(text="Username must contain '@' and '.com'", fg="red")

            return


        if username and password:

            try:

                # Save credentials to a file

                with open("user_credentials.txt", "a") as file:

                    file.write(f"{username},{password}\n")  # Store username and password

                self.signup_username.delete(0, END)  # Clear the Entry widget after saving

                self.signup_password.delete(0, END)

                self.signup_confirmation_label.config(text="Sign-up successful!", fg="green")

                self.root.after(3000, self.go_to_main_interface)


            except Exception as e:

                self.signup_confirmation_label.config(text=f"Error saving details: {e}", fg="red")

        else:

            self.signup_confirmation_label.config(text="Both fields are required.", fg="red")


    def go_to_third_interface(self):

        # Clear the current interface

        for widget in self.root.winfo_children():

            widget.pack_forget()


        # Add a label indicating the current interface

        label = Label(self.root, text="Login - Enter your credentials:", font=("Calibri", 30), bg="#FFCCCC")

        label.pack(pady=20)


        # Add entry widgets for username and password

        self.login_username = Entry(self.root, width=50, font=("Calibri", 14))

        self.login_username.pack(pady=10, padx=40)

        self.login_password = Entry(self.root, width=50, font=("Calibri", 14), show="*")

        self.login_password.pack(pady=10, padx=40)


        # Add a Submit button for login

        submit_button = Button(self.root, text="Login", font=("Calibri", 14), command=self.validate_login_details, bg="#4CAF50", fg="white")

        submit_button.pack(pady=10)


        # Label for confirmation message

        self.login_confirmation_label = Label(self.root, text="", font=("Calibri", 12), bg="#FFCCCC")

        self.login_confirmation_label.pack(pady=5)


        # Add a back button

        back_button = Button(self.root, text="Back", font=("Calibri", 14), command=self.go_to_main_interface, bg="#f44336", fg="white")

        back_button.pack(pady=10)


    def validate_login_details(self):

        username = self.login_username.get().strip()

        password = self.login_password.get().strip()


        # Check if the entered username and password match any saved credentials

        try:

            with open("user_credentials.txt", "r") as file:

                credentials = file.readlines()


            valid_user = False

            for credential in credentials:

                stored_username, stored_password = credential.strip().split(",")

                if username == stored_username and password == stored_password:

                    valid_user = True

                    break


            if valid_user:

                self.login_confirmation_label.config(text="Login successful!", fg="green")

                # After 3 seconds, go to the main interface (home page)

                self.root.after(3000, self.go_to_home_page)

            else:

                self.login_confirmation_label.config(text="Invalid username or password.", fg="red")

        except Exception as e:

            self.login_confirmation_label.config(text=f"Error reading file: {e}", fg="red")

    def go_to_home_page(self):

           

        # Clear the current interface

        for widget in self.root.winfo_children():

            widget.pack_forget()


        # Add a label indicating the current interface

        label = Label(self.root, text="Welcome to Quiz Test!!", font=("Calibri", 30), bg="#FFCCCC")

        label.pack(pady=20)        

        take_quiz_button = Button(self.root, text="Take a quiz: ", font=("Calibri", 14), command=self.take_quiz, bg="#4CAF50", fg="white")

        take_quiz_button.pack(pady=10)

        create_quiz__button = Button(self.root, text="Create quiz:", font=("Calibri", 14), command=self.create_quiz, bg="#4CAF50", fg="white")

        create_quiz__button.pack(pady=10)

        leaderboard_button = Button(self.root, text="Check leaderboard", font=("Calibri", 14), command=self.check_leaderboard, bg="#4CAF50", fg="white")

        leaderboard_button.pack(pady=10)

    def take_quiz(self):

        for widget in self.root.winfo_children():

            widget.pack_forget()


        mcq_button = Button(self.root, text="MCQ", font=("Calibri", 14), command=self.go_to_mcq_interface, bg="#f44336", fg="white")

        mcq_button.pack(pady=10)

        tf_button = Button(self.root, text="True/False", font=("Calibri", 14), command=self.go_to_tf_interface, bg="#f44336", fg="white")

        tf_button.pack(pady=10)

        sa_button = Button(self.root, text="Short Answer", font=("Calibri", 14), command=self.go_to_short_answer_interface, bg="#f44336", fg="white")

        sa_button.pack(pady=10)


        label = Label(self.root, text="Choose the quiz you want to take!!", font=("Calibri", 30), bg="#FFCCCC")

        label.pack(pady=20)

        back_button = Button(self.root, text="Back", font=("Calibri", 14), command=self.go_to_home_page, bg="#f44336", fg="white")

        back_button.pack(pady=10)

        home_button = Button(self.root, text="Home", font=("Calibri", 14),command=self.go_to_home_page, bg="#f44336", fg="white")

        home_button.pack(pady=10)


    def create_quiz(self):

    # Clear the current interface by destroying all existing widgets

        for widget in self.root.winfo_children():

            widget.destroy()  # Destroys the widget from the window


        # Now create and pack the new widgets

        q_mcq_button = Button(self.root, text="MCQ", font=("Calibri", 14), command=self.q_no_and_time_limit, bg="#f44336", fg="white")

        q_mcq_button.pack(pady=10)


        q_tf_button = Button(self.root, text="True/False", font=("Calibri", 14), command=self.q_no_and_time_limit, bg="#f44336", fg="white")

        q_tf_button.pack(pady=10)


        q_sa_button = Button(self.root, text="Short Answer", font=("Calibri", 14), command=self.q_no_and_time_limit, bg="#f44336", fg="white")

        q_sa_button.pack(pady=10)


        # Add a label indicating the current interface

        label = Label(self.root, text="Fill in the options!!", font=("Calibri", 30), bg="#FFCCCC")

        label.pack(pady=20)


        back_button = Button(self.root, text="Back", font=("Calibri", 14), command=self.go_to_home_page, bg="#f44336", fg="white")

        back_button.pack(pady=10)

        home_button = Button(self.root, text="Home", font=("Calibri", 14),command=self.go_to_home_page, bg="#f44336", fg="white")

        home_button.pack(pady=10)


    def check_leaderboard(self):

         # Clear the current interface

        for widget in self.root.winfo_children():

            widget.pack_forget()


        # Add a label indicating the current interface

        label = Label(self.root, text="Welcome to leaderboard!!", font=("Calibri", 30), bg="#FFCCCC")

        label.pack(pady=20)

        back_button = Button(self.root, text="Back", font=("Calibri", 14), command=self.go_to_home_page, bg="#f44336", fg="white")

        back_button.pack(pady=10)

        home_button = Button(self.root, text="Home", font=("Calibri", 14),command=self.go_to_home_page, bg="#f44336", fg="white")

        home_button.pack(pady=10)

    def go_to_intermediate(self):

        for widget in self.root.winfo_children():

            widget.pack_forget()

        a=Label(text=("You have selected to make a quiz that is",self.q_no," questions long and has a duration of ",self.q_time_limit,"minutes.")).pack()

        continue_button = Button(self.root, text="Continue", font=("Calibri", 14),command=self.go_to_home_page, bg="#f44336", fg="white")

        continue_button.pack(pady=10)

        self.root.after(3000, self.go_to_home_page)

        back_button = Button(self.root, text="Back", font=("Calibri", 14), command=self.go_to_home_page, bg="#f44336", fg="white")

        back_button.pack(pady=10)

        home_button = Button(self.root, text="Home", font=("Calibri", 14),command=self.go_to_home_page, bg="#f44336", fg="white")

        home_button.pack(pady=10)

    def q_no_and_time_limit(self):

        for widget in self.root.winfo_children():

            widget.pack_forget()

        label1 = Label(self.root, text="Select number of questions", font=("Calibri", 30), bg="#FFCCCC")

        label1.pack(pady=20)

        self.q_no = Entry(self.root, width=50, font=("Calibri", 14))

        self.q_no.pack(pady=10, padx=40)

        label2 = Label(self.root, text="Select time limit", font=("Calibri", 30), bg="#FFCCCC")

        label2.pack(pady=20)

        self.q_time_limit = Entry(self.root, width=50, font=("Calibri", 14))

        self.q_time_limit.pack(pady=10, padx=40)

        next_button = Button(self.root, text="Next", font=("Calibri", 14), command=self.go_to_intermediate, bg="#f44336", fg="white")

        next_button.pack(pady=10)

        home_button = Button(self.root, text="Home", font=("Calibri", 14),command=self.go_to_home_page, bg="#f44336", fg="white")

        home_button.pack(pady=10)

            

    def go_to_mcq_q_interface(self):

        for widget in self.root.winfo_children():

            widget.pack_forget()

        for i in range(self.q_no.get()):

            pass 

    def go_to_tf_interface(self):

        for widget in self.root.winfo_children():

            widget.pack_forget()

        home_button = Button(self.root, text="Home", font=("Calibri", 14),command=self.go_to_home_page, bg="#f44336", fg="white")

        home_button.pack(pady=10)

    def go_to_short_answer_interface(self):

        for widget in self.root.winfo_children():

            widget.pack_forget()

        home_button = Button(self.root, text="Home", font=("Calibri", 14),command=self.go_to_home_page, bg="#f44336", fg="white")

        home_button.pack(pady=10)

    def go_to_mcq_interface(self):

        for widget in self.root.winfo_children():

            widget.pack_forget()

        home_button = Button(self.root, text="Home", font=("Calibri", 14),command=self.go_to_home_page, bg="#f44336", fg="white")

        home_button.pack(pady=10)

    def go_to_tf_q_interface(self):

        for widget in self.root.winfo_children():

            widget.pack_forget()

    def go_to_q_short_answer_interface(self):

        for widget in self.root.winfo_children():

            widget.pack_forget()

        



# Create the main application window

root = Tk()


# Create an instance of the QuizSocApp class

app = QuizSocApp(root)


# Run the application

root.mainloop()