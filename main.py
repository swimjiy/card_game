import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
from time import sleep

class MatchingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("그림 짝 맞추기 게임")

        # 타이머 제한 모드 설정
        self.timer_running = False
        self.time_limit = 60  # 제한 시간 60초 설정

        # 타이머 라벨 설정
        self.timer_label = tk.Label(self.root, text="남은 시간: 60초", font=("Arial", 14))
        self.timer_label.grid(row=0, column=3, columnspan=2, sticky='e', padx=10, pady=10)

        # 4x4 버튼 배열 생성 (버튼을 저장할 2차원 리스트)
        self.buttons = [[None for _ in range(4)] for _ in range(4)]
        self.pictures = list(range(1, 9)) * 2
        random.shuffle(self.pictures)

        # 첫 번째 클릭을 저장할 변수와 맞춘 짝의 수를 저장할 변수 초기화
        self.first_click = None
        self.matches = 0

        # 8개의 그림을 불러와서 크기 조정
        self.images = [self.load_and_resize_image(f"images/{i}.png") for i in range(1, 9)]

        # 빈 이미지 (기본 상태의 이미지) 설정
        self.empty_image = self.load_and_resize_image("images/default.png")

        # 게임 보드 생성
        self.create_board()

        # 하단에 게임 시작 및 초기화 버튼 생성
        self.start_button = tk.Button(self.root, text="게임 시작", command=self.start_game, highlightbackground='#90ee90', highlightthickness=2, font=('Arial', 14, 'bold'))
        self.start_button.grid(row=5, column=0, columnspan=2, pady=20)

        self.reset_button = tk.Button(self.root, text="게임 초기화", command=self.reset_game, highlightbackground='#f08080', highlightthickness=2, font=('Arial', 14, 'bold'))
        self.reset_button.grid(row=5, column=2, columnspan=2, pady=20)

    # 이미지를 로드하고 크기를 조정하는 함수
    def load_and_resize_image(self, filepath):
        image = Image.open(filepath)
        image = image.resize((200, 200), Image.LANCZOS)
        return ImageTk.PhotoImage(image)

    # 게임 보드를 생성하는 함수
    def create_board(self):
        for i in range(4):
            for j in range(4):
                button = tk.Button(self.root, image=self.empty_image, command=lambda row=i, col=j: self.on_click(row, col))
                button.grid(row=i+1, column=j, padx=2, pady=2)
                self.buttons[i][j] = button


    # 타이머 업데이트 함수
    def update_timer(self):
        if self.timer_running and self.time_limit > 0:
            self.time_limit -= 1
            self.timer_label.config(text=f"남은 시간: {self.time_limit}초")
            self.root.after(1000, self.update_timer) # 1000초 뒤에 update_timer() 함수 실행
        elif self.time_limit == 0:
            self.timer_running = False
            messagebox.showinfo("게임 오버", "제한 시간을 초과했습니다. 다시 시도하세요!")
            self.reset_game()



    # 게임을 초기 상태로 리셋하는 함수
    def reset_game(self):
        random.shuffle(self.pictures)
        self.first_click = None
        self.matches = 0

        # 모든 카드를 초기 상태로 변경
        for i in range(4):
            for j in range(4):
                button = self.buttons[i][j]
                button.config(image=self.empty_image, state='normal', relief='raised')

        # 타이머 리셋
        self.timer_running = False
        self.time_limit = 60
        self.timer_label.config(text="남은 시간: 60초")


    # 게임 시작 함수
    def start_game(self):
        self.reset_game()
        if not self.timer_running:
            self.timer_running = True
            self.time_limit = 60  # 제한 시간 60초로 설정
            self.update_timer()


    # 카드 클릭 시 호출되는 함수
    def on_click(self, row, col):
        button = self.buttons[row][col]

        # 이미 클릭된 버튼이라면 무시
        if button['state'] == 'disabled':
            return

        if not self.timer_running:
            messagebox.showinfo("안내", "게임 시작 버튼을 눌러주세요!")
            return

        # 애니메이션 효과
        button.config(relief='sunken')

        # 카드에 해당하는 그림 표시
        picture_id = self.pictures[row * 4 + col]
        button.config(image=self.images[picture_id - 1], state='disabled')

        # 첫 번째 클릭인 경우
        if self.first_click is None:
            self.first_click = (row, col)  # 첫 번째 클릭 위치 저장
        else:
            # 두 번째 클릭인 경우
            first_row, first_col = self.first_click
            first_button = self.buttons[first_row][first_col]
            self.root.update()

            if self.pictures[first_row * 4 + first_col] == picture_id:
                # 그림이 일치하는 경우
                button.config(state='disabled')
                first_button.config(state='disabled')
                self.matches += 1

                # 모든 짝을 다 맞췄는지 확인
                if self.matches == 8:
                    self.timer_running = False
                    messagebox.showinfo("축하합니다!", "모든 짝을 맞추셨습니다!")
            else:
                # 그림이 일치하지 않는 경우
                sleep(0.5)  # 0.5초 지연
                button.config(image=self.empty_image, state='normal', relief='raised')
                first_button.config(image=self.empty_image, state='normal', relief='raised')

            # 첫 번째 클릭 정보 초기화
            self.first_click = None

if __name__ == "__main__":
    root = tk.Tk()
    game = MatchingGame(root)
    root.mainloop()
