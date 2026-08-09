from quiz_game import QuizGame


def main():
    game = QuizGame()

    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되었습니다. 현재 데이터를 저장합니다.")

        if game.save_state():
            print("저장을 마치고 안전하게 종료합니다.")
        else:
            print("저장에는 실패했지만 프로그램을 종료합니다.")


# 다른 파일에서 import할 때는 실행하지 않고, 이 파일을 직접 실행할 때만 시작한다.
if __name__ == "__main__":
    main()
