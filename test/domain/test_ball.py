import pypinball
import unittest


class TestBall(unittest.TestCase):
    def test_set_ball_position(self):
        ball = pypinball.domain.Ball(position=(0.0, 0.0))
        ball.set_position(position=(1.0, 0.0))

        exp = (1.0, 0.0)
        res = ball.position

        self.assertEqual(exp, res)

    def test_get_ball_position_history(self):
        ball = pypinball.domain.Ball(position=(0.0, 0.0), history=3)

        for i in range(5):
            ball.set_position(position=(i + 1, i + 1))

        exp = [(4, 4), (3, 3), (2, 2)]
        res = ball.position_history

        self.assertEqual(exp, res)

    def test_get_ball_position_history_maximum_not_reached(self):
        ball = pypinball.domain.Ball(position=(0.0, 0.0), history=5)
        ball.set_position(position=(1.0, 1.0))
        ball.set_position(position=(2.0, 2.0))

        exp = [(1.0, 1.0), (0.0, 0.0)]
        res = ball.position_history

        self.assertEqual(exp, res)
