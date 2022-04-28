from random import randint
import copy

kord_ship = []      # все точки корабля для рамки
x3, y3 = 0, 0

class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Сюда уже стреляли"

class Board:
    def __init__(self, hid=False):
        self.position = []
        self.yes = True
        self.position = [[]]
        self.board = [[]]
        self.board = [['0' for i in range(6)] for j in range(6)]  # начальное заполнение доски нулями
        self.ship_install = False
        self.kor = []
        self.ship = {}      # словарь с точками всех кораблей
        self.lives = {}     # словарь с оставшимися жизнями кораблей
        self.liv = 0

    # обрисовка корабля рамкой в 1 клетку
    def ramka(self, position):
        self.position = position
        okrug = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        for x, y in self.position:
            for dx, dy in okrug:
                if (x + dx < 6) and (x + dx >= 0) and (y + dy < 6) and (y + dy >= 0):
                    if self.board[x + dx][y + dy] != "■":
                        self.board[x + dx][y + dy] = "."

    # добавление корабля на доску
    def add_ship(self, l):
        self.l = l
        self.ship_install = False
        attempts = 0    # количество попыток размещения корабля
        n = 0   # номер корабля

        while not self.ship_install and attempts < 2000:
            attempts += 1
            self.position = []
            temp_x = []
            temp_y = []
            self.kor = []
            x = randint(0, 5)  # координата Х
            y = randint(0, 5)  # координата У
            a = randint(0, 3)  # угол поворота
            self.ship_install = False
            if self.l == 1:                      # корабль из 1 клетки
                if self.board[x][y] == "0":
                    self.board[x][y] = "■"
                    self.position = [[x, y]]
                    self.kor = [Dot(x, y)]
                    self.ship_install = True
                    self.ramka(self.position)

            else:
                if a == 0:  # направление вверх
                    for i in range(self.l):
                        if x - i >= 0 and self.board[x - i][y] == "0":
                            self.position += [[x - i, y]]
                            temp_x += [x - i]
                            temp_y += [y]

                if a == 1:   # направление влево
                    for i in range(self.l):
                        if y + i <= 5 and self.board[x][y + i] == "0":
                            self.position += [[x, y + i]]
                            temp_x += [x]
                            temp_y += [y + i]

                if a == 2:  # направление вниз
                    for i in range(self.l):
                        if x + i <= 5 and self.board[x + i][y] == "0":
                            self.position += [[x + i, y]]
                            temp_x += [x + i]
                            temp_y += [y]

                if a == 3:  # направление влево
                    for i in range(self.l):
                        if y - i >= 0 and self.board[x][y - i] == "0":
                            self.position += [[x, y - i]]
                            temp_x += [x]
                            temp_y += [y - i]

                if len(self.position) == self.l:    # запись корабля на доску
                    self.ship_install = True
                    for j in range(self.l):
                        xt = temp_x[j]
                        yt = temp_y[j]
                        self.board[xt][yt] = "■"
                        self.kor.append(Dot(xt, yt))

        self.ramka(self.position)   # запись рамки вокруг корабля
        n += 1

    # установка всех кораблей на доске
    def set_board(self):
        attempts = 0
        n = 0
        lens = [3, 2, 2, 1, 1, 1, 1]    # набор кораблей на доске
        while n != 7 and attempts < 20:
            n = 0
            attempts += 1
            self.board = [['0' for i in range(6)] for j in range(6)]  # начальное заполнение доски нулями
            for l in lens:
                self.add_ship(l)
                if self.ship_install:
                    self.ship.update({n: self.kor})
                    self.lives.update({n: l})
                    n += 1
        for i in range(6):  # удаление рамки вокруг кораблей
            for j in range(6):
                if self.board[i][j] != "■":
                    self.board[i][j] = "0"
        return self.board

    # Печать одной доски
    def prt_pole(self, pole):
        self.pole = pole

        self.str_pole = f"{'-' * 15}"

        self.str_pole += "\n |1|2|3|4|5|6|\n"   # заголовок столбцов
        for i in range(7):
            self.str_pole += f"{i + 1}|"    # заголовок строк
            for j in range(6):  #
                self.str_pole += f"|".join(self.pole[i][j]) + "|"

            self.str_pole += f"\n"
        self.str_pole += f"{'-' * 14}"
        print(*self.str_pole)


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"

class Player:
    def __init__(self):
        board = Board()
        self.b3 = board.set_board()
        self.ship = board.ship
        self.lives = board.lives
        self.con = 7
        self.destruction = False    # корабль уничтожен
        self.wound = False          # корабль ранен
        self.old_wound = False      # имеется недобитый корабль
        self.new_wound = False      # второе попадание
        self.n = 0      # номер шага добивания корабля
        self.d = Dot(0, 0)      # точка 1-го попадания
        self.d1 = Dot(0, 0)     # точка 2-го попадания

    def shot(self, d, board):
        x = d.x
        y = d.y
        self.wound = False
        self.board = board
        if not ((0 <= d.x < 6) and (0 <= d.y < 6)):
            raise BoardOutException()

        if (self.board[x][y] == ".") or (self.board[x][y] == "X"):
            raise BoardUsedException()
        if self.board[x][y] == "0":
            self.board[x][y] = "."
        if self.board[x][y] == "■":
            self.board[x][y] = "X"
            self.wound = True   # ранен
            return True     # попадание
        
    # рамка вокруг убитого корабля
    def fff(self, position, board):

        okrug = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        for i in range(len(position)):
            b = position[i]
            x = b.x
            y = b.y
            for dx, dy in okrug:
                if (x + dx < 6) and (x + dx >= 0) and (y + dy < 6) and (y + dy >= 0):
                    if board[x + dx][y + dy] != "X":
                        board[x + dx][y + dy] = "."

    # проверка попадания в корабль
    def uchet(self, d, ship, lives, board):
        self.wound = False
        for i in range(len(ship.keys())):
            d1 = ship[i]
            if d in d1:
                print("Есть попадание!")
                lives[i] -= 1   # уменьшение жизни корабля
                if self.old_wound:      # второе попадание
                    self.new_wound = True
                self.old_wound = True   # есть раненый корабль
                self.wound = True   # попадание
                self.d = Dot(x3, y3)  # координаты 1-го попадания
                if lives[i] == 0:
                    print("Корабль уничтожен!")
                    self.destruction = True     # корабль убит
                    self.wound = False      # сброс ранения
                    self.new_wound = False
                    self.old_wound = False      # сброс "есть раненый"
                    self.fff(d1, board)     # обведение корабля рамкой
                    self.con -= 1       # уменьшение количества кораблей игрока


class Comp(Player):

    # определение точки выстрела компьютера
    def ask(self, board):
        ys = True
        din = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.x1 = 0
        self.y1 = 0
        self.dx = 0
        self.dy = 0
        global x3
        global y3

        if self.old_wound and not self.new_wound:       # 1-е ранение
            for dx, dy in din:      # поиск клетки возможной для выстрела рядом с раненой
                if (0 <= x3 + dx < 6) and (0 <= y3 + dy < 6):
                    if board[x3 + dx][y3 + dy] != "X" and board[x3 + dx][y3 + dy] != ".":
                        self.d1 = Dot(x3+dx, y3+dy)    # 2-я возможная раненая клетка корабля
                        return Dot(x3+dx, y3+dy)

        if self.old_wound and self.new_wound:      # 2-е ранение, корабль из 3-х клеток
            x, y = self.d.x, self.d.y
            x1, y1 = self.d1.x, self.d1.y

            # определение ориентации корабля из 3-х клеток

            if x - x1 == 0:     # Корабль вдоль оси Х
                if (y - y1) > 0:  # новая точка слева, стреляем направо
                    if (y + 1 <= 5) and (board[x][y + 1] != "." and board[x][y + 1] != "X"):
                        # точка справа для выстрела внутри поля и свободна
                        return Dot(x, y+1)
                    else:   # точка занята, идем в другую сторону
                        if (y - 2 >= 0) and (board[x][y-2] != "." and board[x][y - 2] != "X"):
                            # стреляем на другую сторону от новой раненой клетки
                            return Dot(x, y-2)
                else:   # новая точка справа
                    if (y - 1 > 0) and (board[x][y - 1] != "." and board[x][y - 1] != "X"):
                        # точка слева для выстрела внутри поля и свободна
                        return Dot(x, y - 1)
                    else:
                        if (y + 2 >= 0) and (board[x][y+2] != "." and board[x][y + 2] != "X"):
                            # стреляем на другую сторону от новой раненой клетки
                            return Dot(x, y+2)

            else:   # Корабль вдоль оси У
                if (x-x1) > 0:    # новая точка ранения сверху, стреляем вниз
                    if (x + 1 <= 5) and (board[x+1][y] != "." and board[x + 1][y] != "X"):
                        # точка снизу внутри поля и свободна
                        return Dot(x + 1, y)
                    else:
                        if (x - 2 >= 0) and (board[x-2][y] != "." and board[x - 2][y] != "X"):
                            # выстрел на 2 клетки вверх
                            return Dot(x-2, y)
                else:
                    if (x - 1 >= 0) and (board[x-1][y] != "." and board[x - 1][y] != "X"):
                        # точка сверху внутри поля и свободна
                        return Dot(x-1, y)
                    else:
                        if (x + 2 <= 5) and (board[x+2][y] != "." and board[x + 2][y] != "X"):
                            # выстрел на 2 клетки вниз
                            return Dot(x+2, y)

        # случайный выстрел
        if not self.wound:
            while ys:       # нет раненого корабля противника

                x1 = randint(0, 5)  # координата Х
                y1 = randint(0, 5)  # координата У
                if board[x1][y1] != "X" and board[x1][y1] != ".":
                    x3, y3 = x1, y1
                    return Dot(x1, y1)


class Human(Player):

    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите через пробел 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)

class Game:
    def __init__(self):
        self.comp = Comp()
        self.human = Human()
        self.ai = False
        self.h = True
        print(f"{'-'*70}\n"+f"{' '*30}" + "ИГРА МОРСКОЙ БОЙ\n\n" +
              "     Для выстрела в выбранную клетку наберите сначала номер строки,\n"
              "     затем через пробел, номер столбца выбранной клетки\n" + f"{'-'*70}\n"+f"{' '*30}")

    # печать горизонтально, 2 доски
    def prt_2pole(self, pole_comp, pole_chl):
        self.p_c = copy.deepcopy(pole_comp)

        for i in range(6):  # скрытие кораблей на доске компьютера
            for j in range(6):
                if self.p_c[i][j] == "■":
                    self.p_c[i][j] = "0"

        self.pole_chl = pole_chl
        self.str_pole = f"{'-' * 15}  {' ' * 2}  {'-' * 15}"
        print("       Доска компьютера", " " * 25, " Доска человека")
        self.str_pole += "\n |1|2|3|4|5|6|        |1|2|3|4|5|6|\n"

        for i in range(6):
            self.str_pole += f"{i + 1}|"
            for j in range(6):
                self.str_pole += f"|".join(self.p_c[i][j]) + "|"
            self.str_pole += f"{' ' * 6} {i + 1}|"
            for j in range(6):
                self.str_pole += f"|".join(self.pole_chl[i][j]) + "|"
            self.str_pole += f"\n"

        self.str_pole += f"{'-' * 14}  {' ' * 2}  {'-' * 15}"
        print(*self.str_pole)



    # шаг игры, передача хода
    def step(self, board_hum, board_comp, ship_hum, ship_comp, lives_hum, lives_comp):
        try:

            if self.h:
                print("ходит человек")
                d = self.human.ask()
                self.h = self.human.shot(d, board_comp)
                if self.h:
                    self.human.uchet(d, ship_comp, lives_comp, board_comp)
                else:
                    print("Мимо!")

            else:
                print("ходит компьютер")
                d = self.comp.ask(board_hum)
                self.h = not self.comp.shot(d, board_hum)
                if not self.h:
                    self.comp.uchet(d, ship_hum, lives_hum, board_hum)
                else:
                    print("Мимо!")
        except BoardException as e:
            print(e)



b2 = Game()
comp = Comp()
hum = Human()
u = True

while u:
    b2.prt_2pole(comp.b3, hum.b3)

    b2.step(hum.b3, comp.b3, hum.ship, comp.ship, hum.lives, comp.lives)

    if b2.comp.con == 0:
        print("Выиграл компьютер!")
        u = False

    if b2.human.con == 0:
        print("Выиграл человек!")
        u = False




