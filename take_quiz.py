import tkinter as tk
from tkinter import messagebox
import csv
import os
import create_quiz_  # Import the create_quiz_ module for quiz creation

class QuizTakingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Taking App")
        self.quiz = None
        self.user_answers = []
        self.current_question_index = 0
        self.username = ""  # Initialize username as an empty string
        
        self.ask_for_username()

    def ask_for_username(self):
        """Ask the user for their name before proceeding to the quiz selection."""
        self.username_label = tk.Label(self.root, text="Please enter your name:", font=("Arial", 14))
        self.username_label.pack(pady=20)
        
        self.username_entry = tk.Entry(self.root, font=("Arial", 14))
        self.username_entry.pack(pady=10)
        
        self.submit_button = tk.Button(self.root, text="Submit", command=self.save_username)
        self.submit_button.pack(pady=10)

    def save_username(self):
        """Save the user's name and proceed to quiz selection."""
        self.username = self.username_entry.get().strip()  # Get the entered username and remove leading/trailing spaces
        if not self.username:
            messagebox.showwarning("Input Error", "Please enter a valid name.")
            return

        # Clear the previous widgets (username entry) and proceed to quiz selection
        self.username_label.pack_forget()
        self.username_entry.pack_forget()
        self.submit_button.pack_forget()
        
        self.choose_quiz()

    def choose_quiz(self):
        """Create a Listbox to show quizzes and allow selection."""
        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(pady=20)

        # Open the CSV file containing the quizzes
        with open('quizzes_created', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and len(row) > 1:
                    a = str(row[0])  # Quiz name
                    b = str(row[1])  # Quiz type
                    quiz_item = f"Quiz name: {a}, Quiz type: {b}"
                    self.listbox.insert(tk.END, quiz_item)

        # Add a button to start the quiz after a selection
        start_button = tk.Button(self.root, text="Start Quiz", command=self.start_selected_quiz)
        start_button.pack(pady=10)

    def start_selected_quiz(self):
        """Start the selected quiz by loading its file."""
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_quiz_info = self.listbox.get(selected_index)
            quiz_name = selected_quiz_info.split(",")[0].split(":")[1].strip()

            # Dynamically determine the quiz file based on the selected name
            quiz_file = f"{quiz_name}.csv"
            self.load_quiz(quiz_file)
            self.display_question()
        else:
            messagebox.showwarning("No Selection", "Please select a quiz to start.")

    def load_quiz(self, quiz_file):
        """Load the quiz from the given file."""
        try:
            with open(quiz_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                rows = list(reader)
                
                quiz_title = rows[0][1]
                quiz_description = rows[1][1]
                quiz_type = rows[2][1]
                
                self.quiz = self.create_quiz(quiz_title, quiz_description, quiz_type)

                for row in rows[4:]:
                    question = row[0]
                    if quiz_type == "MCQ":
                        options = row[1].split("|")
                        correct_option = int(row[2])  # Correct option is 0-based, no change needed here
                        self.quiz.add_question(question, options, correct_option)
                    elif quiz_type == "True/False":
                        correct_option = int(row[2])  # 0 for True, 1 for False
                        self.quiz.add_question(question, correct_option)
                    elif quiz_type == "Short Answer":
                        correct_option = row[2]  # Short answer (correct_option is the answer itself)
                        self.quiz.add_question(question, correct_option)

        except FileNotFoundError:
            messagebox.showerror("File Not Found", f"The quiz file {quiz_file} does not exist.")
            self.root.quit()

    def create_quiz(self, title, description, quiz_type):
        """Create an appropriate quiz object based on the type."""
        if quiz_type == "MCQ":
            return create_quiz_.MultipleChoiceQuiz(title, description)
        elif quiz_type == "True/False":
            return create_quiz_.TrueFalseQuiz(title, description)
        elif quiz_type == "Short Answer":
            return create_quiz_.ShortAnswerQuiz(title, description)
        else:
            raise ValueError("Unsupported quiz type")

    def display_question(self):
        """Display the current question based on the quiz type."""
        question_data = self.quiz.questions[self.current_question_index]
        question_text = question_data["question"]
        
        # Clear previous widgets if any
        for widget in self.root.winfo_children():
            widget.pack_forget()

        # Display question
        tk.Label(self.root, text=question_text, font=("Arial", 16)).pack(pady=20)

        if question_data["type"] == "MCQ":
            self.display_mcq_options(question_data)
        elif question_data["type"] == "True/False":
            self.display_tf_options(question_data)
        elif question_data["type"] == "Short Answer":
            self.display_short_answer_field()

        self.create_navigation_buttons()

    def display_mcq_options(self, question_data):
        """Display MCQ options with IntVar() to ensure single selection."""
        self.mcq_var = tk.IntVar()

        # Assign each option an integer value
        for idx, option in enumerate(question_data["options"]):
            tk.Radiobutton(self.root, text=option, variable=self.mcq_var, value=idx).pack()

    def display_tf_options(self, question_data):
        """Display True/False options.""" 
        self.tf_var = tk.IntVar()

        # True and False options stored as 0 and 1
        tk.Radiobutton(self.root, text="True", variable=self.tf_var, value=0).pack()
        tk.Radiobutton(self.root, text="False", variable=self.tf_var, value=1).pack()

    def display_short_answer_field(self):
        """Display Short Answer input field.""" 
        self.sa_entry = tk.Entry(self.root, width=50)
        self.sa_entry.pack(pady=10)

    def create_navigation_buttons(self):
        """Create navigation buttons for next and submit.""" 
        if self.current_question_index < len(self.quiz.questions) - 1:
            next_button = tk.Button(self.root, text="Next", command=self.next_question)
            next_button.pack(pady=10)
        else:
            submit_button = tk.Button(self.root, text="Submit Quiz", command=self.submit_quiz)
            submit_button.pack(pady=10)

    def next_question(self):
        """Handle moving to the next question.""" 
        self.save_answer()
        self.current_question_index += 1
        self.display_question()

    def save_answer(self):
        """Save the user's answer to the current question.""" 
        question_data = self.quiz.questions[self.current_question_index]
        if question_data["type"] == "MCQ":
            self.user_answers.append(self.mcq_var.get())  # Save the selected index (int)
        elif question_data["type"] == "True/False":
            self.user_answers.append(self.tf_var.get())  # Save 0 (True) or 1 (False)
        elif question_data["type"] == "Short Answer":
            self.user_answers.append(self.sa_entry.get())

    def submit_quiz(self):
        """Calculate and display the user's score.""" 
        self.save_answer()

        score = 0
        for i, question_data in enumerate(self.quiz.questions):
            correct_answer = question_data["correct_option"]
            
            if self.user_answers[i] == correct_answer:
                score += 1

        # Save the results with the username
        with open('quiz_details', 'a+') as file:
            writer = csv.writer(file)
    
            selected_index = self.listbox.curselection()  # Get the index of the selected quiz
            
            if selected_index:
                selected_quiz_info = self.listbox.get(selected_index)
                quiz_name = selected_quiz_info.split(",")[0].split(":")[1].strip()  # Extract quiz name
            else:
                quiz_name = "Unknown Quiz"  # Set default value if no quiz is selected

            # Now you can safely write to the file
            writer.writerow([self.username, quiz_name, score, len(self.quiz.questions)])

        messagebox.showinfo("Quiz Completed", f"Your Score: {score}/{len(self.quiz.questions)}")
        self.root.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    app = QuizTakingApp(root)
    root.mainloop()
