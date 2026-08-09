import json

from quiz import Quiz


STATE_FILE = "state.json"


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

        try:
            with open(STATE_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
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
        except OSError as error:
            print(f"저장 파일을 읽을 수 없습니다: {error}")
            self.restore_defaults()

    def restore_defaults(self):
        """기본 퀴즈와 초기 점수로 되돌린다."""
        self.quizzes = self.create_default_quizzes()
        self.best_score = None
