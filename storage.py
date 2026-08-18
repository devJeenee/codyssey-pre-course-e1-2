import json
from pathlib import Path

from quiz import Quiz


# storage.py가 있는 프로젝트 폴더를 기준으로 state.json의 절대 경로를 만든다.
STATE_FILE = Path(__file__).resolve().parent / "state.json"


def save_data(quizzes, best_score):
    """퀴즈 목록과 최고 점수를 state.json에 저장한다."""
    try:
        data = {
            "quizzes": [
                {
                    "question": quiz.question,
                    "choices": quiz.choices,
                    "answer": quiz.answer,
                }
                for quiz in quizzes
            ],
            "best_score": best_score,
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


def load_data():
    """state.json을 불러오고 실패하면 None을 반환한다."""
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

        print(f"저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개)")
        return quizzes, best_score
    except FileNotFoundError:
        print("저장 파일이 없습니다.")
    except (UnicodeDecodeError, KeyError, TypeError, ValueError):
        print("저장 파일이 손상되었습니다.")
    except (RecursionError, MemoryError):
        print("저장 파일이 너무 크거나 구조가 복잡합니다.")
    except OSError as error:
        print(f"저장 파일을 읽을 수 없습니다: {error}")

    return None
