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
    pink = (183, 19, 117)

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
        "S - Selection Sort | I - Insertion Sort | B - Bubble Sort | Q - Quick Sort | M - Merge Sort",
        1,
        drawInfo.white,
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


def selectionSort(drawInfo, ascending=True):
    list = drawInfo.list
    listSize = len(list)
    for i in range(listSize):
        minIndex = i
        for j in range(i + 1, listSize):
            drawList(drawInfo, {j: (drawInfo.red), minIndex: (drawInfo.green)}, True)
            yield True
            if (list[minIndex] > list[j] and ascending) or (
                list[minIndex] < list[j] and not ascending
            ):
                minIndex = j

        list[i], list[minIndex] = list[minIndex], list[i]


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


def partition(list, low, high, drawInfo, ascending):
    pivotIndex = (low + high) // 2
    pivot = list[(low + high) // 2]
    i = low - 1
    j = high + 1

    while True:
        i += 1
        while (list[i] < pivot and ascending) or (list[i] > pivot and not ascending):
            i += 1

        j -= 1
        while (list[j] > pivot and ascending) or (list[j] < pivot and not ascending):
            j -= 1

        if i >= j:
            return j

        drawList(
            drawInfo,
            {i: (drawInfo.red), j: (drawInfo.red), pivotIndex: (drawInfo.pink)},
            True,
        )
        pygame.time.wait(100)
        list[i], list[j] = list[j], list[i]
        drawList(
            drawInfo,
            {i: (drawInfo.green), j: (drawInfo.green), pivotIndex: (drawInfo.pink)},
            True,
        )
        pygame.time.wait(100)


def quickSort(drawInfo, ascending=True):
    def _quickSort(drawInfo, low, high, ascending=True):
        if low < high:
            splitIndex = partition(drawInfo.list, low, high, drawInfo, ascending)
            _quickSort(drawInfo, low, splitIndex, ascending)
            _quickSort(drawInfo, splitIndex + 1, high, ascending)

    _quickSort(drawInfo, 0, len(drawInfo.list) - 1, ascending)


def mergeSort(drawInfo, ascending=True):
    width = 1
    list = drawInfo.list
    listSize = len(list)

    while width < listSize:
        l = 0
        while l < listSize:
            r = min(l + (width * 2 - 1), listSize - 1)
            m = min(l + width - 1, listSize - 1)

            merge(list, l, m, r, drawInfo, ascending)
            l += width * 2

        width *= 2


def merge(a, l, m, r, drawInfo, ascending=True):
    n1 = m - l + 1
    n2 = r - m
    L = [0] * n1
    R = [0] * n2
    for i in range(0, n1):
        L[i] = a[l + i]
    for i in range(0, n2):
        R[i] = a[m + i + 1]

    i, j, k = 0, 0, l
    while i < n1 and j < n2:
        if (L[i] <= R[j] and ascending) or (L[i] >= R[j] and not ascending):
            a[k] = L[i]
            i += 1
        else:
            a[k] = R[j]
            j += 1
        drawList(drawInfo, {k: drawInfo.green}, True)
        pygame.time.wait(100)
        k += 1

    while i < n1:
        a[k] = L[i]
        drawList(drawInfo, {k: drawInfo.green}, True)
        pygame.time.wait(100)
        i += 1
        k += 1

    while j < n2:
        a[k] = R[j]
        drawList(drawInfo, {k: drawInfo.green}, True)
        pygame.time.wait(100)
        j += 1
        k += 1


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
            if (
                sortingAlgorithmName != "Quick Sort"
                and sortingAlgorithmName != "Merge Sort"
            ):
                try:
                    next(sortingAlgorithmGenerator)
                except StopIteration:
                    sorting = False
            else:
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

            elif event.key == pygame.K_s and not sorting:
                sortingAlgorithm = selectionSort
                sortingAlgorithmName = "Selection Sort"

            elif event.key == pygame.K_i and not sorting:
                sortingAlgorithm = insertionSort
                sortingAlgorithmName = "Insertion Sort"

            elif event.key == pygame.K_b and not sorting:
                sortingAlgorithm = bubbleSort
                sortingAlgorithmName = "Bubble Sort"

            elif event.key == pygame.K_q and not sorting:
                sortingAlgorithm = quickSort
                sortingAlgorithmName = "Quick Sort"

            elif event.key == pygame.K_m and not sorting:
                sortingAlgorithm = mergeSort
                sortingAlgorithmName = "Merge Sort"

    pygame.quit()


if __name__ == "__main__":
    main()
