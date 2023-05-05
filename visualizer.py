import pygame
import random

pygame.init()


class DrawInfo:
    black = 0, 0, 0
    white = 255, 255, 255
    green = 0, 255, 0
    red = 255, 0, 0
    gray = 127, 127, 127
    lightGray = 191, 191, 191

    backgroundColor = black
    blockColors = [gray, lightGray, white]

    sidePad = 100
    topPad = 100

    def __init__(self, width, height, list):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithms Visualizer")
        self.setList(list)

    def setList(self, list):
        self.list = list
        self.maxVal = max(list)
        self.minVal = min(list)

        self.blockWidth = round((self.width - self.sidePad) / len(list))
        self.blockHeight = round(
            (self.height - self.topPad) / (self.maxVal - self.minVal)
        )

        self.startX = round(self.sidePad // 2)


def createList(n, minVal, maxVal):
    list = []

    for i in range(n):
        randomNumber = random.randint(minVal, maxVal)
        list.append(randomNumber)

    return list


def draw(drawInfo):
    drawInfo.window.fill(drawInfo.backgroundColor)

    drawList(drawInfo)

    pygame.display.update()


def drawList(drawInfo):
    currentX = drawInfo.startX
    currentColorIndex = 0
    for elem in drawInfo.list:
        currentBlockHeight = elem * drawInfo.blockHeight
        currentY = drawInfo.height - currentBlockHeight
        currentColor = drawInfo.blockColors[
            currentColorIndex % len(drawInfo.blockColors)
        ]
        pygame.draw.rect(
            drawInfo.window,
            currentColor,
            pygame.Rect(
                currentX,
                currentY,
                drawInfo.blockWidth,
                currentBlockHeight,
            ),
        )
        currentX += drawInfo.blockWidth
        currentColorIndex += 1


def main():
    run = True
    clock = pygame.time.Clock()

    listSize = 50
    minListVal = 0
    maxListVal = 100

    list = createList(listSize, minListVal, maxListVal)
    drawInfo = DrawInfo(800, 600, list)

    while run:
        clock.tick(60)

        draw(drawInfo)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                list = createList(listSize, minListVal, maxListVal)
                drawInfo.setList(list)

    pygame.quit()


if __name__ == "__main__":
    main()
