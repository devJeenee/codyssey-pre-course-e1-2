from quiz import Quiz


class QuizGame:
    def __init__(self):
        self.quizzes = self.create_default_quizzes()
        self.best_score = None

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
