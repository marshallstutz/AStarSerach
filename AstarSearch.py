import pygame
import sys
import math
import keyboard
import numpy as np
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gscore = 100000
        self.fscore = 100000
        self.came_from = None
        self.locked = False
        self.overrideable = True

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#Constants
ROWS = 50
COLS = 50
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255, 0,0)
GREEN = (0,255,0)
GRAY = (128, 128, 128)
GOLD = (212, 175, 55)
BLUE = (0, 0, 255)

#globals
screen = None
rect_list = []
start = None
goal = None

def lowest_score(arr):
    current_low = 10000000
    current_node = None
    for item in arr:
        if item.fscore < current_low:
            current_low = item.fscore
            current_node = item
    return current_node

def distance(current, neighbor):
    if current.x != neighbor.x and current.y != neighbor.y:
        return 1.41
    return 1

def get_dist(one, two):
    return math.sqrt((math.fabs(two.x - one.x))**2 + (math.fabs(two.y - one.y))**2)


def get_neighbors(node, arr):
    temp_list = []
    if node.x > 0 and node.y > 0:
        if not arr[node.x-1][node.y -1].locked:
            temp_list.append(arr[node.x-1][node.y-1])
    if node.y > 0 and node.x < ROWS-1:
        if not arr[node.x +1][node.y - 1].locked:
            temp_list.append(arr[node.x+1][node.y-1])
    if node.y < COLS-1 and node.x > 0:
        if not arr[node.x - 1][node.y + 1].locked:
            temp_list.append(arr[node.x-1][node.y+1])
    if node.x < ROWS-1 and node.y < COLS-1:
        if not arr[node.x + 1][node.y + 1].locked:
            temp_list.append(arr[node.x+1][node.y+1])
    if node.x > 0:
        if not arr[node.x - 1][node.y].locked:
            temp_list.append(arr[node.x - 1][node.y])
    if node.y > 0:
        if not arr[node.x][node.y - 1].locked:
            temp_list.append(arr[node.x][node.y - 1])
    if node.x < ROWS-1:
        if not arr[node.x +1][node.y].locked:
            temp_list.append(arr[node.x +1][node.y])
    if node.y < COLS-1:
        if not arr[node.x][node.y +1].locked:
            temp_list.append(arr[node.x][node.y + 1])
    return temp_list


def final_path(current):
    total_path = [current]
    while current.came_from is not None:
        total_path.insert(0, current)
        current = current.came_from
    return total_path

def initialize_board(arr):
    for x in range(ROWS):
        arr.append(0)
        arr[x] = []
        for y in range(COLS):
            arr[x].append(0)
            arr[x][y] = Node(x, y)

def get_node_from_point(point, full_array):
    for y_array in full_array:
        for item in y_array:
            if point.x == item.x and point.y == item.y:
                return item
    return None

def a_star(start, goal, full_array):
    open_set = [full_array[start.x][start.y]]
    open_set[0].gscore = 0
    open_set[0].fscore = get_dist(open_set[0], full_array[goal.x][goal.y])
    while open_set:
        current = lowest_score(open_set)
        if current.x == goal.x and current.y == goal.y:
            return final_path(current)
        circle_node(current, GREEN)
        pygame.display.update()
        x = current.x
        y = current.y

        open_set.remove(current)
        for item in get_neighbors(current, full_array):
            temp_gscore = current.gscore + distance(current, item)
            if temp_gscore < item.gscore:
                item.came_from = current
                item.gscore = temp_gscore
                item.fscore = temp_gscore + get_dist(item, goal)
                if item not in open_set:
                    open_set.append(item)
                    circle_node(item, RED)
                    pygame.display.update()
        circle_node(current, WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.update()
        pygame.time.wait(100)
    return -1

def init_pygame():
    global screen
    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption('A* Search')
    screen.fill(BLACK)
    pygame.display.update()
    return screen

def color_rects(board):
    for i in range(ROWS):
        for j in range(COLS):
            temp_rect = pygame.Rect(20 * i , 20 * j, 19, 19)
            pygame.draw.rect(screen, GRAY, temp_rect)
            rect_list.append(temp_rect)

def set_startgoal(color, board, locked):
    for s in rect_list:
        if s.collidepoint(pygame.mouse.get_pos()) and board[int(s.x/20)][int(s.y/20)].overrideable:
            pygame.draw.rect(screen, color, s)
            pygame.display.update()
            board[int(s.x/20)][int(s.y/20)].locked = locked
            board[int(s.x / 20)][int(s.y / 20)].overrideable = False
            return Point(int(s.x / 20), int(s.y/20))
    return None

def main():
    board = []
    initialize_board(board)
    global screen
    global start
    global goal
    screen = init_pygame()
    #draw base rectangles
    color_rects(board)
    #wait until space bar is hit to start the game and start and end nodes are selected
    #start = Point(2,2)
    #goal = Point(45,45)
    while not keyboard.is_pressed(' '):
        while start is None:
            if pygame.mouse.get_pressed()[0]:
                start = set_startgoal(BLUE, board, False)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                pygame.display.update()
                pygame.time.wait(100)
        while goal is None:
            if pygame.mouse.get_pressed()[0]:
                goal = set_startgoal(GOLD, board, False)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                pygame.display.update()
        if pygame.mouse.get_pressed()[0]:
            set_startgoal(BLACK, board, True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.update()
    path = a_star(start, goal, board)
    if path is not -1:
        draw_path(path)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.update()
        pygame.time.wait(100)

def draw_path(path):
    curr = path[0]
    draw_line(start.x * 20 + 10, start.y * 20 + 10, curr.x * 20 + 10, curr.y * 20 + 10)
    pygame.display.update()
    pygame.time.wait(100)
    for i in range(0, len(path)):
        draw_line(curr.x*20 + 10, curr.y*20 + 10, path[i].x * 20 + 10, path[i].y * 20 + 10)
        pygame.display.update()
        pygame.time.wait(100)
        curr = path[i]
    draw_line(curr.x * 20 + 10, curr.y * 20 + 10, goal.x * 20 + 10, goal.y * 20 + 10)
    pygame.display.update()
    pygame.time.wait(100)

def draw_line(x1, y1, x2, y2):
    pygame.draw.line(screen, GREEN, (x1, y1), (x2, y2), 4)

def circle_node(node, color):
    pygame.draw.circle(screen, color, (node.x * 20 + 10,node.y * 20 + 10), 7)

main()
