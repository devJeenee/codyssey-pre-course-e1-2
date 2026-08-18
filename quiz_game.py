from enum import IntEnum

import storage
from quiz import Quiz


class MenuOption(IntEnum):
    def __new__(cls, number, label):
        member = int.__new__(cls, number)
        member._value_ = number
        member.label = label
        return member

    PLAY_QUIZ = 1, "퀴즈 풀기"
    ADD_QUIZ = 2, "퀴즈 추가"
    LIST_QUIZZES = 3, "퀴즈 목록"
    SHOW_BEST_SCORE = 4, "점수 확인"
    EXIT = 5, "종료"


class QuizGame:
    def __init__(self):
        loaded_data = storage.load_data()

        if loaded_data is None:
            print("기본 퀴즈로 시작합니다.")
            self.quizzes = self.create_default_quizzes()
            self.best_score = None
            storage.save_data(self.quizzes, self.best_score)
        else:
            self.quizzes, self.best_score = loaded_data

    def create_default_quizzes(self):
        """처음 실행할 때 사용할 Python 기초 퀴즈 5개를 만든다."""
        return [
            Quiz(
                "Python에서 변수의 주된 역할은 무엇일까요?",
                [
                    "값에 이름을 붙여 저장한다",
                    "화면의 글자 크기를 바꾼다",
                    "인터넷에 자동으로 연결한다",
                    "Python을 삭제한다",
                ],
                1,
            ),
            Quiz(
                "정수 42의 자료형은 무엇일까요?",
                ["str", "bool", "int", "list"],
                3,
            ),
            Quiz(
                "참과 거짓을 표현하는 자료형은 무엇일까요?",
                ["dict", "bool", "float", "tuple"],
                2,
            ),
            Quiz(
                "여러 값을 순서대로 저장하고 변경할 수 있는 자료형은?",
                ["list", "int", "bool", "None"],
                1,
            ),
            Quiz(
                "키와 값을 한 쌍으로 저장하는 자료형은 무엇일까요?",
                ["str", "list", "dict", "bool"],
                3,
            ),
        ]

    def show_menu(self):
        """사용자가 선택할 수 있는 게임 메뉴를 출력한다."""
        print("\n" + "=" * 40)
        print("       Python 기초 퀴즈 게임")
        print("=" * 40)

        for menu in MenuOption:
            print(f"{menu.value}. {menu.label}")

        print("=" * 40)

    def run(self):
        """종료를 선택할 때까지 메뉴와 선택한 기능을 반복 실행한다."""
        menu_actions = {
            MenuOption.PLAY_QUIZ: self.play_quiz,
            MenuOption.ADD_QUIZ: self.add_quiz,
            MenuOption.LIST_QUIZZES: self.list_quizzes,
            MenuOption.SHOW_BEST_SCORE: self.show_best_score,
        }

        while True:
            self.show_menu()
            menu_number = self.read_number(
                "선택: ",
                min(menu.value for menu in MenuOption),
                max(menu.value for menu in MenuOption),
            )
            selected_menu = MenuOption(menu_number)

            if selected_menu is MenuOption.EXIT:
                print("게임을 종료합니다.")
                return

            menu_actions[selected_menu]()

    def read_number(self, prompt, minimum, maximum):
        """정해진 범위의 숫자가 입력될 때까지 다시 입력받는다."""
        while True:
            user_input = input(prompt).strip()

            if not user_input:
                print("입력값이 비어 있습니다. 다시 입력하세요.")
                continue

            try:
                number = int(user_input)
            except ValueError:
                print("숫자로 입력하세요.")
                continue

            if number < minimum or number > maximum:
                print(f"{minimum}부터 {maximum} 사이의 숫자를 입력하세요.")
                continue

            return number

    def read_text(self, prompt):
        """내용이 있는 문자열이 입력될 때까지 다시 입력받는다."""
        while True:
            user_input = input(prompt).strip()

            if user_input:
                return user_input

            print("입력값은 비워 둘 수 없습니다. 다시 입력하세요.")

    def play_quiz(self):
        """저장된 퀴즈를 차례대로 출제하고 결과를 보여준다."""
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        correct_count = 0
        total_count = len(self.quizzes)
        print(f"\n퀴즈를 시작합니다! (총 {total_count}문제)")

        for number, quiz in enumerate(self.quizzes, start=1):
            print()
            quiz.display(number)
            user_answer = self.read_number(
                "정답 입력: ", 1, Quiz.CHOICE_COUNT,
            )

            if quiz.is_correct(user_answer):
                correct_count += 1
                print("정답입니다!")
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

        score = round(correct_count / total_count * 100)
        print("\n" + "=" * 40)
        print(f"결과: {total_count}문제 중 {correct_count}문제 정답! ({score}점)")

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            storage.save_data(self.quizzes, self.best_score)
            print("새로운 최고 점수입니다!")
        else:
            print(f"현재 최고 점수는 {self.best_score}점입니다.")

        print("=" * 40)

        return score

    def add_quiz(self):
        """새 퀴즈 정보를 입력받아 목록과 state.json에 저장한다."""
        print("\n새로운 퀴즈를 추가합니다.")
        question = self.read_text("문제를 입력하세요: ")

        choices = []
        for number in range(1, Quiz.CHOICE_COUNT + 1):
            choice = self.read_text(f"선택지 {number}: ")
            choices.append(choice)

        answer = self.read_number(
            "정답 번호: ", 1, Quiz.CHOICE_COUNT,
        )
        self.quizzes.append(Quiz(question, choices, answer))

        if storage.save_data(self.quizzes, self.best_score):
            print("퀴즈가 추가되고 저장되었습니다!")
        else:
            print("퀴즈는 추가했지만 파일에는 저장하지 못했습니다.")

    def list_quizzes(self):
        """저장된 퀴즈의 번호와 문제를 목록으로 보여준다."""
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)

        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")

        print("-" * 40)

    def show_best_score(self):
        """저장된 최고 점수를 보여준다."""
        if self.best_score is None:
            print("아직 퀴즈를 푼 기록이 없습니다.")
            return

        print(f"최고 점수: {self.best_score}점")
