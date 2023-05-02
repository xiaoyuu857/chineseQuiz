from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QCursor, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QRadioButton, QButtonGroup, QHBoxLayout
import sys
import json
from functools import partial
import random


class MyWindow(QMainWindow):
    def __init__(self, questions, answer_to_explanation):
        super().__init__()
        self.setGeometry(500, 500, 800, 400)
        self.setWindowTitle("Chinese Idioms")
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.current_question_index = 0
        self.score = 0
        self.questions = random.sample(questions, 10)
        self.answer_to_explanation = answer_to_explanation
        self.current_question_id = 1
        self.show_correct_answers = False
        random.shuffle(self.questions)
        self.initUI()


    def initUI(self):
        page1 = QWidget()
        layout = QVBoxLayout()
        layout.addStretch()
        logo_label = QLabel()
        logo_pixmap = QPixmap('logo.png')
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(logo_label)

        self.play_button = QtWidgets.QPushButton("Play", page1)
        self.play_button.setStyleSheet(    
            '''*{
                    padding: 25px 0px;
                    background: '#BC006C';
                    color: 'white';
                    font-family: 'Arial';
                    font-size: 35px;
                    border-radius: 40px;
                    margin: 10px 200px;
                }
                *:hover{
                    background: '#ff1b9e';
            }'''
            )
        layout.addWidget(self.play_button)
        layout.addStretch()
        page1.setLayout(layout)
        self.play_button.clicked.connect(lambda: self.showQuestion(self.questions, 0))
        self.stacked_widget.addWidget(page1)

        self.page2 = QWidget()
        self.stacked_widget.addWidget(self.page2)
        layout = QVBoxLayout(self.page2)
        self.question_label = QLabel()
        layout.addWidget(self.question_label)
        
        self.score_label = QLabel(self)
        font = QFont('Helvetica', 15)
        self.score_label.setFont(font)
        self.score_label.setAlignment(Qt.AlignRight)

        self.updateScoreLabel()

        self.correct_label = QLabel(self)
        font = QFont('Helvetica', 15)
        self.correct_label.setFont(font)
        self.correct_label.setAlignment(Qt.AlignRight)
        self.correct_label.setGeometry(0, 0, 800, 50)

        self.question_id_label = QLabel(self)
        font = QFont('Helvetica', 20)
        self.question_id_label.setFont(font)
        self.question_id_label.setAlignment(Qt.AlignLeft)

        self.progress_bar = QtWidgets.QProgressBar(self)
        self.progress_bar.setRange(0, 9)
        self.progress_bar.setValue(0)
        self.progress_bar.setGeometry(0, 0, 300, 25)

        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.addWidget(self.progress_bar)
        status_layout.addWidget(self.score_label)

        self.statusBar().setStyleSheet("margin-left: 10px")    

        layout.addWidget(self.question_id_label)
        layout.addWidget(self.score_label)
        layout.addWidget(self.correct_label)
        layout.addWidget(self.question_label)
        layout.addWidget(status_widget)

        self.button_group = QButtonGroup()
        self.answers = []
        for i in range(4):
            answer = QRadioButton()
            self.answers.append(answer)
            font = QFont('Helvetica', 15)
            answer.setFont(font)
            self.button_group.addButton(answer)
            answer.clicked.connect(partial(self.updateExplanation, answer))
            layout.addWidget(answer)

        self.submit_button = QPushButton("Submit")
        layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.submitAnswer)

        self.next_button = QPushButton("Next")
        layout.addWidget(self.next_button)
        self.next_button.clicked.connect(self.nextQuestion)

        # self.hint_button = QPushButton("Hint")
        # layout.addWidget(self.hint_button)
        # self.hint_button.clicked.connect(self.hintAnswer)

        self.explanation_label = QLabel()
        font = QFont('Helvetica', 14)
        self.explanation_label.setFont(font)
        # self.explanation_label.hide()
        layout.addWidget(self.explanation_label)

        self.correct_answer_label = QLabel()
        font = QFont('Helvetica', 14)
        self.correct_answer_label.setFont(font)
        layout.addWidget(self.correct_answer_label)

    def updateScoreLabel(self):
        self.score_label.setText(f"Score: {self.score}/{len(self.questions)}")

    def updateQuestionLabel(self):
        self.question_id_label.setText(f"Question: {self.current_question_id}/{len(self.questions)}")

    def updateProgressBar(self):
        self.progress_bar.setValue(self.current_question_index)

    def showFinalScreen(self):
        self.final_page = QWidget()

        score_label = QLabel(f"Your final score is {self.score} out of {len(self.questions)}")
        font = QFont('Helvetica', 14)
        score_label.setFont(font)
        score_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(score_label)
        layout.addStretch()
        self.final_page.setLayout(layout)

        self.button = QtWidgets.QPushButton('TRY AGAIN', self.final_page)
        self.button.setStyleSheet(
            '''*{
                padding: 25px 0px;
                background: '#BC006C';
                color: 'white';
                font-family: 'Arial';
                font-size: 35px;
                border-radius: 40px;
                margin: 10px 200px;
            }
            *:hover{
                background: '#ff1b9e';
            }'''
            )
        layout.addWidget(self.button)
        self.button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.button.clicked.connect(lambda: self.showQuestion(self.questions, 0))
        self.stacked_widget.addWidget(self.final_page)
        self.stacked_widget.setCurrentWidget(self.final_page)
        self.button.clicked.connect(self.resetGame)


    def updateExplanation(self, button):
        selected_answer = button.text()

        for answer in self.current_question['answers']:
            if answer['answer'] == selected_answer:
                explanation = answer['explanation']
                break

        self.explanation_label.setText(explanation)
        self.explanation_label.show()


    def showQuestion(self, questions, index):
        self.updateProgressBar()
        self.updateQuestionLabel()
        question = self.questions[self.current_question_index]
        font = QFont('SimSun', 20)
        self.question_label.setFont(font)
        self.current_question_index = index
        self.updateProgressBar()
        self.current_question = questions[self.current_question_index]
        self.question_label.setText(self.current_question['question'])
        for i, answer in enumerate(self.current_question['answers']):
            self.answers[i].setText(answer['answer'])

        self.next_button.setEnabled(False)

        self.stacked_widget.setCurrentIndex(1)


    def get_selected_answer(self):
        for button in self.answers:
            if button.isChecked():
                return button.text()
        return None
    

    # def hintAnswer(self):
    #     for i, answer in enumerate(self.current_question['answers']):
    #         correct_answer = self.current_question["answer"] 
    #     buttons = self.button_group.buttons()
    #     incorrect_buttons = [button for button in buttons if button.text() != correct_answer]
    #     incorrect_answers = random.sample(incorrect_buttons, 2)
    #     for answer in incorrect_answers:
    #         answer.hide()
    #         self.answers.remove(answer)


    def submitAnswer(self):
        if self.button_group.checkedButton() is None:
            QtWidgets.QMessageBox.warning(self, "No answer selected", "Please select an answer.")
            return

        selected_answer_text = self.get_selected_answer()
        for question in self.questions:
            if question['id'] == self.current_question['id']:
                for answer in question['answers']:
                    if answer['answer'] == selected_answer_text:
                        is_true = answer['is_correct']
                        if is_true:
                            explanation = answer['explanation']
                        break
                break

        self.showExplanation(selected_answer_text)
        self.correct_label.show()

        for answer in self.answers:
            answer.setEnabled(False)

        if is_true:
            self.score += 1
            self.correct_label.setText("Correct")
            self.correct_label.setStyleSheet("color: green")
        else:
            self.correct_answer = [answer['answer'] for answer in self.current_question['answers'] if answer['is_correct']][0]
            self.correct_label.setText("Incorrect")
            self.correct_label.setStyleSheet("color: red")
            self.showExplanation(self.correct_answer)
            explanation = self.answer_to_explanation[self.correct_answer]  # get the explanation from the answer_to_explanation dict
            self.correct_answer_label.setText(f"Correct answer: {self.correct_answer}\nExplanation: {explanation}")
            self.correct_answer_label.show()
            self.explanation_label.setText("")


        self.updateScoreLabel()
        self.submit_button.setEnabled(False)
        self.button_group.setExclusive(False)
        self.next_button.setEnabled(True)



    def showExplanation(self, answer_text):
        for answer in self.questions[self.current_question_index]['answers']:
            if answer['answer'] == answer_text:
                explanation = answer['explanation']
                self.explanation_label.setText(explanation)
                break
    
    def nextQuestion(self):
        for button in self.answers:
            button.setChecked(False)
        self.current_question_id += 1
        self.updateQuestionLabel()
        if self.current_question_index == len(self.questions) - 1:
            self.showFinalScreen()
            self.correct_label.setText("")
            self.question_id_label.hide()
            self.score_label.hide()
            return
        if self.current_question_id > len(self.questions):
            self.stacked_widget.setCurrentIndex(1)
            self.question_id_label.hide()
            return
        else:
            self.button_group.setExclusive(True)
            self.submit_button.setEnabled(True)
            self.showQuestion(self.questions, self.current_question_id - 1)
            self.correct_label.setText("")
            for answer in self.answers:
                answer.setEnabled(True)
        self.explanation_label.setText("")
        self.correct_label.setText("")
        self.correct_answer_label.setText("")

    
    def resetGame(self):
        self.current_question_index = 0
        self.score = 0
        self.current_question_id = 1
        self.show_correct_answers = False
        self.updateScoreLabel()
        self.updateQuestionLabel()
        self.stacked_widget.setCurrentIndex(0)
        self.submit_button.setEnabled(True)
        self.correct_label.hide()
        self.question_id_label.show()
        self.score_label.show()
        self.correct_answer_label.setText("") 
        self.explanation_label.setText("")
        for answer in self.answers:
            answer.setEnabled(True)


def load_questions_and_answers():
    # Load the questions
    with open('questions.json', 'r', encoding="utf-8") as f:
        questions = json.load(f)

    # Load the answers
    with open('answers.json', 'r', encoding="utf-8") as f:
        answers = json.load(f)

    answer_to_explanation = {answer['answer']: answer['explanation'] for answer in answers}

    for question in questions:
        for answer in question['answers']:
            answer['explanation'] = answer_to_explanation.get(answer['answer'], '')

    # Save the updated questions
    with open('updated_questions.json', 'w', encoding="utf-8") as f:
        json.dump(questions, f, indent=4)

    return questions


if __name__ == '__main__':
    app = QApplication(sys.argv)
    questions = load_questions_and_answers()
    with open('answers.json', 'r', encoding="utf-8") as f:
        answers = json.load(f)
    answer_to_explanation = {answer['answer']: answer['explanation'] for answer in answers}
    win = MyWindow(questions, answer_to_explanation)
    win.show()
    sys.exit(app.exec_())