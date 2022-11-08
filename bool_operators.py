from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFrame, QLabel
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication


class OpenBracket(QLabel):
    def __init__(self, widget, show=False, negate=False):
        super().__init__('', widget)
        self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        if show:
            if negate:
                self.setText('not(')
            else:
                self.setText('(')
        else:
            self.setText('')

        self.setStyleSheet(
            'background-color: transparent;'
            'font-size: 24px;'
            'color: white;'
            'border: 0px;'
        )


class CloseBracket(QLabel):
    def __init__(self, widget, show=False):
        super().__init__('', widget)
        self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        if show:
            self.setText(')')
        else:
            self.setText('')

        self.setStyleSheet(
            'background-color: transparent;'
            'color: white;'
            'font-size: 24px;'
            'border: 0px;'

        )


class LogicalOperator(QLabel):
    def __init__(self, widget, operator, show=True):
        super().__init__(operator, widget)
        self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.setStyleSheet(
            'background-color: transparent;'
            'color: white;'
            'font-size: 24px;'
            'border: 0px;'
        )
        if not show:
            self.hide()


class ClickableBoolState(QLabel):
    clicked = pyqtSignal()

    def __init__(self, widget):
        super().__init__('', widget)
        self.setText('False')
        self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.setStyleSheet(
            'background-color: red;'
            'border: 1px solid grey;'
            'font-size: 24px;'
        )

    def set_state(self, state):
        if state:
            self.setStyleSheet(
                'background-color: #00FF00;'
                'border: 1px solid grey;'
                'font-size: 24px;'
            )
            self.setText('True')
        else:
            self.setStyleSheet(
                'background-color: #FF0000;'
                'border: 1px solid grey;'
                'font-size: 24px;'
            )
            self.setText('False')

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()


class BoolState(QLabel):
    def __init__(self, widget):
        super().__init__('', widget)
        self.setText('False')
        self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.setStyleSheet(
            'background-color: red;'
            'border: 1px solid grey;'
            'font-size: 24px;'
        )
    def set_state(self, state):
        if state:
            self.setStyleSheet(
                'background-color: #00FF00;'
                'border: 1px solid grey;'
                'font-size: 24px;'
            )
            self.setText('True')
        else:
            self.setStyleSheet(
                'background-color: #FF0000;'
                'border: 1px solid grey;'
                'font-size: 24px;'
            )
            self.setText('False')


class Expression:
    def __init__(self, widget, width, height, x_pos, y_pos,
                 show_first_brackets=False, negate=False, first_op='AND',
                 second_op_show=True, second_op='AND',
                 show_second_brackets=False, third_op='AND'):
        self.negate = negate
        self.frame = QFrame(widget)
        self.frame.setStyleSheet(
            'background-color: transparent;'
            'border: 3px solid white;'
        )

        self.state = BoolState(self.frame)
        self.equal_label = QLabel('=', self.frame)
        self.equal_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.equal_label.setStyleSheet(
            'background-color: transparent;'
            'color: white;'
            'font-size: 24px;'
            'border: 0px;'
        )
        self.first_bracket = OpenBracket(self.frame, show_first_brackets or negate, negate)
        self.first_bool = ClickableBoolState(self.frame)
        self.first_operator = LogicalOperator(self.frame, first_op)
        self.second_bool = ClickableBoolState(self.frame)
        self.second_bracket = CloseBracket(self.frame, show_first_brackets)
        self.second_operator = LogicalOperator(self.frame, show=second_op_show, operator=second_op)
        self.third_bracket = OpenBracket(self.frame, show_second_brackets)
        self.third_bool = ClickableBoolState(self.frame)
        self.third_operator = LogicalOperator(self.frame, third_op)
        self.fourth_bool = ClickableBoolState(self.frame)
        self.fourth_bracket = CloseBracket(self.frame, show_second_brackets or negate)

        self.resize(width, height, x_pos, y_pos)

    def resize(self, width, height, x, y):
        self.frame.resize(width, height)
        self.frame.move(x, y)

        self.state.resize(int(width * 0.1), int(height * 0.7))
        self.state.move(int(width * 0.02), int(height * 0.15))

        self.equal_label.resize(int(width * 0.04), int(height * 0.7))
        self.equal_label.move(int(width * 0.13), int(height * 0.15))

        if self.negate:
            self.first_bracket.resize(int(width * 0.04), int(height * 0.7))
            self.first_bracket.move(int(width * 0.16), int(height * 0.15))
        else:
            self.first_bracket.resize(int(width * 0.03), int(height * 0.7))
            self.first_bracket.move(int(width * 0.17), int(height * 0.15))

        self.first_bool.resize(int(width * 0.1), int(height * 0.7))
        self.first_bool.move(int(width * 0.2), int(height * 0.15))

        self.first_operator.resize(int(width * 0.04), int(height * 0.7))
        self.first_operator.move(int(width * 0.31), int(height * 0.15))

        self.second_bool.resize(int(width * 0.1), int(height * 0.7))
        self.second_bool.move(int(width * 0.36), int(height * 0.15))

        self.second_bracket.resize(int(width * 0.03), int(height * 0.7))
        self.second_bracket.move(int(width * 0.46), int(height * 0.15))

        self.second_operator.resize(int(width * 0.04), int(height * 0.7))
        self.second_operator.move(int(width * 0.5), int(height * 0.15))

        self.third_bracket.resize(int(width * 0.03), int(height * 0.7))
        self.third_bracket.move(int(width * 0.55), int(height * 0.15))

        self.third_bool.resize(int(width * 0.1), int(height * 0.7))
        self.third_bool.move(int(width * 0.58), int(height * 0.15))

        self.third_operator.resize(int(width * 0.04), int(height * 0.7))
        self.third_operator.move(int(width * 0.69), int(height * 0.15))

        self.fourth_bool.resize(int(width * 0.1), int(height * 0.7))
        self.fourth_bool.move(int(width * 0.74), int(height * 0.15))

        self.fourth_bracket.resize(int(width * 0.03), int(height * 0.7))
        self.fourth_bracket.move(int(width * 0.84), int(height * 0.15))


class Program(QMainWindow):
    def __init__(self):
        super().__init__()
        '''self, widget, width, height, x_pos, y_pos,
                 show_first_brackets=False, negate=False, first_op='AND',
                 second_op_show=True, second_op='AND',
                 show_second_brackets=False, third_op='AND'
        '''

        self.bool_values = [
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False]
        ]

        self.op_1 = Expression(self, 1500, 70, 50, 50)
        self.op_1.first_bool.clicked.connect(lambda: self.expression_clicked(1, 0))
        self.op_1.second_bool.clicked.connect(lambda: self.expression_clicked(1, 1))
        self.op_1.third_bool.clicked.connect(lambda: self.expression_clicked(1, 2))
        self.op_1.fourth_bool.clicked.connect(lambda: self.expression_clicked(1, 3))


        self.op_2 = Expression(
            self, 1500, 70, 50, 150, first_op='OR', second_op='OR', third_op='OR'
        )
        self.op_2.first_bool.clicked.connect(lambda: self.expression_clicked(2, 0))
        self.op_2.second_bool.clicked.connect(lambda: self.expression_clicked(2, 1))
        self.op_2.third_bool.clicked.connect(lambda: self.expression_clicked(2, 2))
        self.op_2.fourth_bool.clicked.connect(lambda: self.expression_clicked(2, 3))


        self.op_3 = Expression(
            self, 1500, 70, 50, 250, show_first_brackets=True,
            second_op='OR', show_second_brackets=True
        )
        self.op_3.first_bool.clicked.connect(lambda: self.expression_clicked(3, 0))
        self.op_3.second_bool.clicked.connect(lambda: self.expression_clicked(3, 1))
        self.op_3.third_bool.clicked.connect(lambda: self.expression_clicked(3, 2))
        self.op_3.fourth_bool.clicked.connect(lambda: self.expression_clicked(3, 3))

        self.op_4 = Expression(
            self, 1500, 70, 50, 350, show_first_brackets=True, first_op='OR',
            show_second_brackets=True, third_op='OR'
        )
        self.op_4.first_bool.clicked.connect(lambda: self.expression_clicked(4, 0))
        self.op_4.second_bool.clicked.connect(lambda: self.expression_clicked(4, 1))
        self.op_4.third_bool.clicked.connect(lambda: self.expression_clicked(4, 2))
        self.op_4.fourth_bool.clicked.connect(lambda: self.expression_clicked(4, 3))

        self.op_5 = Expression(
            self, 1500, 70, 50, 450, show_second_brackets=True, first_op='AND',
            second_op='XOR', show_first_brackets=True, third_op='AND'
        )
        self.op_5.first_bool.clicked.connect(lambda: self.expression_clicked(5, 0))
        self.op_5.second_bool.clicked.connect(lambda: self.expression_clicked(5, 1))
        self.op_5.third_bool.clicked.connect(lambda: self.expression_clicked(5, 2))
        self.op_5.fourth_bool.clicked.connect(lambda: self.expression_clicked(5, 3))

        self.op_6 = Expression(
            self, 1500, 70, 50, 550, show_second_brackets=True, first_op='OR',
            second_op='XOR', show_first_brackets=True, third_op='OR'
        )
        self.op_6.first_bool.clicked.connect(lambda: self.expression_clicked(6, 0))
        self.op_6.second_bool.clicked.connect(lambda: self.expression_clicked(6, 1))
        self.op_6.third_bool.clicked.connect(lambda: self.expression_clicked(6, 2))
        self.op_6.fourth_bool.clicked.connect(lambda: self.expression_clicked(6, 3))

        self.op_7 = Expression(
            self, 1500, 70, 50, 650, negate=True,
        )
        self.op_7.first_bool.clicked.connect(lambda: self.expression_clicked(7, 0))
        self.op_7.second_bool.clicked.connect(lambda: self.expression_clicked(7, 1))
        self.op_7.third_bool.clicked.connect(lambda: self.expression_clicked(7, 2))
        self.op_7.fourth_bool.clicked.connect(lambda: self.expression_clicked(7, 3))

        self.op_8 = Expression(
            self, 1500, 70, 50, 750, first_op='OR', negate=True, second_op='OR', third_op='OR'
        )
        self.op_8.first_bool.clicked.connect(lambda: self.expression_clicked(8, 0))
        self.op_8.second_bool.clicked.connect(lambda: self.expression_clicked(8, 1))
        self.op_8.third_bool.clicked.connect(lambda: self.expression_clicked(8, 2))
        self.op_8.fourth_bool.clicked.connect(lambda: self.expression_clicked(8, 3))


        self.setStyleSheet('background-color: #2c3e4c')
        self.setWindowTitle('Bool Operators')
        self.show()
        self.resize(1600, 900)
        self.move(200, 50)

        for i in range(9):
            self.evaluate(i)

    def evaluate(self, expression_number):
        if expression_number == 1:
            self.op_1.state.set_state(
                self.bool_values[0][0] and
                self.bool_values[0][1] and
                self.bool_values[0][2] and
                self.bool_values[0][3]
            )
        elif expression_number == 2:
            self.op_2.state.set_state(
                self.bool_values[1][0] or
                self.bool_values[1][1] or
                self.bool_values[1][2] or
                self.bool_values[1][3]
            )
        elif expression_number == 3:
            self.op_3.state.set_state(
                (self.bool_values[2][0] and self.bool_values[2][1])
                or
                (self.bool_values[2][2] and self.bool_values[2][3])
            )
        elif expression_number == 4:
            self.op_4.state.set_state(
                (self.bool_values[3][0] or self.bool_values[3][1])
                and
                (self.bool_values[3][2] or self.bool_values[3][3])
            )
        elif expression_number == 5:
            self.op_5.state.set_state(
                (self.bool_values[4][0] and self.bool_values[4][1])
                ^
                (self.bool_values[4][2] and self.bool_values[4][3])
            )
        elif expression_number == 6:
            self.op_6.state.set_state(
                (self.bool_values[5][0] or self.bool_values[5][1])
                ^
                (self.bool_values[5][2] or self.bool_values[5][3])
            )
        elif expression_number == 7:
            self.op_7.state.set_state(
                not(
                        self.bool_values[6][0]
                        and self.bool_values[6][1]
                        and self.bool_values[6][2]
                        and self.bool_values[6][3]
                )
            )
        elif expression_number == 8:
            self.op_8.state.set_state(
                not(
                        self.bool_values[7][0]
                        or self.bool_values[7][1]
                        or self.bool_values[7][2]
                        or self.bool_values[7][3]
                )
            )


    def expression_clicked(self, expression, val):
        if expression == 1:
            self.bool_values[0][val] = not self.bool_values[0][val]
            self.op_1.first_bool.set_state(self.bool_values[0][0])
            self.op_1.second_bool.set_state(self.bool_values[0][1])
            self.op_1.third_bool.set_state(self.bool_values[0][2])
            self.op_1.fourth_bool.set_state(self.bool_values[0][3])
            self.evaluate(1)
        elif expression == 2:
            self.bool_values[1][val] = not self.bool_values[1][val]
            self.op_2.first_bool.set_state(self.bool_values[1][0])
            self.op_2.second_bool.set_state(self.bool_values[1][1])
            self.op_2.third_bool.set_state(self.bool_values[1][2])
            self.op_2.fourth_bool.set_state(self.bool_values[1][3])
            self.evaluate(2)
        elif expression == 3:
            self.bool_values[2][val] = not self.bool_values[2][val]
            self.op_3.first_bool.set_state(self.bool_values[2][0])
            self.op_3.second_bool.set_state(self.bool_values[2][1])
            self.op_3.third_bool.set_state(self.bool_values[2][2])
            self.op_3.fourth_bool.set_state(self.bool_values[2][3])
            self.evaluate(3)
        elif expression == 4:
            self.bool_values[3][val] = not self.bool_values[3][val]
            self.op_4.first_bool.set_state(self.bool_values[3][0])
            self.op_4.second_bool.set_state(self.bool_values[3][1])
            self.op_4.third_bool.set_state(self.bool_values[3][2])
            self.op_4.fourth_bool.set_state(self.bool_values[3][3])
            self.evaluate(4)
        elif expression == 5:
            self.bool_values[4][val] = not self.bool_values[4][val]
            self.op_5.first_bool.set_state(self.bool_values[4][0])
            self.op_5.second_bool.set_state(self.bool_values[4][1])
            self.op_5.third_bool.set_state(self.bool_values[4][2])
            self.op_5.fourth_bool.set_state(self.bool_values[4][3])
            self.evaluate(5)
        elif expression == 6:
            self.bool_values[5][val] = not self.bool_values[5][val]
            self.op_6.first_bool.set_state(self.bool_values[5][0])
            self.op_6.second_bool.set_state(self.bool_values[5][1])
            self.op_6.third_bool.set_state(self.bool_values[5][2])
            self.op_6.fourth_bool.set_state(self.bool_values[5][3])
            self.evaluate(6)
        elif expression == 7:
            self.bool_values[6][val] = not self.bool_values[6][val]
            self.op_7.first_bool.set_state(self.bool_values[6][0])
            self.op_7.second_bool.set_state(self.bool_values[6][1])
            self.op_7.third_bool.set_state(self.bool_values[6][2])
            self.op_7.fourth_bool.set_state(self.bool_values[6][3])
            self.evaluate(7)
        elif expression == 8:
            self.bool_values[7][val] = not self.bool_values[7][val]
            self.op_8.first_bool.set_state(self.bool_values[7][0])
            self.op_8.second_bool.set_state(self.bool_values[7][1])
            self.op_8.third_bool.set_state(self.bool_values[7][2])
            self.op_8.fourth_bool.set_state(self.bool_values[7][3])
            self.evaluate(8)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Program()
    sys.exit(app.exec_())