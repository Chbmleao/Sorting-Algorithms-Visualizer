import pygame
import random
import math

pygame.init()


class DrawInfo:
    black = (42, 47, 79)
    white = (253, 226, 243)
    green = (252, 79, 0)
    red = (247, 149, 64)
    gray = (145, 127, 179)
    lightGray = (229, 190, 236)

    backgroundColor = black
    blockColors = [gray, lightGray, white]

    sidePad = 100
    topPad = 200

    font = pygame.font.SysFont("arial", 25)
    largeFont = pygame.font.SysFont("arial", 35)

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
        self.blockHeight = math.floor(
            (self.height - self.topPad) / (self.maxVal - self.minVal)
        )

        self.startX = round(self.sidePad // 2)


def createList(n, minVal, maxVal):
    list = []

    for i in range(n):
        randomNumber = random.randint(minVal, maxVal)
        list.append(randomNumber)

    return list


def draw(drawInfo, algorithmName, ascending):
    drawInfo.window.fill(drawInfo.backgroundColor)

    drawText(drawInfo, algorithmName, ascending)

    drawList(drawInfo)

    pygame.display.update()


def drawText(drawInfo, algorithmName, ascending):
    tittleStr = algorithmName
    if ascending:
        tittleStr += " - Ascending"
    else:
        tittleStr += " - Descending"
    tittle = drawInfo.largeFont.render(tittleStr, 1, drawInfo.white)
    x = drawInfo.width / 2 - tittle.get_width() / 2
    y = 10
    drawInfo.window.blit(tittle, (x, y))

    controls = drawInfo.font.render(
        "R - reset | Space - Sort | A - Ascending | D - Descending", 1, drawInfo.white
    )
    x = drawInfo.width / 2 - controls.get_width() / 2
    y += tittle.get_height() + 10
    drawInfo.window.blit(controls, (x, y))

    algorithms = drawInfo.font.render(
        "I - Insertion Sort | B - Bubble Sort | Q - Quick Sort", 1, drawInfo.white
    )
    x = drawInfo.width / 2 - algorithms.get_width() / 2
    y += controls.get_height() + 10
    drawInfo.window.blit(algorithms, (x, y))


def drawList(drawInfo, colorPositions={}, clearBackground=False):
    if clearBackground:
        clearRect = (
            drawInfo.sidePad // 2,
            drawInfo.topPad,
            drawInfo.width - drawInfo.sidePad // 2,
            drawInfo.height - drawInfo.topPad,
        )
        pygame.draw.rect(drawInfo.window, drawInfo.backgroundColor, clearRect)

    currentX = drawInfo.startX
    currentIndex = 0
    for elem in drawInfo.list:
        currentBlockHeight = elem * drawInfo.blockHeight

        currentY = drawInfo.height - currentBlockHeight

        currentColor = drawInfo.blockColors[currentIndex % len(drawInfo.blockColors)]
        if currentIndex in colorPositions:
            currentColor = colorPositions[currentIndex]

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
        currentIndex += 1

    if clearBackground:
        pygame.display.update()


def insertionSort(drawInfo, ascending=True):
    list = drawInfo.list
    n = len(list)
    for i in range(1, n):
        key = list[i]
        j = i - 1

        while j >= 0 and (
            (key < list[j] and ascending) or (key > list[j]) and not ascending
        ):
            list[j + 1] = list[j]
            j -= 1
            drawList(drawInfo, {j + 1: (drawInfo.red), j: (drawInfo.green)}, True)
            yield True

        list[j + 1] = key


def bubbleSort(drawInfo, ascending=True):
    list = drawInfo.list
    n = len(list)
    for i in range(n):
        for j in range(0, n - i - 1):
            if (list[j] > list[j + 1] and ascending) or (
                list[j] < list[j + 1] and not ascending
            ):
                list[j], list[j + 1] = list[j + 1], list[j]
                drawList(drawInfo, {j + 1: (drawInfo.red), j: (drawInfo.green)}, True)
                yield True


def main():
    run = True
    clock = pygame.time.Clock()

    listSize = 50
    minListVal = 0
    maxListVal = 100

    list = createList(listSize, minListVal, maxListVal)
    drawInfo = DrawInfo(1366, 768, list)

    sorting = False
    ascending = True

    sortingAlgorithm = insertionSort
    sortingAlgorithmName = "Insertion Sort"
    sortingAlgorithmGenerator = None

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sortingAlgorithmGenerator)
            except StopIteration:
                sorting = False
        else:
            draw(drawInfo, sortingAlgorithmName, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                list = createList(listSize, minListVal, maxListVal)
                drawInfo.setList(list)
                sorting = False

            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sortingAlgorithmGenerator = sortingAlgorithm(drawInfo, ascending)

            elif event.key == pygame.K_a and not sorting:
                ascending = True

            elif event.key == pygame.K_d and not sorting:
                ascending = False

            elif event.key == pygame.K_i and not sorting:
                sortingAlgorithm = insertionSort
                sortingAlgorithmName = "Insertion Sort"

            elif event.key == pygame.K_b and not sorting:
                sortingAlgorithm = bubbleSort
                sortingAlgorithmName = "Bubble Sort"

    pygame.quit()


if __name__ == "__main__":
    main()
