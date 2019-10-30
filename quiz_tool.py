from tkinter import *
# import tkinter.ttk as ttk
import json
import random
filepath = '/Users/mattdonnelly/PycharmProjects/QuizGUI/quiz_sample.json'
class StartMenu(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('300x500')
        self.title('Quiz Master')
        categories = []
        button_frame = Frame(self)
        with open(filepath,'r') as json_data:
            d = json.load(json_data)
            for i in range(len(d['categories'])):
                try:
                    categories.append(d['categories'][i]['name'])
                except:
                    print('Failed list load from quiz master')
        def subjectButtons(*cats):
            Button(self, text = cats, command = lambda: self.openQuiz(main_window, cats)).pack(fill=BOTH, pady=15, expand=True)
        for i in range(len(categories)):
            subjectButtons(categories[i])
        button_frame.pack(side=TOP)
    @staticmethod
    def openQuiz(parent, *category):
        top = Toplevel(parent)
        top.geometry('750x750')
        top.title(category)
        question_frame = Frame(top)
        answer_frame = Frame(top)
        grade_frame = Frame(top)
        v = IntVar()
        v.set(random.randint(1,4))
        question = []
        scoring = []
        with open(filepath, 'r') as json_data:
            d = json.load(json_data)
            for i in range(len(d[category[0][0]])):
                question.append(d[category[0][0]][i])
        def questionGen(**ans):
            line = random.randint(1,4)
            r = [1,2,3,4]
            r.remove(line)
            for key, val in ans.items():
                if key == 'quest':  # Print questions
                    Label(question_frame, text=val).grid(row=0, column=1)
                    q = val
                elif key == 'entr':  # Print correct answer
                    c = val
                    Radiobutton(answer_frame, text=val, value=0, variable=v).grid(row=line, column=1)
                    Button(answer_frame, text='Next', command=lambda: grading(quest=q, choice=v, corr=c)).grid(row=5, column=2)
                else:  # Print wrong answers
                    rval = sorted(iter(val), key=lambda k: random.random())
                    for i, x in enumerate(rval):
                        Radiobutton(answer_frame, text=x, value=i+1, variable=v).grid(row=r[i], column=1)
        def grading(**result):
            for ind, val in result.items():
                if ind == 'quest':
                    scoring.append(val)
                if ind == 'choice' and val.get()==0:
                    scoring.append('Correct')
                if ind == 'choice' and val.get()!=0:
                    scoring.append('Incorrect')
                if ind == 'corr':
                    scoring.append(val)
            rand.pop(0)
            try:
                questionGen(quest=rand[0]['question'], entr=rand[0]['answer'], wrg=rand[0]['nanswer'])
            except:
                finalGrade(scoring)
        def finalGrade(*score):
            answer_frame.destroy()
            question_frame.destroy()
            points = 0
            row_count = 0
            total = len(score[0])
            for i in range(total):
                if row_count%3 == 0:
                    Label(grade_frame, text=score[0][i]).grid(row=i, column=2)
                elif row_count%3 == 1:
                    Label(grade_frame, text=score[0][i]).grid(row=i, column=1)
                else:
                    Label(grade_frame, text=score[0][i]).grid(row=i-1, column=3)
                if score[0][i] == 'Correct':
                    points+=1
                row_count+=1
            Label(grade_frame, text='Your score:').grid(row=total+1, column=0)
            Label(grade_frame, text=points).grid(row=total+1, column=2)
        rand = sorted(iter(question), key=lambda k: random.random())
        questionGen(quest=rand[0]['question'], entr=rand[0]['answer'], wrg=rand[0]['nanswer'])
        question_frame.pack(side=TOP)
        answer_frame.pack(side=TOP)
        grade_frame.pack(side=TOP)

main_window = StartMenu()
main_window.mainloop()
