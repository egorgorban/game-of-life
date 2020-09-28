from random import randint


class Cell:
    def __init__(self):
        self._status = 'Dead'

    # пометить ячейку живой
    def set_alive(self):
        self._status = 'Alive'

    # пометить ячейку мёртвой
    def set_dead(self):
        self._status = 'Dead'

    # является ли ячейка живой
    def is_alive(self):
        if self._status == 'Alive':
            return True
        return False

    # напечатать ячейку в консоли (пустая если мертва, '0' если живая)
    def print_cell(self):
        if self.is_alive():
            return '0'
        return ' '

    # -------------------------------------------------------------------


class Board:
    def __init__(self, r, c):
        self._rows = r
        self._columns = c
        
        # сетка ячеек
        self._grid = [[Cell() for column_cells in range(self._columns)] for row_cells in range(self._rows)]

        self._make_board()
        
    # создать доску
    def _make_board(self):
        for row in self._grid:
            for cell in row:
                dead_or_alive = randint(0, 3)
                # 25% ячеек живы при нулевой итерации
                if dead_or_alive == 3:
                    cell.set_alive()
    
    # возвращает список соседей текущей ячейки
    def get_neighbours(self, cur_row, cur_col):
        neighbour_list = []  # список соседей текущей клетки
        
        # проверяем предыдущий, текущий и следующий ряд/столбец
        for row in range(-1, 2):
            for col in range(-1, 2):
               
                neighbour_row = cur_row + row
                neighbour_col = cur_col + col

                is_neighbour = True
                
                # клетка не является соседом, если это текущая клетка
                if neighbour_row == cur_row and neighbour_col == cur_col:
                    is_neighbour = False
                    
                # а также, если текущая клетка - граничная, мы не можем рассматривать клетки за пределами сетки
                if neighbour_row < 0 or neighbour_row >= self._rows:
                    is_neighbour = False
                if neighbour_col < 0 or neighbour_col >= self._columns:
                    is_neighbour = False

                if is_neighbour:
                    neighbour_list.append(self._grid[neighbour_row][neighbour_col])
        return neighbour_list

    # отрисовываем доску
    def draw_board(self):
        for row in self._grid:
            for col in row:
                print(col.print_cell(), end='  ')
            print()

    # обновляем доску - генерируем следующее поколение
    def renew_board(self):
        print('new generation')
        to_live = []  # список ячеек, которые должны быть живыми в новом поколении
        to_kill = []  # список ячеек, которые должны быть мёртвыми в новом поколении

        for row in range(len(self._grid)):
            for col in range(len(self._grid[row])):
                # получаем список соседей для каждой ячейки
                get_neighbours = self.get_neighbours(row, col)
                alive_neighbours = []
                
                # и смотрим количество живых соседей
                for _cell in get_neighbours:
                    if _cell.is_alive():
                        alive_neighbours.append(_cell)

                cur_cell = self._grid[row][col]
                
                # реализуем работу автомата
                status_cell = cur_cell.is_alive()

                if status_cell:
                    if len(alive_neighbours) < 2 or len(alive_neighbours) > 3:
                        to_kill.append(cur_cell)
                    else:
                        to_live.append(cur_cell)
                else:
                    if len(alive_neighbours) == 3:
                        to_live.append(cur_cell)
        # обновляем информацию для всех клеток
        for cell in to_live:
            cell.set_alive()
        for cell in to_kill:
            cell.set_dead()

    # -------------------------------------------------------------------


def main():
    rows = 20
    columns = 20

    game_of_life_board = Board(rows, columns)
    game_of_life_board.draw_board()

    print('Press enter to go or 0 to exit:')
    user_action = input()

    while user_action != '0':
        game_of_life_board.renew_board()
        game_of_life_board.draw_board()

        print('Press enter to go or 0 to exit:')
        user_action = input()


if __name__ == '__main__':
    main()
