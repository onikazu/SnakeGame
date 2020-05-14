import sys
import random
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW


class Cons:
    BOARD_WIDTH = 300
    BOARD_HEIGHT = 300
    DELAY = 100
    DOT_SIZE = 10
    MAX_RAND_POS = 27

class Board(Canvas):
    def __init__(self):
        super().__init__(width=Cons.BOARD_WIDTH, height=Cons.BOARD_HEIGHT,
            background="black", highlightthickness=0)
        self.initGame()
        self.pack()

    def initGame(self):
        """initialize game"""
        self.inGame = True
        self.dots = 3
        self.score = 0

        # variables used to move snake object
        self.moveX = Cons.DOT_SIZE
        self.moveY = 0

        # starting apple coordinates
        self.appleX = 100
        self.appleY = 190

        self.loadImages()
        self.createObjects()
        self.locateApple()
        self.bind_all("<Key>", self.onKeyPressed)
        self.after(Cons.DELAY, self.onTimer)

    def loadImages(self):
        width = height = Cons.DOT_SIZE
        try:
            self.idot = Image.open("images/dot.png").resize((width, height))
            self.dot = ImageTk.PhotoImage(self.idot)
            self.ihead = Image.open("images/head.png").resize((width, height))
            self.head = ImageTk.PhotoImage(self.ihead)
            self.iapple = Image.open("images/apple.png").resize((width, height))
            self.apple = ImageTk.PhotoImage(self.iapple)
        except IOError as e:
            print(e)
            sys.exit(1)

    def createObjects(self):
        self.create_text(30, 10, text="Score: {0}".format(self.score),
            tag="score", fill="white")
        self.create_image(self.appleX, self.appleY, image=self.apple,
            anchor=NW, tag="apple")
        self.create_image(50, 50, image=self.head, anchor=NW, tag="head")
        self.create_image(30, 50, image=self.dot, anchor=NW, tag="dot")
        self.create_image(40, 50, image=self.dot, anchor=NW, tag="dot")

    def checkAppleCollision(self):
        apple = self.find_withtag("apple")
        head = self.find_withtag("head")
        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)
        for ovr in overlap:
            if apple[0] == ovr:
                self.score += 1
                x, y = self.coords(apple)
                self.create_image(x, y, image=self.dot, anchor=NW, tag="dot")
                self.locateApple()

    def moveSnake(self):
        dots = self.find_withtag("dot")
        head = self.find_withtag("head")
        items = dots + head

        z = 0
        while z < len(items) - 1:
            c1 = self.coords(items[z])
            c2 = self.coords(items[z+1])
            self.move(items[z], c2[0]-c1[0], c2[1]-c1[1])
            z += 1
        self.move(head, self.moveX, self.moveY)

    def checkCollisions(self):
        dots = self.find_withtag("dot")
        head = self.find_withtag("head")
        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)
        for dot in dots:
            for over in overlap:
                if over == dot:
                    self.inGame = False
        if x1 < 0:
            self.inGame = False

        if x1 > Cons.BOARD_WIDTH - Cons.DOT_SIZE:
            self.inGame = False

        if y1 < 0:
            self.inGame = False

        if y1 > Cons.BOARD_HEIGHT -  Cons.DOT_SIZE:
            self.inGame = False

    def locateApple(self):
        apple = self.find_withtag("apple")
        self.delete(apple[0])

        r = random.randint(0, Cons.MAX_RAND_POS)
        self.appleX = r * Cons.DOT_SIZE
        r = random.randint(0, Cons.MAX_RAND_POS)
        self.appleY = r * Cons.DOT_SIZE

        self.create_image(self.appleX, self.appleY, anchor=NW, image=self.apple, tag="apple")

    def onKeyPressed(self, e):
        key = e.keysym
        LEFT_CURSOR_KEY = "Left"
        RIGHT_CURSOR_KEY = "Right"
        UP_CURSOR_KEY = "Up"
        DOWN_CURSOR_KEY = "Down"

        if key == LEFT_CURSOR_KEY and self.moveX <= 0:
            self.moveX = -Cons.DOT_SIZE
            self.moveY = 0

        if key == RIGHT_CURSOR_KEY and self.moveX >= 0:
            self.moveX = Cons.DOT_SIZE
            self.moveY = 0

        if key == UP_CURSOR_KEY and self.moveY <= 0:
            self.moveX = 0
            self.moveY = -Cons.DOT_SIZE

        if key == DOWN_CURSOR_KEY and self.moveY >= 0:
            self.moveX = 0
            self.moveY = Cons.DOT_SIZE

    def onTimer(self):
        self.drawScore()
        self.checkCollisions()
        if self.inGame:
            self.checkAppleCollision()
            self.moveSnake()
            self.after(Cons.DELAY, self.onTimer)
        else:
            self.gameOver()

    def drawScore(self):
        score = self.find_withtag("score")
        self.itemconfigure(score, text="Score: {0}".format(self.score))

    def gameOver(self):
        print("GameOver")
        self.delete(ALL)
        self.create_text(self.winfo_width() // 2, self.winfo_height() // 2)

class Snake(Frame):
    def __init__(self):
        super().__init__()
        self.master.title("Snake")
        self.board = Board()
        self.pack()

def main():
    root = Tk()
    nib = Snake()
    root.mainloop()


if __name__ == "__main__":
    main()

