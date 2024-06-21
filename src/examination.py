import tkinter
import yaml
import os
import sys
import random
from PIL import Image,ImageTk
import pygame.mixer
import time

YAML = "./question.yaml"

N_QUESTION = 10

class Quiz():
    def __init__(self, master):
        self.master = master

        self.getQuiz()
        self.createWidgets()
        
        self.n_correct = 0
        
        while self.master == True:
            pygame.mixer.init()
            pygame.mixer.music.load("data/bgm.wav")
            pygame.mixer.music.play(-1)
            time.sleep(30)
            pygame.mixer.music.stop

    def getQuiz(self):
        if not os.path.exists(YAML):
            sys.exit(f"FileNotFoundError: {YAML}")

        with open(YAML, encoding='UTF-8') as yaml_file:
            yaml_load = yaml.load(yaml_file, Loader=yaml.SafeLoader)
            self.quiz_list = yaml_load.get('questions')
       
        if N_QUESTION < len(self.quiz_list):
            self.quiz_list = random.sample(self.quiz_list, N_QUESTION)
        else:
            self.quiz_list = random.sample(self.quiz_list, len(self.quiz_list))

    def createWidgets(self):  
        self.im = ImageTk.PhotoImage(file="../data/exam.png")
        self.frame = tkinter.Frame(
            self.master,
            width=1000
        )
        self.frame.pack()
        
        self.image = tkinter.Canvas(
            self.master,
            width=700,height=394
            )
        self.image.pack()
        self.image.create_image(350,150,image=self.im)

        self.button = tkinter.Button(
            self.master,
            text="検定開始",
            command=self.showQuiz
        )
        self.button.pack()
        

    def showQuiz(self):
        self.quiz = self.quiz_list[0]
        question = self.quiz.get('question')
        self.options = self.quiz.get('options')

        self.image.destroy()

        self.frame_q = tkinter.Frame(
            self.master,
        )
        self.frame_q.pack()


        self.question = tkinter.Label(
            self.frame_q,
            text=question,
        )
        self.question.grid(
            column=0,
            row=0,
            columnspan=len(self.options),
        )

              #現在選択中の選択肢番号
        self.choice_value = tkinter.IntVar()
        
        for i, option in enumerate(self.options):

            choice = tkinter.Radiobutton(
                self.frame_q,
                text=option,
                variable=self.choice_value,
                value=i
            )
            choice.grid(
                column=i,
                row=1,
                columnspan=1,
            )
    
            self.button.config(
                text="確認",
                command=self.checkAnswer
            )

        self.button_h = tkinter.Button(
            self.master,
            text="ヒントを見る",
            command=self.checkHint
        )
        self.button_h.pack()

    
    def checkHint(self):
        hint = self.quiz.get('hint')
        self.hint = tkinter.Label(
            self.frame_q,
            text=hint,
        )
        self.hint.grid(
            column=0,
            row=3,
            columnspan=2,
        )

    def checkAnswer(self):
        answer = self.quiz.get('answer')
        self.img = ImageTk.PhotoImage(file=self.quiz.get('image'))
        self.button_h.destroy()
        
        self.frame_a = tkinter.Frame(
            self.master,
        )
        self.frame_a.pack()

        self.button.config(
            text="次の問題へ",
            command=self.nextCommand
        )

        self.image = tkinter.Canvas(
            self.frame_a,
            width=700,height=550
        )
        self.image.grid(
                column=0,
                row=3,
                columnspan=2,
        )
        self.image.create_image(350,275,image=self.img)
     

        if self.choice_value.get() == int(answer):
            self.correct = tkinter.Label(
                self.frame_a,
                text='おみごと！正解です',
            )
            self.correct.grid(
                column=0,
                row=2,
                columnspan=2,
            )  
            self.n_correct += 1
        else:
            self.incorrect = tkinter.Label(
                self.frame_a,
                text='残念！正解は'+self.options[answer]+'です！',
            )
            self.incorrect.grid(
                column=0,
                row=2,
                columnspan=2,
            )  
        
        if len(self.quiz_list) == 1:
            self.button.config(
                text='結果発表',
                command=self.showResult,
            )
        else:
            self.button.config(
                text='NEXT',
                command=self.nextCommand,
            )

    def nextCommand(self):
        del self.quiz_list[0]
        self.frame_q.destroy()
        self.frame_a.destroy()
        self.showQuiz()

    def showResult(self):
        self.img1 = ImageTk.PhotoImage(file="../data/kaicho.png")
        self.img2 = ImageTk.PhotoImage(file="../data/shain.png")
        self.img3 = ImageTk.PhotoImage(file="../data/tsukinami.png")
        self.img4 = ImageTk.PhotoImage(file="../data/niwaka.png")
        self.img5 = ImageTk.PhotoImage(file="../data/kyomi.png")

        self.frame_r = tkinter.Frame(
        self.master,
        )
        self.frame_r.pack()

        self.frame_q.destroy()
        self.frame_a.destroy()
        self.button.config(
            text='検定終了',
            command=self.master.destroy
        )

        if self.n_correct == N_QUESTION:
            self.result = tkinter.Label(
                self.frame_r,
                text=str(N_QUESTION)+'問中'+str(self.n_correct)+'問正解です'
            )
            self.image = tkinter.Canvas(
            self.frame_r,
            width=700,height=550
            )
            self.image.grid(
                column=0,
                row=3,
                columnspan=2,
            )
            self.image.create_image(350,275,image=self.img1)

        if self.n_correct < N_QUESTION and self.n_correct > N_QUESTION*0.69:
            self.result = tkinter.Label(
                self.frame_r,
                text=str(N_QUESTION)+'問中'+str(self.n_correct)+'問正解です'
            )
            self.image = tkinter.Canvas(
            self.frame_r,
            width=700,height=550
            )
            self.image.grid(
                column=0,
                row=3,
                columnspan=2,
            )
            self.image.create_image(350,275,image=self.img2)

        if self.n_correct < N_QUESTION*0.69 and self.n_correct >= N_QUESTION*0.49:
            self.result = tkinter.Label(
                self.frame_r,
                text=str(N_QUESTION)+'問中'+str(self.n_correct)+'問正解です'
            )
            self.image = tkinter.Canvas(
            self.frame_r,
            width=700,height=550
            )
            self.image.grid(
                column=0,
                row=3,
                columnspan=2,
            )
            self.image.create_image(350,275,image=self.img3)

        if self.n_correct < N_QUESTION*0.49 and self.n_correct > N_QUESTION*0.19:
            self.result = tkinter.Label(
                self.frame_r,
                text=str(N_QUESTION)+'問中'+str(self.n_correct)+'問正解です'
            )
            self.image = tkinter.Canvas(
            self.frame_r,
            width=700,height=550
            )
            self.image.grid(
                column=0,
                row=3,
                columnspan=2,
            )
            self.image.create_image(350,275,image=self.img4)

        if self.n_correct < N_QUESTION*0.19:
            self.result = tkinter.Label(
                self.frame_r,
                text=str(N_QUESTION)+'問中'+str(self.n_correct)+'問正解です\nあなたはジェットコースターに興味のない人です'
            )
            self.result.grid(
                column=0,
                row=2,
                columnspan=2
            )
            self.image = tkinter.Canvas(
            self.frame_r,
            width=700,height=550
            )
            self.image.grid(
                column=0,
                row=3,
                columnspan=2,
            )
            self.image.create_image(350,275,image=self.img5)
        


if __name__ == '__main__':
    app = tkinter.Tk()
    quiz = Quiz(app)
    app.mainloop()
