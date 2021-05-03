import pygame


class Node:
    pos = tuple()
    walkable = True
    g_cost = 0
    h_cost = 0
    parent = None

    def f_cost(self):
        return self.g_cost + self.h_cost


def get_distance(node_a, node_b):
    global matrix, start, end

    dst_x = abs(node_a.pos[0] - node_b.pos[0])
    dst_y = abs(node_a.pos[1] - node_b.pos[1])

    if dst_x > dst_y:
        return 14 * dst_y + 10 * (dst_x - dst_y)
    return 14 * dst_x + 10 * (dst_y - dst_x)


def get_neighbours(node):
    global n
    neighbours = []

    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue

            check_x = node.pos[0] + x
            check_y = node.pos[1] + y

            if 0 <= check_x < n and 0 <= check_y < n:
                neighbours.append(matrix[check_x][check_y])

    return neighbours


def find_path():
    global matrix, matrix_of_costs, start, end

    open_set = []
    close_set = []

    start_node = Node()
    start_node.pos = start

    end_node = Node()
    end_node.pos = end

    open_set.append(start_node)

    while len(open_set) > 0:
        current_node = open_set[0]
        for i in range(len(open_set)):  # поиск клетки с min f_cost
            if open_set[i].f_cost() < current_node.f_cost() or open_set[i].f_cost() == current_node.f_cost() and \
                    open_set[
                        i].h_cost < current_node.h_cost:
                current_node = open_set[i]

        open_set.remove(current_node)
        close_set.append(current_node)

        if current_node.pos == end:
            draw_way(start_node, current_node)
            return

        for neighbour in get_neighbours(current_node):
            try:
                close_set.index(neighbour)
                neighbour_closed = True
            except ValueError:
                neighbour_closed = False

            if neighbour.walkable == False or neighbour_closed == True:
                continue
            try:
                open_set.index(neighbour)
                neighbour_opened = True
            except ValueError:
                neighbour_opened = False

            new_movement = current_node.g_cost + get_distance(current_node, neighbour)

            if new_movement < neighbour.g_cost or neighbour_opened == False:
                neighbour.g_cost = new_movement
                neighbour.h_cost = get_distance(neighbour, end_node)
                neighbour.parent = current_node

                if neighbour_opened == False:
                    open_set.append(neighbour)


def retrace(start_node, end_node):
    path = []

    current_node = end_node

    while current_node != start_node:
        path.append(current_node.pos)
        current_node = current_node.parent

    return path


def draw_way(start_node, end_node):
    global surface, size
    path = retrace(start_node, end_node)

    for i in path:  # path - координаты клеток
        color = pygame.Color(70, 70, 220)

        pygame.draw.rect(surface, color, (size * i[0], size * i[1], size, size))

        pygame.display.update()


def draw_matrix():
    global surface, size, n
    for i in range(n):
        for j in range(n):
            text = font.render(f"{i},{j}", False, (0, 0, 0))

            # определение цвета
            if i == start[0] and j == start[1]:
                color = pygame.Color(74, 228, 80)
            elif i == end[0] and j == end[1]:
                color = pygame.Color(180, 192, 245)
            elif matrix[i][j].walkable == False:
                color = pygame.Color(47, 63, 61)
            else:
                color = pygame.Color(200, 210, 200)

            pygame.draw.rect(surface, color, (size * i, size * j, size, size))
            # surface.blit(text, (size*i + size/4, size*j + size/4))
            pygame.display.update()


# сторона квадрата
n = 20
size = 25

pygame.init()

surface = pygame.display.set_mode((size * n, size * n))
pygame.display.set_caption("App")
font = pygame.font.SysFont('Comic Sans MS', 30)

# создание клеток
matrix = [[0] * n for i in range(n)]  # false если это препятсвие

for i in range(n):
    for j in range(n):
        matrix[i][j] = Node()
        matrix[i][j].pos = (i, j)

# начало
start = (n - 1, 0)

# конец
end = (0, n - 1)

print(matrix)

run = True
already_drawn = False
draw_matrix()

while run:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN and already_drawn == False:
            already_drawn = True
            find_path()
        elif event.type == pygame.KEYDOWN and already_drawn == True:
            already_drawn = False
            draw_matrix()

        if event.type == pygame.MOUSEBUTTONDOWN:
            cords = pygame.mouse.get_pos()

            x = cords[0] // size
            y = cords[1] // size
            if x == end[0] and y == end[1]:
                for i in range(n):
                    for j in range(n):
                        matrix[i][j].walkable = True
            else:
                if matrix[x][y].walkable == False:
                    matrix[x][y].walkable = True
                else:
                    matrix[x][y].walkable = False
            already_drawn = False
            draw_matrix()

pygame.quit()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
