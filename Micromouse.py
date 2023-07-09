import numpy as np
import matplotlib.pyplot as plt
import tkinter
from tkinter import filedialog
import os
import cv2


def main():
    imgdir = get_image()
    maze = cv2.imread(imgdir, cv2.IMREAD_GRAYSCALE)
    solved = cv2.imread(imgdir)

    size = maze.shape[0]
    path = np.zeros(maze.shape+(2,), int)

    curmap = FloodFill(np.zeros(maze.shape, int))
    start = [30, 0]
    curpos = start
    curval = curmap[curpos[0]][curpos[1]]
    visited = [[False]*(size) for _ in range(size)]
    lastjunc = []

    while curval != 0:
        x, y = curpos
        visited[x][y] = True
        possible = []

        for i, j in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
            x1, y1 = x+i, y+j
            if x1 >= 0 and y1 >= 0 and x1 < size and y1 < size:
                if maze[x1][y1] == 255:
                    curmap[x1][y1] = 255
                    solved[x1][y1] = 200
                elif not visited[x1+i][y1+j]:
                    possible.append([x1+i, y1+j])

        curmap = FloodFill(curmap)

        if len(possible) > 1:
            lastjunc.append(curpos)

        if not possible:
            curpos = lastjunc.pop()
            continue

        next = possible[0]
        minval = curmap[next[0]][next[1]]

        for x1, y1 in possible[1:]:
            if curmap[x1][y1] < minval:
                minval = curmap[x1][y1]
                next = [x1, y1]

        path[next[0], next[1], :] = curpos

        curpos = next
        curval = curmap[curpos[0]][curpos[1]]


    while curpos != start:
        x, y = curpos
        solved[x][y][0] = 255
        curpos = list(path[x, y, :])
        solved[(x+curpos[0])//2][(y+curpos[1])//2][0] = 255
    solved[start[0], start[1], 2] = 255

    display_array(np.array(solved))


def FloodFill(flood_map):
    n = (flood_map.shape[0]+1)//2
    center = [[n-2, n-2], [n-2, n], [n, n-2], [n, n]]
    queue = [[n-2, n-2], [n-2, n], [n, n-2], [n, n]]

    while queue:
        x, y = queue.pop()
        val = flood_map[x][y]
        for i, j in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
            x1, y1 = x + i, y + j
            if x1 >= 0 and y1 >= 0 and x1 < n*2-1 and y1 < n*2-1:
                val1 = flood_map[x1][y1]
                val2 = flood_map[x1+i][y1+j]
                if val1 != 255 and (val2 > val + 1 or val2 == 0) and [x1+i, y1+j] not in center:
                    flood_map[x1+i][y1+j] = val + 1
                    queue.append([x1+i, y1+j])
    return flood_map


def display_array(array):
    array = array.repeat(50, 0).repeat(50, 1)
    plt.imshow(array, cmap='gray', vmin=0, vmax=255)
    plt.show()


def get_image():
    try:
        root = tkinter.Tk()
        root.attributes('-topmost', True)
        root.iconify() 
        currdir = os.getcwd()
        tempdir = filedialog.askopenfilename(parent=root, initialdir=currdir, title='Please select an image', filetypes=(("Image Files", "*.jpg;*.png;*.jpeg"),))
        root.destroy() 
        return tempdir
    except:
        print("Error selecting image")


main()