from unittest import TestCase
from optimization import *
import numpy as np


def cost_scalar(x):
    return x * x


def derivative(x):
    return 2.0 * x


def second_derivative(x):
    return 2.0


def cost_vector(x):
    return np.sum(x * x)


def gradient(x):
    return 2.0 * x


def hessian(x):
    return 2.0 * np.identity(x.size)


class TestOptimization(TestCase):
    def test_gradient_descent(self):
        # Scalar test
        i, x, cost = run_iterations(gradient_descent(cost_scalar, derivative, 10.0, 0.1), 1000)
        self.assertAlmostEqual(x, 0.0)
        self.assertAlmostEqual(cost, 0.0)
        self.assertGreater(i, 1)
        self.assertLess(i, 200)

        # Vector test
        i, x, cost = run_iterations(gradient_descent(cost_vector, gradient, np.array([10.0, 0.0]), 0.1), 1000)
        np.testing.assert_almost_equal(x, np.zeros(2))
        self.assertAlmostEqual(cost, 0.0)
        self.assertGreater(i, 1)
        self.assertLess(i, 200)

    def test_newtons_method(self):
        # Scalar test
        i, x, cost = run_iterations(newtons_method(cost_scalar, derivative, second_derivative, 10.0, 1.0), 1000)
        self.assertEqual(i, 1)
        self.assertAlmostEqual(x, 0.0)
        self.assertAlmostEqual(cost, 0.0)

        # Vector test
        i, x, cost = run_iterations(newtons_method(cost_vector, gradient, hessian, np.array([10.0, 0.0]), 1.0), 1000)
        self.assertEqual(i, 1)
        self.assertAlmostEqual(x[0], 0.0)
        self.assertAlmostEqual(x[1], 0.0)
        self.assertAlmostEqual(cost, 0.0)

    def test_linear_least_square(self):
        A = np.array([[0.1, 0.9], [0.2, 0.8]])
        b = np.array([0.3, 0.7])
        actual = linear_least_square(A, b)
        expected = np.linalg.solve(A, b)
        np.testing.assert_almost_equal(actual, expected)

    def test_constrained_linear_least_square(self):
        A = np.array([[0.1, 0.9], [0.2, 0.8]])
        b = np.array([0.3, 0.7])
        x = constrained_linear_least_square(A, b)
        np.testing.assert_almost_equal(np.linalg.norm(x), 1.0)
        cost = np.linalg.norm(A @ x - b) ** 2 / 2.0
        cost0 = np.linalg.norm(A @ np.zeros(2) - b) ** 2 / 2.0
        self.assertLess(cost, cost0)

        cost1 = np.linalg.norm(A @ np.linalg.solve(A, b) - b) ** 2 / 2.0
        self.assertGreater(cost, cost1)
