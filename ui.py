from random import randint
from Tkinter import Frame, Tk, Button
from sudoku import solvable, solve, inflate


class SudokuBoard(object):

    def __init__(self):
        # UI
        self.root = Tk()
        self.root.resizable(0, 0)
        self.root.title('Sudoku Solver')

        # problem sets
        easy = self._load('problems/easy')
        hard = self._load('problems/hard')

        # frames and buttons
        self.sudoku_frame = Frame(self.root)
        self.control_frame = Frame(self.root)
        self.sudoku_frame.grid(row=0, column=0)
        self.control_frame.grid(row=1, column=0)
        self.buttons = self._create_buttons()
        self.clear_btn = Button(self.control_frame, text='Clear',
                                command=lambda: self.clear())
        self.solve_btn = Button(self.control_frame, text='Solve')
        self.easy_btn = Button(self.control_frame, text='Easy',
                               command=lambda: self.pick(easy))
        self.hard_btn = Button(self.control_frame, text='Hard',
                               command=lambda: self.pick(hard))
        self.easy_btn.grid(row=0, column=0)
        self.hard_btn.grid(row=0, column=1)
        self.clear_btn.grid(row=0, column=2)
        self.solve_btn.grid(row=0, column=3)

        # start
        self.root.mainloop()

    def _load(self, filename):
        problems = list()
        with open(filename, 'r') as f:
            problems = f.readlines()
        return problems

    def clear(self):
        cleared = [[0 for y in range(9)] for x in range(9)]
        self.set_buttons(cleared)

    def pick(self, problems):
        problem = inflate(problems[randint(0, len(problems))])
        self.set_buttons(problem)

    def set_buttons(self, arr):
        for x in range(9):
            for y in range(9):
                btn = self.buttons[x][y]
                btn.config(text=str(arr[x][y]))

    def attempt(self):
        pass

    def _create_buttons(self):
        buttons = list()

        for x in range(9):
            row = list()
            for y in range(9):
                btn = Button(self.sudoku_frame, text='0')
                btn.grid(row=x, column=y)
                row.append(btn)
            buttons.append(row)

        return buttons

if __name__ == '__main__':
    SudokuBoard()
