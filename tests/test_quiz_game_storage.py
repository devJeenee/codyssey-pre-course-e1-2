import json
import unittest
from unittest.mock import mock_open, patch

import storage
from quiz import Quiz
from quiz_game import QuizGame


class QuizGameStorageTest(unittest.TestCase):
    def test_save_data_writes_quizzes_and_best_score_as_json(self):
        quizzes = [Quiz("문제", ["하나", "둘", "셋", "넷"], 2)]
        mocked_open = mock_open()

        with patch("builtins.open", mocked_open):
            self.assertTrue(storage.save_data(quizzes, 80))

        written_text = "".join(
            call.args[0]
            for call in mocked_open().write.call_args_list
        )
        self.assertEqual(
            json.loads(written_text),
            {
                "quizzes": [
                    {
                        "question": "문제",
                        "choices": ["하나", "둘", "셋", "넷"],
                        "answer": 2,
                    }
                ],
                "best_score": 80,
            },
        )

    def test_save_data_returns_false_when_file_cannot_be_written(self):
        with (
            patch("builtins.open", side_effect=OSError),
            patch("builtins.print"),
        ):
            self.assertFalse(storage.save_data([], None))

    def test_load_data_restores_saved_quizzes_and_best_score(self):
        saved_data = json.dumps(
            {
                "quizzes": [
                    {
                        "question": "저장된 문제",
                        "choices": ["하나", "둘", "셋", "넷"],
                        "answer": 3,
                    }
                ],
                "best_score": 60,
            },
            ensure_ascii=False,
        )

        with patch("builtins.open", mock_open(read_data=saved_data)):
            quizzes, best_score = storage.load_data()

        self.assertEqual(len(quizzes), 1)
        self.assertEqual(quizzes[0].question, "저장된 문제")
        self.assertEqual(quizzes[0].answer, 3)
        self.assertEqual(best_score, 60)

    def test_load_data_returns_none_when_file_is_missing(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            self.assertIsNone(storage.load_data())

    def test_load_data_returns_none_when_json_is_damaged(self):
        with patch("builtins.open", mock_open(read_data="{잘못된 JSON")):
            self.assertIsNone(storage.load_data())

    def test_quiz_game_uses_defaults_when_load_data_fails(self):
        with (
            patch.object(storage, "load_data", return_value=None),
            patch.object(storage, "save_data", return_value=True) as mocked_save,
        ):
            game = QuizGame()

        self.assertEqual(len(game.quizzes), 5)
        self.assertIsNone(game.best_score)
        mocked_save.assert_called_once_with(game.quizzes, None)


if __name__ == "__main__":
    unittest.main()
