from sympy import *
import pyperclip
from enum import Enum
from dataclasses import dataclass
import argparse 


class Variable(Enum):
    X = "x"

@dataclass
class ConstantInit:
    name: str
    value: int | float
    
    
class Constant(Enum):
    SEN = ConstantInit("sen", 1000)
    MAN = ConstantInit("man", 10000)

@dataclass
class MyCalculator:
    _x = symbols(Variable.X.value)
    _man = symbols(Constant.MAN.value.name)
    _sen = symbols(Constant.SEN.value.name)
    _EXIT_STR = "e" 

    def get_exit_str(self) -> str:
        """

        Returns:
            _type_: _description_
        """
        return self._EXIT_STR
    
    def _input_expression(self, prompt: str) -> str | None:
        """
        数学式を入力するようユーザーに促すメソッド。

        Args:
            - prompt (str): ユーザーに表示するプロンプト。

        Returns:
            - Union[str, None]: 入力された数学式。ユーザーがEXIT_STRを入力した場合はNoneを返す
        """
        expression = input(prompt).strip()
        return None if expression == self._EXIT_STR else expression

    def _exp_str_normalization(self, exp_str: str) -> str:
        """
        数学式文字列を正規化するメソッド。

        Args:
            - exp_str (str): 正規化対象の数学式文字列。

        Returns:
            - str: 正規化された数学式文字列。

        正規化のルール:
        - カンマはアンダースコアに置き換える。
        - '_sen' は '*sen' に置き換える。
        - '_man' は '*man' に置き換える。
        """
        get_tuple = lambda replacement_str : (f'_{replacement_str}', f'*{replacement_str}')
        replacement_string_list = [
            (',', '_'), 
            get_tuple(Constant.SEN.value.name),
            get_tuple(Constant.MAN.value.name),
        ]
        for before, after in replacement_string_list:
            exp_str = exp_str.replace(before, after)
        return exp_str

    def _prefix_substitution(self, exp: Expr) -> Expr:
        """
        数学式に含まれる定数 'man' および 'sen' をそれぞれ 10,000 および 1,000 に置き換えるメソッド。

        Args:
            - exp (Expr): 置き換え対象の数学式。

        Returns:
            - Expr: 定数が置き換えられた数学式。

        定数の置き換え:
        - 'man' が数学式に含まれている場合、そのすべての出現を 10,000 に置き換える。
        - 'sen' が数学式に含まれている場合、そのすべての出現を 1,000 に置き換える。

        注記:
        - 数学式が int または float の場合は置き換えを行わず、そのまま返す。
        """
        if not isinstance(exp, (int, float)):
            if exp.has(self._man):
                exp = exp.subs(self._man, Constant.MAN.value.value)
            if exp.has(self._sen):
                exp = exp.subs(self._sen, Constant.SEN.value.value)
        return exp
    
    def _parse_expression(self, expression_str: str) -> None| Expr:
        """
        数学式文字列を解析し、SymPyの式オブジェクトに変換するメソッド。

        Args:
            - expression_str (str): 解析対象の数学式文字列。

        Returns:
            - Union[None, Expr]: 解析されたSymPyの式オブジェクト。解析に失敗した場合は None。

        解析の手順:
        1. `_exp_str_normalization` メソッドを使用して数学式文字列を正規化する。
        2. `parse_expr` 関数を使用して数学式文字列をSymPyの式オブジェクトに変換する。
        3. `_prefix_substitution` メソッドを使用して前置演算子を正しく処理する。
        4. 変換された式オブジェクトを返す。

        例外:
        - 解析に失敗した場合は、エラーメッセージを表示し、Noneを返す。
        """
        try:
            expression = parse_expr(self._exp_str_normalization(expression_str))
            return self._prefix_substitution(expression)
        except Exception as e:
            print(f"正しい式を入力してください {e}")
            return None        
        
    def _answer_print_and_copy(self, solution : Expr):
        """
        解や計算結果を表示し、クリップボードにコピーするメソッド。

        Args:
            - solution (Expr): 解や計算結果のSymPyの式オブジェクト。

        表示とクリップボードコピーのルール:
        - 解や計算結果を表示する。
        - 解が整数の場合、整数に変換してクリップボードにコピーする。
        - 解が浮動小数点数の場合、浮動小数点数に変換してクリップボードにコピーする。
        - 上記以外の場合は、解を評価した結果を浮動小数点数に変換してクリップボードにコピーする。

        例外:
        - エラーが発生した場合は、エラーメッセージを表示する。
        """
        try:
            solution_eval = solution.evalf()
            print(f"x = {solution} = {solution_eval}")
            
            if isinstance(solution, Integer):
                solution_cast_int = int(solution)
                pyperclip.copy(solution_cast_int)
                print(f"{solution_cast_int} をクリップボードにコピー")
            elif isinstance(solution, Float):
                solution_cast_float = float(solution)
                pyperclip.copy(solution_cast_float)
                print(f"{solution_cast_float} をクリップボードにコピー")
            else:
                pyperclip.copy(float(solution_eval))
                print(f"{solution_eval} をクリップボードにコピー")
                

        except Exception as e: 
            print(e) 
    

    def liner_equation(self):
        """
        一次方程式を解くためのメソッド。

        終了文字列が入力されるまで、ユーザーに左辺と右辺の数学式を入力させ、
        一次方程式を構築して解を求め、解や計算結果を表示し、クリップボードにコピーする。
        """
        print("xの方程式を解く")
        print(f"{self.get_exit_str()}で終了")
        while True:
            left_exp_str = self._input_expression("左辺: ")
            if left_exp_str is None:
                break
            left_exp = self._parse_expression(left_exp_str)
            if left_exp is None:
                continue

            right_exp_str = self._input_expression("右辺: ")
            if right_exp_str is None:
                break

            right_exp = self._parse_expression(right_exp_str)
            if right_exp is None:
                continue  
            
            equation = Eq(left_exp, right_exp)
            
            try:
                solution_list = solve(equation, self._x)
            except Exception as e:
                print(e)
                continue
            
            print(equation)
            
            if len(solution_list) > 0:
                self._answer_print_and_copy(solution_list[0])
            else:
                print("解なし")

    def calculation(self):
        """
        数式を計算するためのメソッド。

        終了文字列が入力されるまで、ユーザーに数学式を入力させ、
        数式を解析して結果を表示し、クリップボードにコピーする。
        """
        print("数式を計算する")
        print(f"{self.get_exit_str()}で終了")
        while True:
            formula_str = self._input_expression("計算式: ")
            if formula_str is None:
                break
            
            result = self._parse_expression(formula_str)
            if result is None:
                continue
            
            #result = self._prefix_substitution(result)
            
            self._answer_print_and_copy(result)
    
if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='簡単な数値計算とxの方程式を解析的に解くプログラム')  
    parser.add_argument('--calculation', action='store_true', help="指定すると数値計算を行う 指定しないと方程式を解くモードに変更")
    args = parser.parse_args()
    
    my_calucu = MyCalculator()
    if args.calculation:
        my_calucu.calculation()
    else:
        my_calucu.liner_equation()