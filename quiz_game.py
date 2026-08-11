import json
from pathlib import Path

from quiz import Quiz


# quiz_game.py가 있는 프로젝트 폴더를 기준으로 state.json의 절대 경로를 만든다.
STATE_FILE = Path(__file__).resolve().parent / "state.json"


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = None
        self.load_state()

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
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def run(self):
        """종료를 선택할 때까지 메뉴와 선택한 기능을 반복 실행한다."""
        while True:
            self.show_menu()
            menu_number = self.read_number("선택: ", 1, 5)

            if menu_number == 1:
                self.play_quiz()
            elif menu_number == 2:
                self.add_quiz()
            elif menu_number == 3:
                self.list_quizzes()
            elif menu_number == 4:
                self.show_best_score()
            else:
                print("게임을 종료합니다.")
                return

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

    def save_state(self):
        """퀴즈 목록과 최고 점수를 state.json에 저장한다."""
        try:
            data = {
                "quizzes": [
                    {
                        "question": quiz.question,
                        "choices": quiz.choices,
                        "answer": quiz.answer,
                    }
                    for quiz in self.quizzes
                ],
                "best_score": self.best_score,
            }

            with open(STATE_FILE, "w", encoding="utf-8") as file:
                # indent : 들여쓰기
                json.dump(data, file, ensure_ascii=False, indent=4)
        except MemoryError:
            print("저장할 데이터가 너무 커서 파일에 저장하지 못했습니다.")
            return False
        except OSError as error:
            print(f"저장 파일을 쓸 수 없습니다: {error}")
            return False

        return True

    def load_state(self):
        """state.json을 불러오고 문제가 있으면 기본 퀴즈로 복구한다."""
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data["quizzes"], list):
                raise ValueError

            quizzes = [
                Quiz(item["question"], item["choices"], item["answer"])
                for item in data["quizzes"]
            ]
            best_score = data["best_score"]

            if best_score is not None and (
                not isinstance(best_score, int) or not 0 <= best_score <= 100
            ):
                raise ValueError

            self.quizzes = quizzes
            self.best_score = best_score
            print(f"저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개)")
        except FileNotFoundError:
            print("저장 파일이 없어 기본 퀴즈로 시작합니다.")
            self.restore_defaults()
            self.save_state()
        except (json.JSONDecodeError, UnicodeDecodeError, KeyError, TypeError, ValueError):
            print("저장 파일이 손상되어 기본 퀴즈로 복구합니다.")
            self.restore_defaults()
            self.save_state()
        except (RecursionError, MemoryError):
            print("저장 파일이 너무 크거나 구조가 복잡하여 기본 퀴즈로 복구합니다.")
            self.restore_defaults()
            self.save_state()
        except OSError as error:
            print(f"저장 파일을 읽을 수 없습니다: {error}")
            self.restore_defaults()

    def restore_defaults(self):
        """기본 퀴즈와 초기 점수로 되돌린다."""
        self.quizzes = self.create_default_quizzes()
        self.best_score = None

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
            self.save_state()
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

        if self.save_state():
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
