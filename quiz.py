class Quiz:
    CHOICE_COUNT = 4

    def __init__(self, question, choices, answer):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 비어 있을 수 없습니다.")
        if not isinstance(choices, list) or len(choices) != self.CHOICE_COUNT:
            raise ValueError(f"선택지는 {self.CHOICE_COUNT}개여야 합니다.")
        if any(not isinstance(choice, str) or not choice.strip() for choice in choices):
            raise ValueError("선택지는 비어 있을 수 없습니다.")
        if not isinstance(answer, int) or not 1 <= answer <= self.CHOICE_COUNT:
            raise ValueError(
                f"정답은 1부터 {self.CHOICE_COUNT} 사이의 숫자여야 합니다.")

        try:
            question.encode("utf-8")

            for choice in choices:
                choice.encode("utf-8")
        except UnicodeEncodeError:
            raise ValueError("문제와 선택지는 UTF-8로 표현할 수 있어야 합니다.")

        self.question = question.strip()
        self.choices = [choice.strip() for choice in choices]
        self.answer = answer

    def display(self, number):
        """현재 퀴즈 한 문제와 선택지를 문제 순서 번호와 함께 출력한다."""
        print("-" * 40)
        print(f"[문제 {number}]")
        print(self.question)
        print()

        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def is_correct(self, user_answer):
        """사용자가 입력한 답이 정답인지 확인한다."""
        return user_answer == self.answer
