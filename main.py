import tkinter as tk
from tkinter import messagebox  # 팝업 창을 띄우기 위해 messagebox 모듈 추가
from PIL import Image, ImageTk  # 이미지 처리를 위해 PIL 라이브러리 사용
import random  # 그림 순서를 무작위로 섞기 위해 random 모듈 사용
from time import sleep  # 짝이 맞지 않을 때 잠시 지연하기 위해 sleep 사용

# 그림 짝 맞추기 게임 클래스
class MatchingGame:
    def __init__(self, root):
        # GUI 창 초기 설정
        self.root = root
        self.root.title("그림 짝 맞추기 게임")  # 창 제목 설정
        # 창의 크기를 800x800으로 설정 (주석처리됨)
        # self.root.geometry("800x800")
        # 사용자가 창 크기를 변경하지 못하도록 고정 (주석처리됨)
        # self.root.resizable(False, False)
        self.timer_running = False
        self.time = 0

        # 타이머 라벨 추가
        self.timer_label = tk.Label(self.root, text="시간: 0초", font=("Arial", 14))
        self.timer_label.grid(row=0, column=3, columnspan=2, sticky='e', padx=10, pady=10)

        # 4x4 버튼 배열 생성 (버튼을 저장할 2차원 리스트)
        self.buttons = [[None for _ in range(4)] for _ in range(4)]

        # 그림 목록 (1부터 8까지 두 번씩 들어있는 리스트, 총 16개 그림)
        self.pictures = list(range(1, 9)) * 2
        random.shuffle(self.pictures)  # 그림 순서를 무작위로 섞음

        # 첫 번째 클릭을 저장할 변수와 맞춘 짝의 수를 저장할 변수 초기화
        self.first_click = None
        self.matches = 0

        # 8개의 그림을 불러와서 크기 조정
        self.images = [self.load_and_resize_image(f"images/{i}.png") for i in range(1, 9)]

        # 빈 이미지 (기본 상태의 이미지) 설정
        self.empty_image = ImageTk.PhotoImage(Image.new("RGBA", (200, 200), (15, 15, 70, 255)))  # 더 어둡고 채도가 낮은 남색으로 설정
        # 기본 이미지 로드 (주석처리됨)
        # self.empty_image = self.load_and_resize_image("images/default.png")

        # 게임 보드 생성
        self.create_board()

        # 하단에 게임 시작 및 초기화 버튼 생성
        self.start_button = tk.Button(self.root, text="게임 시작", command=self.start_game)
        self.start_button.grid(row=5, column=0, columnspan=2, pady=20)

        self.reset_button = tk.Button(self.root, text="게임 초기화", command=self.reset_game)
        self.reset_button.grid(row=5, column=2, columnspan=2, pady=20)

    # 이미지를 로드하고 크기를 조정하는 함수
    def load_and_resize_image(self, filepath):
        image = Image.open(filepath)  # 파일 경로로부터 이미지를 로드
        image = image.resize((200, 200), Image.LANCZOS)  # 이미지를 200x200 크기로 조정
        return ImageTk.PhotoImage(image)

    # 게임 보드를 생성하는 함수
    def create_board(self):
        for i in range(4):
            for j in range(4):
                # 각 버튼에 빈 이미지를 설정하고, 클릭 시 on_click 메서드 호출
                button = tk.Button(self.root, image=self.empty_image, command=lambda row=i, col=j: self.on_click(row, col))
                button.grid(row=i, column=j, padx=2, pady=2)  # 버튼을 4x4 그리드로 배치하고 간격 추가
                self.buttons[i][j] = button  # 버튼을 버튼 배열에 저장

    def start_game(self):
        if not self.timer_running:
            # 타이머가 실행되지 않은 상태라면 타이머를 시작
            self.timer_running = True
            self.time = 0
            self.update_timer()

    def update_timer(self):
        if self.timer_running:
            # 타이머가 실행 중이라면 1초 증가
            self.time_elapsed += 1
            self.timer_label.config(text=f"시간: {self.time_elapsed}초")
            # 1초 후에 update_timer를 호출
            self.root.after(1000, self.update_timer)

    # 게임을 초기 상태로 리셋하는 함수
    def reset_game(self):
        random.shuffle(self.pictures)  # 그림을 다시 무작위로 섞음
        self.first_click = None  # 첫 번째 클릭 초기화
        self.matches = 0  # 맞춘 짝의 수 초기화

        # 모든 버튼을 기본 상태로 초기화
        for i in range(4):
            for j in range(4):
                button = self.buttons[i][j]
                button.config(image=self.empty_image, state='normal')
        
        # 타이머 리셋
        self.timer_running = False
        self.time_elapsed = 0
        self.timer_label.config(text="시간: 0초")

    # 버튼 클릭 시 호출되는 함수
    def on_click(self, row, col):
        button = self.buttons[row][col]

        # 이미 클릭된 버튼이라면 무시
        if button['state'] == 'disabled':
            return

        # 버튼에 해당하는 그림 표시
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

            # 두 버튼의 그림이 같은지 확인
            if self.pictures[first_row * 4 + first_col] == picture_id:
                # 그림이 일치하는 경우
                button.config(state='disabled')  # 현재 버튼 비활성화
                first_button.config(state='disabled')  # 첫 번째 버튼 비활성화
                self.matches += 1  # 맞춘 짝의 수 증가

                # 모든 짝을 다 맞췄는지 확인
                if self.matches == 8:
                    # 모든 짝을 맞췄다면 메시지 박스 표시 후 게임 재시작
                    self.timer_running = False
                    messagebox.showinfo("축하합니다!", "모든 짝을 맞추셨습니다!")
                    self.reset_game()  # 게임을 초기 상태로 리셋
            else:
                # 그림이 일치하지 않는 경우
                self.root.update()  # GUI 업데이트 (버튼이 변경된 상태로 유지되도록)
                sleep(1)  # 1초간 지연
                button.config(image=self.empty_image, state='normal')  # 현재 버튼을 빈 이미지로 변경
                first_button.config(image=self.empty_image, state='normal')  # 첫 번째 버튼도 빈 이미지로 변경

            # 첫 번째 클릭 정보 초기화
            self.first_click = None

# 게임 실행을 위한 메인 코드
if __name__ == "__main__":
    root = tk.Tk()  # Tk 객체를 생성하여 기본 창 생성
    game = MatchingGame(root)  # MatchingGame 클래스의 인스턴스 생성
    root.mainloop()  # mainloop를 호출하여 GUI 이벤트 루프를 시작
