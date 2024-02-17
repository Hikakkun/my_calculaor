import pytest
from my_calculator import MyCalculator
from io import StringIO
import sys
from sympy import symbols

@pytest.fixture
def calculator_with_input():
    def create_calculator(user_input):
        calculator = MyCalculator()
        saved_stdin = sys.stdin  # sys.stdin を保存
        with StringIO(user_input) as mock_input:
            sys.stdin = mock_input
            result = calculator._input_expression("Enter expression: ")
        sys.stdin = saved_stdin  # sys.stdin を元に戻す
        return result

    return create_calculator

@pytest.mark.parametrize("input_str, expected_output_str", [
    ("e\n", None),
    ("2*x + 5\n", "2*x + 5"),
    ("e 2*x+3\n", "e 2*x+3"),
])
def test_input_expression(calculator_with_input, input_str, expected_output_str):
    result = calculator_with_input(input_str)
    assert result == expected_output_str

def exp_str_normalization(input_exp, expected_output_exp):
    result = MyCalculator()._exp_str_normalization(input_exp)
    assert result == expected_output_exp

def prefix_substitution(input_exp, expected_output_exp):
    my_calculator = MyCalculator()
    result = my_calculator._prefix_substitution(input_exp)
    assert result == expected_output_exp

def parse_expression(input_str, expected_output_exp):
    my_calculator = MyCalculator()
    result = my_calculator._parse_expression(input_str)
    assert result == expected_output_exp

@pytest.mark.parametrize("input_exp, expected_output_exp", [
    ("x + y", "x + y"),
    ("2_sen", "2*sen"),
    ("3_man", "3*man"),
    ("5_man+2_sen", "5*man+2*sen"),
    ("1,234,567", "1_234_567"),
])
def test_exp_str_normalization(input_exp, expected_output_exp):
    exp_str_normalization(input_exp, expected_output_exp)

@pytest.mark.parametrize("input_exp, expected_output_exp", [
    (symbols('x')+3, symbols('x')+3),
    (1*symbols('sen'), 1000),
    (2*symbols('sen') + 3*symbols('man'), 2*1000+3*10000),
])
def test_prefix_substitution(input_exp, expected_output_exp):
    prefix_substitution(input_exp, expected_output_exp)

@pytest.mark.parametrize("input_str, expected_output_exp", [
    ("x+3", symbols('x')+3),
    ("1_sen", 1000),
    ("2_sen + 3_man", 2*1000+3*10000),
    ("x_sen", symbols('x')*1000),
    ("x+1", symbols('x')+1),
])
def test_parse_expression(input_str, expected_output_exp):
    parse_expression(input_str, expected_output_exp)