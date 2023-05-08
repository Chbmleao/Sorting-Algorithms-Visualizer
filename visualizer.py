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


def draw(drawInfo, algorithmName, ascending, clockTime):
    drawInfo.window.fill(drawInfo.backgroundColor)

    drawText(drawInfo, algorithmName, ascending, clockTime)

    drawList(drawInfo)

    pygame.display.update()


def drawText(drawInfo, algorithmName, ascending, clockTime):
    tittleStr = algorithmName
    if ascending:
        tittleStr += " - Ascending"
    else:
        tittleStr += " - Descending"
    tittleStr += " - Clock Time: " + str(clockTime)

    tittle = drawInfo.largeFont.render(tittleStr, 1, drawInfo.white)
    x = drawInfo.width / 2 - tittle.get_width() / 2
    y = 10
    drawInfo.window.blit(tittle, (x, y))

    controls = drawInfo.font.render(
        "R - reset | Space - Sort | A - Ascending | D - Descending | ↑ - Increase Speed | ↓ - Decrease Speed",
        1,
        drawInfo.white,
    )
    x = drawInfo.width / 2 - controls.get_width() / 2
    y += tittle.get_height() + 10
    drawInfo.window.blit(controls, (x, y))

    algorithms = drawInfo.font.render(
        "S - Selection Sort | I - Insertion Sort | B - Bubble Sort | Q - Quick Sort | M - Merge Sort | H - Heap Sort",
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
            yield j
            return j

        drawList(
            drawInfo,
            {i: (drawInfo.red), j: (drawInfo.red), pivotIndex: (drawInfo.pink)},
            True,
        )
        yield True
        list[i], list[j] = list[j], list[i]
        drawList(
            drawInfo,
            {i: (drawInfo.green), j: (drawInfo.green), pivotIndex: (drawInfo.pink)},
            True,
        )
        yield True


def quickSort(drawInfo, ascending=True):
    def _quickSort(drawInfo, low, high, ascending=True):
        if low < high:
            partitioning = True
            partitionGenerator = partition(
                drawInfo.list, low, high, drawInfo, ascending
            )
            splitIndex = 0

            while partitioning:
                try:
                    yield True
                    splitIndex = next(partitionGenerator)
                except StopIteration:
                    partitioning = False

            quickSorting = True
            quickSortGenerator = _quickSort(drawInfo, low, splitIndex, ascending)
            while quickSorting:
                try:
                    yield True
                    next(quickSortGenerator)
                except StopIteration:
                    quickSorting = False

            quickSorting = True
            quickSortGenerator = _quickSort(drawInfo, splitIndex + 1, high, ascending)
            while quickSorting:
                try:
                    yield True
                    next(quickSortGenerator)
                except StopIteration:
                    quickSorting = False

    quickSorting = True
    quickSortGenerator = _quickSort(drawInfo, 0, len(drawInfo.list) - 1, ascending)

    while quickSorting:
        try:
            yield True
            next(quickSortGenerator)
        except StopIteration:
            quickSorting = False


def mergeSort(drawInfo, ascending=True):
    width = 1
    list = drawInfo.list
    listSize = len(list)

    while width < listSize:
        l = 0
        while l < listSize:
            r = min(l + (width * 2 - 1), listSize - 1)
            m = min(l + width - 1, listSize - 1)

            merging = True
            mergeGenerator = merge(list, l, m, r, drawInfo, ascending)
            while merging:
                try:
                    yield True
                    next(mergeGenerator)
                except StopIteration:
                    merging = False

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
        yield True
        k += 1

    while i < n1:
        a[k] = L[i]
        drawList(drawInfo, {k: drawInfo.green}, True)
        yield True
        i += 1
        k += 1

    while j < n2:
        a[k] = R[j]
        yield True
        j += 1
        k += 1


def heapify(list, listSize, i, drawInfo, ascending=True):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < listSize and (
        (list[largest] < list[left] and ascending)
        or (list[largest] > list[left] and not ascending)
    ):
        largest = left

    if right < listSize and (
        (list[largest] < list[right] and ascending)
        or (list[largest] > list[right] and not ascending)
    ):
        largest = right

    if largest != i:
        list[i], list[largest] = list[largest], list[i]
        drawList(drawInfo, {i: drawInfo.green, largest: drawInfo.red}, True)
        yield True

        heapifying = True
        heapifyGenerator = heapify(list, listSize, largest, drawInfo, ascending)

        while heapifying:
            try:
                yield True
                next(heapifyGenerator)
            except StopIteration:
                heapifying = False


def heapSort(drawInfo, ascending=True):
    list = drawInfo.list
    listSize = len(list)

    for i in range(listSize // 2 - 1, -1, -1):
        heapifying = True
        heapifyGenerator = heapify(list, listSize, i, drawInfo, ascending)

        while heapifying:
            try:
                yield True
                next(heapifyGenerator)
            except StopIteration:
                heapifying = False

    for i in range(listSize - 1, 0, -1):
        list[i], list[0] = list[0], list[i]

        drawList(drawInfo, {i: drawInfo.green, 0: drawInfo.red}, True)
        yield True

        heapifying = True
        heapifyGenerator = heapify(list, i, 0, drawInfo, ascending)

        while heapifying:
            try:
                yield True
                next(heapifyGenerator)
            except StopIteration:
                heapifying = False


def main():
    run = True
    clock = pygame.time.Clock()
    clockTime = 60

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
        clock.tick(clockTime)

        if sorting:
            try:
                next(sortingAlgorithmGenerator)
            except StopIteration:
                sorting = False
        else:
            draw(drawInfo, sortingAlgorithmName, ascending, clockTime)

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

            elif event.key == pygame.K_UP:
                if clockTime < 240:
                    clockTime += 30
                draw(drawInfo, sortingAlgorithmName, ascending, clockTime)

            elif event.key == pygame.K_DOWN:
                if clockTime > 30:
                    clockTime -= 30
                draw(drawInfo, sortingAlgorithmName, ascending, clockTime)

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

            elif event.key == pygame.K_h and not sorting:
                sortingAlgorithm = heapSort
                sortingAlgorithmName = "Heap Sort"

    pygame.quit()


if __name__ == "__main__":
    main()
