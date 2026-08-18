import unittest
from unittest.mock import patch

from quiz_game import MenuOption, QuizGame


class QuizGameMenuTest(unittest.TestCase):
    def test_menu_options_hold_number_and_label(self):
        menu_items = [(menu.value, menu.label) for menu in MenuOption]

        self.assertEqual(
            menu_items,
            [
                (1, "퀴즈 풀기"),
                (2, "퀴즈 추가"),
                (3, "퀴즈 목록"),
                (4, "점수 확인"),
                (5, "종료"),
            ],
        )

    def test_show_menu_displays_all_menu_items(self):
        game = QuizGame.__new__(QuizGame)

        with patch("builtins.print") as mocked_print:
            game.show_menu()

        printed_lines = [call.args[0] for call in mocked_print.call_args_list]
        self.assertIn("1. 퀴즈 풀기", printed_lines)
        self.assertIn("2. 퀴즈 추가", printed_lines)
        self.assertIn("3. 퀴즈 목록", printed_lines)
        self.assertIn("4. 점수 확인", printed_lines)
        self.assertIn("5. 종료", printed_lines)

    def test_run_dispatches_each_menu_action_and_exits(self):
        game = QuizGame.__new__(QuizGame)

        with (
            patch.object(game, "show_menu"),
            patch.object(game, "read_number", side_effect=[1, 2, 3, 4, 5]),
            patch.object(game, "play_quiz") as mocked_play_quiz,
            patch.object(game, "add_quiz") as mocked_add_quiz,
            patch.object(game, "list_quizzes") as mocked_list_quizzes,
            patch.object(game, "show_best_score") as mocked_show_best_score,
            patch("builtins.print") as mocked_print,
        ):
            game.run()

        mocked_play_quiz.assert_called_once_with()
        mocked_add_quiz.assert_called_once_with()
        mocked_list_quizzes.assert_called_once_with()
        mocked_show_best_score.assert_called_once_with()
        mocked_print.assert_called_once_with("게임을 종료합니다.")


if __name__ == "__main__":
    unittest.main()
