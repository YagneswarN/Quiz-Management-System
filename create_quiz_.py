import tkinter as tk
from tkinter import messagebox
import csv
import os

class Quiz:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.questions = []


class MultipleChoiceQuiz(Quiz):
    def add_question(self, question, options, correct_option):
        self.questions.append({
            "type": "MCQ",
            "question": question,
            "options": options,
            "correct_option": correct_option
        })


class TrueFalseQuiz(Quiz):
    def add_question(self, question, correct_option):
        self.questions.append({
            "type": "True/False",
            "question": question,
            "options": ["True", "False"],
            "correct_option": correct_option
        })


class ShortAnswerQuiz(Quiz):
    def add_question(self, question, correct_option):
        self.questions.append({
            "type": "Short Answer",
            "question": question,
            "correct_option": correct_option
        })


# Main App
class QuizCreationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Creation System")
        self.quiz = None

        self.quiz_type = None
        self.current_frame = None  # Keep track of the current frame
        self.setup_quiz_type_page()

    def setup_quiz_type_page(self):
        """Setup the quiz type selection page."""
        if self.current_frame:
            self.current_frame.destroy()  # Destroy any previous frame

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.current_frame, text="Select Quiz Type", font=("Arial", 18)).pack(pady=20)

        tk.Button(self.current_frame, text="Multiple Choice Quiz", command=lambda: self.setup_title_page("MCQ")).pack(pady=10)
        tk.Button(self.current_frame, text="True/False Quiz", command=lambda: self.setup_title_page("True/False")).pack(pady=10)
        tk.Button(self.current_frame, text="Short Answer Quiz", command=lambda: self.setup_title_page("Short Answer")).pack(pady=10)

    def setup_title_page(self, quiz_type):
        """Setup the quiz title and description input page."""
        self.quiz_type = quiz_type
        if self.current_frame:
            self.current_frame.destroy()  # Destroy the previous frame

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.current_frame, text=f"{quiz_type} Quiz", font=("Arial", 18)).pack(pady=20)
        tk.Label(self.current_frame, text="Quiz Title:").pack()
        self.title_entry = tk.Entry(self.current_frame, width=50)
        self.title_entry.pack()

        tk.Label(self.current_frame, text="Quiz Description:").pack()
        self.description_entry = tk.Entry(self.current_frame, width=50)
        self.description_entry.pack()

        tk.Button(self.current_frame, text="Back", command=self.setup_quiz_type_page).pack(pady=10)
        tk.Button(self.current_frame, text="Next", command=self.setup_quiz_creation_page).pack(pady=20)

    def setup_quiz_creation_page(self):
        """Setup the quiz creation page."""
        title = self.title_entry.get().strip()
        description = self.description_entry.get().strip()

        if not title or not description:
            messagebox.showwarning("Input Error", "Please provide a title and description for the quiz.")
            return

        if self.quiz_type == "MCQ":
            self.quiz = MultipleChoiceQuiz(title, description)
        elif self.quiz_type == "True/False":
            self.quiz = TrueFalseQuiz(title, description)
        elif self.quiz_type == "Short Answer":
            self.quiz = ShortAnswerQuiz(title, description)

        if self.current_frame:
            self.current_frame.destroy()  # Destroy the title frame

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.current_frame, text=f"Create {self.quiz_type} Quiz", font=("Arial", 18)).pack(pady=20)

        if self.quiz_type == "MCQ":
            self.setup_mcq_creation_page()
        elif self.quiz_type == "True/False":
            self.setup_tf_creation_page()
        elif self.quiz_type == "Short Answer":
            self.setup_sa_creation_page()

    def setup_mcq_creation_page(self):
        """Setup Multiple Choice Question creation page."""
        tk.Label(self.current_frame, text="Question:").pack()
        self.question_entry = tk.Entry(self.current_frame, width=50)
        self.question_entry.pack()

        tk.Label(self.current_frame, text="Options:").pack()
        self.options_frame = tk.Frame(self.current_frame)
        self.options_frame.pack()

        self.option_entry = tk.Entry(self.options_frame, width=40)
        self.option_entry.pack(side=tk.LEFT, padx=5)

        self.add_option_button = tk.Button(self.options_frame, text="Add Option", command=self.add_option)
        self.add_option_button.pack(side=tk.LEFT, padx=5)

        self.options_listbox = tk.Listbox(self.current_frame, width=50, height=5)
        self.options_listbox.pack(pady=10)

        self.delete_option_button = tk.Button(self.current_frame, text="Delete Selected Option", command=self.delete_option)
        self.delete_option_button.pack(pady=5)

        tk.Label(self.current_frame, text="Correct Option (Enter Index 1-4):").pack()
        self.correct_option_entry = tk.Entry(self.current_frame, width=50)
        self.correct_option_entry.pack()

        self.add_common_controls()

    def setup_tf_creation_page(self):
        """Setup True/False Question creation page."""
        tk.Label(self.current_frame, text="Question:").pack()
        self.question_entry = tk.Entry(self.current_frame, width=50)
        self.question_entry.pack()

        tk.Label(self.current_frame, text="Correct Answer (True/False):").pack()
        self.correct_option_entry = tk.Entry(self.current_frame, width=50)
        self.correct_option_entry.pack()

        self.add_common_controls()

    def setup_sa_creation_page(self):
        """Setup Short Answer Question creation page."""
        tk.Label(self.current_frame, text="Question:").pack()
        self.question_entry = tk.Entry(self.current_frame, width=50)
        self.question_entry.pack()

        tk.Label(self.current_frame, text="Correct Answer:").pack()
        self.correct_option_entry = tk.Entry(self.current_frame, width=50)
        self.correct_option_entry.pack()

        self.add_common_controls()

    def add_common_controls(self):
        """Add controls common to all quiz types."""
        tk.Button(self.current_frame, text="Add Question", command=self.add_question).pack(pady=10)
        tk.Label(self.current_frame, text="Questions:").pack()
        self.questions_listbox = tk.Listbox(self.current_frame, width=80, height=10)
        self.questions_listbox.pack(pady=10)

        self.delete_question_button = tk.Button(self.current_frame, text="Delete Selected Question", command=self.delete_question)
        self.delete_question_button.pack(pady=5)

        self.save_quiz_button = tk.Button(self.current_frame, text="Save Quiz", command=self.save_quiz)
        self.save_quiz_button.pack(pady=20)

    def add_option(self):
        """Add an option for MCQ question."""
        option = self.option_entry.get().strip()
        if option:
            self.options_listbox.insert(tk.END, option)
            self.option_entry.delete(0, tk.END)

    def delete_option(self):
        """Delete selected option for MCQ question."""
        selected = self.options_listbox.curselection()
        if selected:
            self.options_listbox.delete(selected)

    def add_question(self):
        """Add the current question to the quiz."""
        question = self.question_entry.get().strip()
        correct_option = self.correct_option_entry.get().strip()

        if not question or not correct_option:
            messagebox.showwarning("Input Error", "Please fill in all fields before adding a question.")
            return

        if self.quiz_type == "MCQ":
            options = [self.options_listbox.get(i) for i in range(self.options_listbox.size())]
            self.quiz.add_question(question, options, correct_option)
        elif self.quiz_type == "True/False" or self.quiz_type == "Short Answer":
            self.quiz.add_question(question, correct_option)

        self.question_entry.delete(0, tk.END)
        self.correct_option_entry.delete(0, tk.END)
        self.options_listbox.delete(0, tk.END)

        self.update_questions_listbox()

    def update_questions_listbox(self):
        """Update the list of questions in the UI."""
        self.questions_listbox.delete(0, tk.END)
        for question in self.quiz.questions:
            if question["type"] == "MCQ":
                display = f"{question['question']} (Options: {', '.join(question['options'])})"
            elif question["type"] == "True/False":
                display = f"{question['question']} (Answer: {question['correct_option']})"
            elif question["type"] == "Short Answer":
                display = f"{question['question']} (Answer: {question['correct_option']})"
            self.questions_listbox.insert(tk.END, display)

    def delete_question(self):
        """Delete selected question."""
        selected = self.questions_listbox.curselection()
        if selected:
            question_text = self.questions_listbox.get(selected[0])
            for question in self.quiz.questions:
                if question_text.startswith(question["question"]):
                    self.quiz.questions.remove(question)
                    break
            self.update_questions_listbox()

    def save_quiz(self):
        """Save the quiz to a CSV file."""
        if not self.quiz.questions:
            messagebox.showwarning("Save Error", "Please add at least one question before saving.")
            return

        filename = f"{self.quiz.title.replace(' ', '_')}.csv"
        
        with open('quizzes_created','a+') as overall_quiz_file:
            writer=csv.writer(overall_quiz_file)
            writer.writerow([self.quiz.title, self.quiz_type])

        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", self.quiz.title])
            writer.writerow(["Description", self.quiz.description])
            writer.writerow(["Type", self.quiz_type])
            writer.writerow(["Questions"])
            for question in self.quiz.questions:
                if question["type"] == "MCQ":
                    writer.writerow([question["question"], "|".join(question["options"]), question["correct_option"]])
                elif question["type"] == "True/False":
                    writer.writerow([question["question"], "True/False", question["correct_option"]])
                elif question["type"] == "Short Answer":
                    writer.writerow([question["question"], "Short Answer", question["correct_option"]])

        messagebox.showinfo("Quiz Saved", f"Quiz saved successfully as '{filename}'.")
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizCreationApp(root)
    root.mainloop()
