from random import randint, shuffle
from Tkinter import Frame, Tk, Button, Toplevel, Label, W
from sudoku import solvable, solve, inflate, already_valid


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
        self.control_frame.grid(row=1, column=0, sticky=W)
        self.buttons = self._create_buttons()
        self.clear_btn = Button(self.control_frame, text='Clear',
                                command=lambda: self.clear())
        self.solve_btn = Button(self.control_frame, text='Solve',
                                command=lambda: self.attempt())
        self.easy_btn = Button(self.control_frame, text='Easy',
                               command=lambda: self.puzzle(easy, 81 - 36))
        self.med_btn = Button(self.control_frame, text='Medium',
                              command=lambda: self.puzzle(easy, 81 - 46))
        self.hard_btn = Button(self.control_frame, text='Hard',
                               command=lambda: self.puzzle(hard, 81 - 56))
        self.easy_btn.grid(row=0, column=0)
        self.med_btn.grid(row=0, column=1)
        self.hard_btn.grid(row=0, column=2)
        self.clear_btn.grid(row=0, column=3)
        self.solve_btn.grid(row=0, column=4)

        # start
        self.root.mainloop()

    def _load(self, filename):
        problems = list()
        try:
            with open(filename, 'r') as f:
                problems = f.readlines()
        except IOError:
            print 'IOError: Cannot open', filename
        return problems

    def clear_color(self):
        for x in range(9):
            for y in range(9):
                btn = self.buttons[x][y]
                btn['bg'] = 'white'

    def clear(self):
        cleared = [[0 for y in range(9)] for x in range(9)]
        self.set_buttons(cleared)
        self.clear_color()

    def pick(self, problems):
        problem = inflate(problems[randint(0, len(problems))])
        self.set_buttons(problem)

    def puzzle(self, problems, n):
        problem = inflate(problems[randint(0, len(problems))])
        solve(0, 0, problem)
        locs = list()
        for x in range(9):
            for y in range(9):
                locs.append((x, y))
        shuffle(locs)

        while n > 0:
            loc = locs.pop()
            x, y = loc
            problem[x][y] = 0
            n -= 1

        self.set_buttons(problem)


    def cycle(self, x, y):
        btn = self.buttons[x][y]
        val = int(btn['text'])
        if val == 9:
            val = 0
        else:
            val += 1
        btn['text'] = str(val)

    def set_buttons(self, arr):
        for x in range(9):
            for y in range(9):
                btn = self.buttons[x][y]
                btn.config(text=str(arr[x][y]))

    def get_buttons(self):
        arr = list()
        for x in range(9):
            row = list()
            for y in range(9):
                row.append(int(self.buttons[x][y]['text']))
            arr.append(row)
        return arr

    def show_troublemakers(self, arr):
        for x in range(9):
            for y in range(9):
                if arr[x][y] != 0:
                    if already_valid(x, y, arr):
                        self.buttons[x][y]['bg'] = 'white'
                    else:
                        self.buttons[x][y]['bg'] = 'red'

    def double_check(self):
        arr = self.get_buttons()
        if not solvable(arr):
            self.show_troublemakers(arr)
            return False
        return True

    def error_popup(self):
        tl = Toplevel()
        message = Label(tl, text='Cannot solve grid!')
        message.pack()
        close = Button(tl, text='Okay', command=tl.destroy)
        close.pack()

    def attempt(self):
        if self.double_check():
            self.clear_color()
            board = self.get_buttons()
            solve(0, 0, board)
            self.set_buttons(board)
        else:
            self.error_popup()

    def _create_buttons(self):
        buttons = list()

        for x in range(9):
            row = list()
            for y in range(9):
                btn = Button(self.sudoku_frame, text='0', bg='white',
                             command=lambda x=x, y=y: self.cycle(x, y))
                btn.grid(row=x, column=y)
                row.append(btn)
            buttons.append(row)

        return buttons


if __name__ == '__main__':
    SudokuBoard()
