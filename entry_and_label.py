from tkinter import *
from PIL import Image, ImageTk  # Import Image and ImageTk from Pillow
import os

class QuizSocApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Soc")
        self.root.config(background="#FFCCCC")

        # Set window size to fill the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")

        # Sample leaderboard data
        self.quiz_scores = {
            "Math Quiz": [("Alice", 95), ("Bob", 85), ("Charlie", 75)],
            "Science Quiz": [("Alice", 90), ("Charlie", 80), ("David", 70)],
            "History Quiz": [("Bob", 88), ("Alice", 76), ("Charlie", 90)],
        }

        # Initialize the interface
        self.go_to_main_interface()

    def go_to_main_interface(self):
        # Clear the current interface
        for widget in self.root.winfo_children():
            widget.destroy()

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
        for widget in self.root.winfo_children():
            widget.destroy()

        # Add a label indicating the current interface
        label = Label(self.root, text="Sign Up - Enter your credentials:", font=("Calibri", 30), bg="#FFCCCC")
        label.pack(pady=20)

        # Add a label and entry for username (Email)
        email_label = Label(self.root, text="Email:", font=("Calibri", 16), bg="#FFCCCC")
        email_label.pack(pady=5)
        self.signup_username = Entry(self.root, width=50, font=("Calibri", 14))
        self.signup_username.pack(pady=10, padx=40)

        # Add a label and entry for password
        password_label = Label(self.root, text="Password:", font=("Calibri", 16), bg="#FFCCCC")
        password_label.pack(pady=5)
        self.signup_password = Entry(self.root, width=50, font=("Calibri", 14), show="*")
        self.signup_password.pack(pady=10, padx=40)

        # Add a "Show Password" checkbox
        self.show_signup_password = BooleanVar()
        show_password_check = Checkbutton(self.root, text="Show Password", variable=self.show_signup_password, command=self.toggle_signup_password, font=("Calibri", 14), bg="#FFCCCC")
        show_password_check.pack(pady=5)

        # Add a Submit button for sign-up
        submit_button = Button(self.root, text="Sign Up", font=("Calibri", 14), command=self.save_signup_details, bg="#4CAF50", fg="white")
        submit_button.pack(pady=10)

        # Label for confirmation message
        self.signup_confirmation_label = Label(self.root, text="", font=("Calibri", 12), bg="#FFCCCC")
        self.signup_confirmation_label.pack(pady=5)

        # Add a back button
        back_button = Button(self.root, text="Back", font=("Calibri", 14), command=self.go_to_main_interface, bg="#f44336", fg="white")
        back_button.pack(pady=10)


    def toggle_signup_password(self):
        # Toggle password visibility based on checkbox
        if self.show_signup_password.get():
            self.signup_password.config(show="")
        else:
            self.signup_password.config(show="*")

    def save_signup_details(self):
        username = self.signup_username.get().strip()
        password = self.signup_password.get().strip()

        # Validate username format (must contain '@' and '.com')
        if "@" not in username or "gmail.com" not in username:
            self.signup_confirmation_label.config(text="Invalid email address.", fg="red")
            return

        if " " in username:
            self.signup_confirmation_label.config(text="Email cannot contain spaces.", fg="red")
            return

        # Ensure the file exists
        if not os.path.exists("user_credentials.txt"):
            with open("user_credentials.txt", "w") as file:
                pass  # Create the file if it does not exist

        # Check if the email already exists in the file
        try:
            with open("user_credentials.txt", "r") as file:
                credentials = file.readlines()

            # Check for existing email
            for credential in credentials:
                stored_username, _ = credential.strip().split(",")
                if username == stored_username:
                    self.signup_confirmation_label.config(text="Email already taken.", fg="red")
                    return

            # If email doesn't exist, proceed with saving the credentials
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
        except Exception as e:
            self.signup_confirmation_label.config(text=f"Error reading file: {e}", fg="red")


    def go_to_third_interface(self):
    # Clear the current interface
        for widget in self.root.winfo_children():
            widget.destroy()

        # Add a label indicating the current interface
        label = Label(self.root, text="Login - Enter your credentials:", font=("Calibri", 30), bg="#FFCCCC")
        label.pack(pady=20)

        # Add a label and entry for username (Email)
        email_label = Label(self.root, text="Email:", font=("Calibri", 16), bg="#FFCCCC")
        email_label.pack(pady=5)
        self.login_username = Entry(self.root, width=50, font=("Calibri", 14))
        self.login_username.pack(pady=10)

        # Add a label and entry for password
        password_label = Label(self.root, text="Password:", font=("Calibri", 16), bg="#FFCCCC")
        password_label.pack(pady=5)
        self.login_password = Entry(self.root, width=50, font=("Calibri", 14), show="*")
        self.login_password.pack(pady=10)

        # Add a "Show Password" checkbox
        self.show_login_password = BooleanVar()
        show_password_check = Checkbutton(self.root, text="Show Password", variable=self.show_login_password, command=self.toggle_login_password, font=("Calibri", 14), bg="#FFCCCC")
        show_password_check.pack(pady=5)

        # Add a Submit button for login
        submit_button = Button(self.root, text="Login", font=("Calibri", 14), command=self.validate_login_details, bg="#4CAF50", fg="white")
        submit_button.pack(pady=10)

        # Label for confirmation message
        self.login_confirmation_label = Label(self.root, text="", font=("Calibri", 12), bg="#FFCCCC")
        self.login_confirmation_label.pack(pady=5)

        # Add a back button
        back_button = Button(self.root, text="Back", font=("Calibri", 14), command=self.go_to_main_interface, bg="#f44336", fg="white")
        back_button.pack(pady=10)

    def toggle_login_password(self):
        # Toggle password visibility based on checkbox
        if self.show_login_password.get():
            self.login_password.config(show="")
        else:
            self.login_password.config(show="*")

    def validate_login_details(self):
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()

        # Ensure the file exists
        if not os.path.exists("user_credentials.txt"):
            self.login_confirmation_label.config(text="No users found. Please sign up first.", fg="red")
            return

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
            widget.destroy()

        # Add a label indicating the current interface
        label = Label(self.root, text="Welcome to Quiz Test!!", font=("Calibri", 30), bg="#FFCCCC")
        label.pack(pady=20)
        submit_button = Button(self.root, text="TAKE QUIZ", font=("Calibri", 14), command=self.take_quiz, bg="#4CAF50", fg="white")
        submit_button.pack(pady=10)
        submit_button = Button(self.root, text="CREATE QUIZ", font=("Calibri", 14), command=self.create_quiz, bg="#4CAF50", fg="white")
        submit_button.pack(pady=10)
        submit_button = Button(self.root, text="LEADERBOARD", font=("Calibri", 14), command=self.check_leaderboard, bg="#4CAF50", fg="white")
        submit_button.pack(pady=10)

    def take_quiz(self):
        # Clear the current interface
        for widget in self.root.winfo_children():
            widget.destroy()

        # Add a label indicating the current interface
        label = Label(self.root, text="Choose the quiz you want to take!!", font=("Calibri", 30), bg="#FFCCCC")
        label.pack(pady=20)

    def create_quiz(self):
        # Clear the current interface
        for widget in self.root.winfo_children():
            widget.destroy()

        # Add a label indicating the current interface
        label = Label(self.root, text="Fill in the options!!", font=("Calibri", 30), bg="#FFCCCC")
        label.pack(pady=20)

    def check_leaderboard(self):
        # Clear the current interface
        for widget in self.root.winfo_children():
            widget.destroy()

        # Add a label indicating the current interface
        label = Label(self.root, text="Select a Quiz to View Leaderboard:", font=("Calibri", 30), bg="#FFCCCC")
        label.pack(pady=20)

        # Add buttons for each quiz
        for quiz_name in self.quiz_scores.keys():
            quiz_button = Button(self.root, text=quiz_name, font=("Calibri", 14), command=lambda q=quiz_name: self.show_leaderboard(q), bg="#4CAF50", fg="white")
            quiz_button.pack(pady=10)

        # Add a back button
        back_button = Button(self.root, text="Back", font=("Calibri", 14), command=self.go_to_home_page, bg="#f44336", fg="white")
        back_button.pack(pady=10)

    def show_leaderboard(self, quiz_name):
        # Clear the current interface
        for widget in self.root.winfo_children():
            widget.destroy()

        # Add a label for the quiz leaderboard
        label = Label(self.root, text=f"Leaderboard - {quiz_name}", font=("Calibri", 30), bg="#FFCCCC")
        label.pack(pady=20)

        # Fetch leaderboard data and sort it
        scores = self.quiz_scores[quiz_name]
        scores = sorted(scores, key=lambda x: x[1], reverse=True)  # Sort by score, descending

        # Add leaderboard header
        header = Label(self.root, text="Name\t\tScore\t\tRank", font=("Calibri", 16), bg="#FFCCCC", anchor="w", justify="left")
        header.pack(pady=10)

        # Add scores to the leaderboard
        for rank, (name, score) in enumerate(scores, start=1):
            row = Label(self.root, text=f"{name}\t\t{score}\t\t{rank}", font=("Calibri", 14), bg="#FFCCCC", anchor="w", justify="left")
            row.pack()

        # Add a back button
        back_button = Button(self.root, text="Back", font=("Calibri", 14), command=self.check_leaderboard, bg="#f44336", fg="white")
        back_button.pack(pady=20)


# Create the main application window
root = Tk()

# Create an instance of the QuizSocApp class
app = QuizSocApp(root)

# Run the application
root.mainloop()
