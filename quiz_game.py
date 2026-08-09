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
