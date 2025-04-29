import math
import random
import time
from parameters import Parameter
from Processing import PreProcess
from trans import trans
from removeTime import removeTime


class Node(object):
    def __init__(self, cellIndexS, timeIndexS, count=0.0, nCount=0.0, level=0, eCount=0.0):
        self.cellIndexS = cellIndexS
        self.timeIndexS = timeIndexS
        self.count = count
        self.nCount = nCount
        self.eCount = eCount
        self.level = level
        self.next = None

    def show(self):
        print('Node parameters：')
        print(self.cellIndexS)
        print(self.timeIndexS)
        print(self.level)


class LinkList(object):
    class LinkListIterator(object):
        def __init__(self, node):
            self.node = node

        def __next__(self):
            if self.node:
                cur_node = self.node
                self.node = cur_node.next
                return cur_node.cellIndexS, cur_node.timeIndexS
            else:
                raise StopIteration

        def __iter__(self):
            return self

    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, node):
        """

        :param node:
        :return:
        """
        # s = LinkList.Node(obj)
        if not self.head:  # head is NULL
            self.head = node
            self.tail = node
        else:  # Not for empty, head insert
            node.next = self.head.next
            self.head.next = node

    def findNode(self, node):
        n = self.head
        while n:
            if (n.level == node.level):
                flag = 0
                for i in range(node.level + 1):
                    if ((n.cellIndexS[i] != node.cellIndexS[i]) or (n.timeIndexS[i] != node.timeIndexS[i])):
                        flag = 1
                        break
                if flag == 0:
                    return n
            n = n.next
        return None

    def __iter__(self):
        return self.LinkListIterator(self.head)

    def __repr__(self):
        return '<<' + ','.join(map(str, self)) + '>>'


class HashTableS(object):
    def __init__(self, size):
        self.size = size
        # List T, each position of T holds a linked table, create a linked table object with LinkList
        self.T = [LinkList() for i in range(self.size)]

    def getHashValue(self, node):
        s = ''
        for i in range(node.level + 1):
            if i is not None:
                s = s + str(node.cellIndexS[i])
        for j in range(node.level + 1):
            if j is not None:
                s = s + str(node.timeIndexS[j])
        index = self.sfold(s)
        return index

    def sfold(self, key):
        intlength = int(len(key) / 4)
        sum = 0
        bin_array = []
        for i in range(0, intlength):
            s = ''
            for j in range(int(i * 4), int(i * 4 + 4)):
                s = '{0:08b}'.format(ord(key[j])) + s
            bin_array.append(s)
        extra = len(key) - intlength * 4
        if extra != 0:
            s = ''
            for i in range(extra):
                s = '{0:08b}'.format(ord(key[intlength * 4 + i])) + s
            bin_array.append(s)
        for i in range(len(bin_array)):
            sum += int(bin_array[i], 2)
        return sum % int(pow(2, hashLen))
        # return sum % int(10)

    def insertNode(self, node):
        hashValue = self.getHashValue(node)
        if self.find(node):
            print('The current incoming node: ')
            print(node.cellIndexS)
            print(node.timeIndexS)
            print('something is wrong: Duplicated Insert')
        else:
            self.T[hashValue].append(node)

    def find(self, node):
        hashValue = self.getHashValue(node)
        n = self.T[hashValue].findNode(node)
        if n is not None:
            return True
        else:
            return False

    def updateCount(self, node, increment):
        hashValue = self.getHashValue(node)
        temp = self.T[hashValue].findNode(node)
        if temp is None:
            print('something is wrong: cannot find the node')
            print('cellIndex ', node.cellIndexS)
            print('timeIndex ', node.timeIndexS)
            print('level ', node.level)
            a = input('a')
            return False
        temp.count += increment
        return True

    def setNoiseCount(self, node, noiseCount):
        hashValue = self.getHashValue(node)
        temp = self.T[hashValue].findNode(node)
        if temp is None:
            print('something is wrong: cannot find the node')
            for j in range(0, node.level + 1):
                print(node.cellIndexS[j], end=" ")
                print(' ', end=" ")
                print(node.timeIndexS[j], end=" ")
                print(';', end=" ")
            st = input("enter a string to stop")
            print(st)
            return False

        temp.nCount = hashArray.getCount(temp) + float(noiseCount)
        if (temp.nCount < 0):
            temp.nCount = 0
        return True

    def getNoiseCount(self, node):
        hashValue = self.getHashValue(node)
        temp = self.T[hashValue].findNode(node)
        if temp is None:
            print('something is wrong: cannot find the node')
            return -1
        return temp.nCount

    def getCount(self, node):
        hashValue = self.getHashValue(node)
        temp = self.T[hashValue].findNode(node)
        if temp is None:
            print('something is wrong: cannot find the node')
            return -1
        return temp.count

    def setENoiseCount(self, node, noiseCount=0.0):
        hashValue = self.getHashValue(node)
        temp = self.T[hashValue].findNode(node)
        if temp is None:
            print('something is wrong: cannot find the node')
            return False
        if noiseCount < 0:
            noiseCount = 0
        temp.eCount = float(noiseCount)
        return True

    def getENoiseCount(self, node):
        hashValue = self.getHashValue(node)
        temp = self.T[hashValue].findNode(node)
        if temp is None:
            print('something is wrong: cannot find the node')
            return -1
        return temp.eCount


def createNode(array, timeArray, count=0.0, nCount=0.0, level=0, eCount=0.0):
    temp_A = []
    temp_T = []
    for i in range(len(array)):
        temp_A.append(array[i])
    for j in range(len(timeArray)):
        temp_T.append(timeArray[j])
    temp = Node(temp_A, temp_T, count, nCount, level, eCount)
    return temp


def startPoint():
    global count
    array = ['' for i in range(para.maxLevel + 2)]
    timeArray = ['' for i in range(para.maxLevel + 2)]
    for i in range(0, para.cellCount):
        for j in range(0, para.numtimeInterval):
            level = 0
            array[level] = para.startSign
            timeArray[level] = para.startSign
            level += 1
            array[level] = i
            timeArray[level] = j
            node = createNode(array, timeArray, 0.0, 0.0, level, 0.0)
            hashArray.insertNode(node)
            count += 1
            if count % 100000 == 0:
                print("The node count: " + str(count))


def read_tra(str):
    """

    :param str:
    :return:
    """
    data = []
    coordinates = list(map(lambda s: tuple(s.split(',')),
                           filter(lambda l: len(l) > 1, str.split(';'))))
    data.append(coordinates)
    return data


def loadDataStartPoint():
    lineIndex = 0
    path = './data/output/middleFile.txt'
    with open(path) as input:
        content = input.readlines()

    line_number = 0
    i = 0
    while i < len(content):
        line_number = line_number + 1
        if (line_number % 2) == 0:
            s = content[i][3:]
            tra = read_tra(s)
            lineIndex = lineIndex + 1
            level = 0
            temp_a = ['' for i in range(para.maxLevel + 2)]
            temp_t = ['' for i in range(para.maxLevel + 2)]
            array = temp_a
            timeArray = temp_t
            end = (para.endSign, para.endSign)
            tra[0].append(end)

            tLen = len(tra[0])

            array[level] = para.startSign
            timeArray[level] = para.startSign
            level += 1
            number = 0
            while (level <= para.maxLevel) and (level <= tLen):
                array[level] = int(tra[0][number][0])
                timeArray[level] = int(tra[0][number][1])
                node = createNode(array, timeArray, 0, 0, level)
                hashArray.updateCount(node, 1.0)
                level += 1
                number += 1
        i += 1
    return


def getNoise(epsilon, level, sensitivity):
    noise = LapLaceNoise(epsilon / level, sensitivity)
    return noise


def addNoiseStartPoint():
    array = ['' for i in range(para.maxLevel + 2)]
    timeArray = ['' for i in range(para.maxLevel + 2)]
    for i in range(0, para.cellCount):
        for j in range(0, para.numtimeInterval):
            level = 0
            array[level] = para.startSign
            timeArray[level] = para.startSign
            level += 1
            array[level] = i
            timeArray[level] = j
            node = createNode(array, timeArray, 0, 0, level)
            noise = getNoise(para.epsilonPrefix, para.maxLevel, para.sensitivity)
            hashArray.setNoiseCount(node, noise)


def enforceConsistency():
    path = './data/output/middleFile.txt'
    with open(path) as input:
        content = input.readlines()
    line_number = 0
    i = 0
    sum = 0
    while i < len(content):
        line_number = line_number + 1
        if (line_number % 2) == 0:
            sum += 1  # the count of the trajectories
        i += 1
    array = ['' for i in range(para.maxLevel + 2)]
    timeArray = ['' for i in range(para.maxLevel + 2)]

    cSum = 0.0
    checkSum = 0.0
    # get the noise count of all the root's children
    for i in range(para.cellCount):
        for j in range(para.numtimeInterval):
            level = 0
            array[level] = para.startSign
            timeArray[level] = para.startSign
            level += 1
            array[level] = i
            timeArray[level] = j
            node = createNode(array, timeArray, 0.0, 0.0, level)
            cSum += hashArray.getNoiseCount(node)

    if math.isclose(cSum, 0.0, rel_tol=1e-5):
        return

        # regulate sum

    temp = [[0 for i in range(para.numtimeInterval)] for i in range(para.cellCount)]

    for i in range(0, para.cellCount):
        for j in range(0, para.numtimeInterval):
            level = 0
            array[level] = para.startSign
            timeArray[level] = para.startSign
            level += 1

            array[level] = i
            timeArray[level] = j
            node = createNode(array, timeArray, 0.0, 0.0, level)

            nCount = hashArray.getNoiseCount(node)
            eNCount = int(sum * nCount / cSum)
            checkSum = checkSum + eNCount
            temp[i][j] = nCount

    #   print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ check regulate', checkSum)
    tempSum = sum
    while checkSum <= sum:
        checkSum = 0
        tempSum = tempSum + 1
        for i in range(0, para.cellCount):
            for j in range(0, para.numtimeInterval):
                checkSum = checkSum + int(float(temp[i][j]) / cSum * tempSum)

    sumT = tempSum - 1
    # regulate sum

    checkSum = 0
    for i in range(0, para.cellCount):
        for j in range(0, para.numtimeInterval):
            level = 0
            array[level] = para.startSign
            timeArray[level] = para.startSign
            level += 1

            array[level] = i
            timeArray[level] = j
            node = createNode(array, timeArray, 0.0, 0.0, level)

            nCount = hashArray.getNoiseCount(node)
            eNCount = int(sumT * nCount / cSum)
            hashArray.setENoiseCount(node, eNCount)
            # print('eNCount ', eNCount)
            checkSum = checkSum + eNCount

    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ main - checkSum ', sum - checkSum)
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ sum ', sum)
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ checkSum ', checkSum)


def buildMarkov3():
    global count
    array = ['' for i in range(para.tmaxLevel + 2)]
    timeArray = ['' for i in range(para.tmaxLevel + 2)]
    for i in range(0, para.cellCount):
        for j in range(para.numtimeInterval):
            level = 0
            array[level] = para.aSign
            timeArray[level] = para.aSign

            level += 1
            array[level] = i
            timeArray[level] = j

            if level == para.tmaxLevel:
                node = createNode(array, timeArray, 0.0, 0.0, level, 0.0)
                hashArray.insertNode(node)
                count += 1
            else:
                generateLevelMarkov3(array, timeArray, level + 1)


def generateLevelMarkov3(array, timeArray, level):
    global count
    if level > para.tmaxLevel:
        return
    else:
        cellA = int(array[level - 1])
        timeA = int(timeArray[level - 1])
        for i in para.neighbor[cellA]:
            if i == -1:
                break
            if i == cellA:
                for j in range(1, para.numstep+1):
                    preTime = timeA + j
                    if preTime > para.numtimeInterval - 1:
                        continue
                    if not ((i == cellA) and (preTime == timeA)):
                        array[level] = i
                        timeArray[level] = preTime
                        if level == para.tmaxLevel:
                            node = createNode(array, timeArray, 0.0, 0.0, level)
                            hashArray.insertNode(node)
                            count += 1
                        else:
                            generateLevelMarkov3(array, timeArray, level + 1)
                        if count % 10000 == 0:
                            print("buildMarkov3 node count: " + str(count))
            elif i != cellA:
                for j in range(2):
                    preTime = timeA + j
                    if preTime > para.numtimeInterval - 1:
                        continue
                    if not ((i == cellA) and (preTime == timeA)):
                        array[level] = i
                        timeArray[level] = preTime
                        if level == para.tmaxLevel:
                            node = createNode(array, timeArray, 0.0, 0.0, level)
                            hashArray.insertNode(node)
                            count += 1
                        else:
                            generateLevelMarkov3(array, timeArray, level + 1)
                        if count % 10000 == 0:
                            print("buildMarkov3 node count: " + str(count))
        if level == para.tmaxLevel:
            array[level] = para.endSign
            timeArray[level] = para.endSign
            node = createNode(array, timeArray, 0.0, 0.0, level, 0.0)
            hashArray.insertNode(node)
            count += 1
        return


def loadData2Markov3():
    lineIndex = 0
    path = './data/output/middleFile.txt'
    with open(path) as input:
        content = input.readlines()
    line_number = 0
    number = 0
    i = 0
    while i < len(content):
        line_number = line_number + 1
        if (line_number % 2) == 0:
            s = content[i][3:]
            tra = read_tra(s)
            if len(tra[0]) < para.tmaxLevel:
                i += 1
                continue

            lineIndex += 1
            temp_a = ['' for i in range(para.tmaxLevel + 2)]
            temp_t = ['' for i in range(para.tmaxLevel + 2)]
            array = temp_a
            timeArray = temp_t
            end = (para.endSign, para.endSign)
            tra[0].append(end)

            tLen = len(tra[0])

            for j in range(0, tLen - para.tmaxLevel + 1):
                level = 0
                array[level] = para.aSign
                timeArray[level] = para.aSign
                level += 1
                low = j
                hight = low + para.tmaxLevel
                for k in range(j, hight):
                    pair = tra[0][k]
                    array[level] = int(pair[0])
                    timeArray[level] = int(pair[1])
                    level += 1
                node = createNode(array, timeArray, 0.0, 0.0, level - 1)
                hashArray.updateCount(node, 1.0 / (tLen - para.tmaxLevel + 1))
        i += 1


def addNoise2Markov3():
    array = ['' for i in range(para.tmaxLevel + 2)]
    timeArray = ['' for i in range(para.tmaxLevel + 2)]
    for i in range(0, para.cellCount):
        for j in range(para.numtimeInterval):
            level = 0
            array[level] = para.aSign
            timeArray[level] = para.aSign
            level += 1
            array[level] = i
            timeArray[level] = j

            if level == para.tmaxLevel:
                node = createNode(array, timeArray, 0, 0, level)
                noise = getNoiseMarkov(para.epsilon - para.epsilonPrefix, para.sensitivity)
                hashArray.setNoiseCount(node, noise)
            else:
                addNoise2Markov3Level(array, timeArray, level + 1)


def getNoiseMarkov(epsilon, sensitivity):
    noise = LapLaceNoise(epsilon, sensitivity)
    return noise


def addNoise2Markov3Level(array, timeArray, level):
    if level > para.tmaxLevel:
        return
    cellA = int(array[level - 1])
    timeA = int(timeArray[level - 1])
    for i in para.neighbor[cellA]:
        if i == -1:
            break
        if i == cellA:
            for j in range(1, para.numstep + 1):
                preTime = timeA + j
                if preTime > para.numtimeInterval - 1:
                    continue
                if not ((i == cellA) and (preTime == timeA)):
                    array[level] = i
                    timeArray[level] = preTime
                    if level == para.tmaxLevel:
                        node = createNode(array, timeArray, 0.0, 0.0, level)
                        noise = getNoiseMarkov(para.epsilon - para.epsilonPrefix, para.sensitivity)
                        hashArray.setNoiseCount(node, noise)
                    else:
                        addNoise2Markov3Level(array, timeArray, level + 1)
        elif i != cellA:
            for j in range(2):
                preTime = timeA + j
                if preTime > para.numtimeInterval - 1:
                    continue
                if not ((i == cellA) and (preTime == timeA)):
                    array[level] = i
                    timeArray[level] = preTime
                    if level == para.tmaxLevel:
                        node = createNode(array, timeArray, 0.0, 0.0, level)
                        noise = getNoiseMarkov(para.epsilon - para.epsilonPrefix, para.sensitivity)
                        hashArray.setNoiseCount(node, noise)
                    else:
                        addNoise2Markov3Level(array, timeArray, level + 1)
    if level == para.tmaxLevel:
        array[level] = para.endSign
        timeArray[level] = para.endSign
        node = createNode(array, timeArray, 0, 0, level)
        noise = getNoiseMarkov(para.epsilon - para.epsilonPrefix, para.sensitivity)
        hashArray.setNoiseCount(node, noise)
    return


def normalizeMarkov3():
    array = ['' for i in range(para.tmaxLevel + 2)]
    timeArray = ['' for i in range(para.tmaxLevel + 2)]
    if para.tmaxLevel <= 1:
        return
    else:
        for i in range(0, para.cellCount):
            for j in range(para.numtimeInterval):
                level = 0
                array[level] = para.aSign
                timeArray[level] = para.aSign
                level += 1
                array[level] = i
                timeArray[level] = j
                normalizeMarkovLevel3(array, timeArray, level + 1)


def normalizeMarkovLevel3(array, timeArray, level):
    if level > para.tmaxLevel:
        return
    cSum = 0
    sum = 1.0
    cellA = int(array[level - 1])
    timeA = int(timeArray[level - 1])
    for i in para.neighbor[cellA]:
        if i == -1:
            break
        if i == cellA:
            for j in range(1, para.numstep + 1):
                preTime = timeA + j
                if preTime > para.numtimeInterval - 1:
                    continue
                if not ((i == cellA) and (preTime == timeA)):
                    array[level] = i
                    timeArray[level] = preTime
                    normalizeMarkovLevel3(array, timeArray, level + 1)
                    if level == para.tmaxLevel:
                        node = createNode(array, timeArray, 0.0, 0.0, level)
                        nCount = hashArray.getNoiseCount(node)
                        cSum += nCount
        elif i != cellA:
            for j in range(2):
                preTime = timeA + j
                if preTime > para.numtimeInterval - 1:
                    continue
                if not ((i == cellA) and (preTime == timeA)):
                    array[level] = i
                    timeArray[level] = preTime
                    normalizeMarkovLevel3(array, timeArray, level + 1)
                    if level == para.tmaxLevel:
                        node = createNode(array, timeArray, 0.0, 0.0, level)
                        nCount = hashArray.getNoiseCount(node)
                        cSum += nCount
    if level == para.tmaxLevel:
        array[level] = para.endSign
        timeArray[level] = para.endSign
        node = createNode(array, timeArray, 0.0, 0.0, level)
        cSum += hashArray.getNoiseCount(node)

        #  changes: indent    here;  Markov noise
        if cSum > 0:
            cellA = array[level - 1]
            for i in para.neighbor[cellA]:

                if i == -1:
                    break
                if i == cellA:
                    for j in range(1, para.numstep + 1):
                        preTime = timeA + j
                        if preTime > para.numtimeInterval - 1:
                            break
                        if not ((i == cellA) and (preTime == timeA)):
                            array[level] = i
                            timeArray[level] = preTime
                            node = createNode(array, timeArray, 0.0, 0.0, level)
                            nCount = hashArray.getNoiseCount(node)
                            eNCount = sum * nCount / cSum
                            hashArray.setENoiseCount(node, eNCount)
                elif i != cellA:
                    for j in range(2):
                        preTime = timeA + j
                        if preTime > para.numtimeInterval - 1:
                            break
                        if not ((i == cellA) and (preTime == timeA)):
                            array[level] = i
                            timeArray[level] = preTime
                            node = createNode(array, timeArray, 0.0, 0.0, level)
                            nCount = hashArray.getNoiseCount(node)
                            eNCount = sum * nCount / cSum
                            hashArray.setENoiseCount(node, eNCount)
            array[level] = para.endSign
            timeArray[level] = para.endSign
            node = createNode(array, timeArray, 0.0, 0.0, level)

            nCount = hashArray.getNoiseCount(node)
            eNCount = sum * nCount / cSum
            hashArray.setENoiseCount(node, eNCount)
    return


def writeTrajecoryM4():
    array = ['' for i in range(para.maxTLen + 2)]
    timeArray = ['' for i in range(para.maxTLen + 2)]

    path = './data/output/middleFile.txt'
    with open(path) as input:
        content = input.readlines()
    sum = len(content)/2
    sumTemp = 0
    for i in range(0, para.cellCount):
        for j in range(0, para.numtimeInterval):
            level = 0
            array[level] = para.startSign
            timeArray[level] = para.startSign
            level += 1

            array[level] = i
            timeArray[level] = j
            node = createNode(array, timeArray, 0.0, 0.0, level)
            tCount = int(hashArray.getENoiseCount(node))
            sumTemp = sumTemp + tCount

            # print('tCount ', tCount)

            if tCount < 1:
                continue

            flag = 0
            writeTrajecoryLevelMarkov4(array, timeArray, level + 1, level, tCount, flag, j)
    print('sum - sumTemp main ', sum - sumTemp)
    print('sum ', sum)
    print('sumTemp main ', sumTemp)


def writeTrajecoryLevelMarkov4(array, timeArray, level, curlen, cCount, flag, pre):
    if cCount < 1:
        return

    if (array[level - 1] == para.endSign) or (curlen == para.maxTLen):
        write2File(array, timeArray, cCount, curlen)
        array[level - 1] = ''
        timeArray[level - 1] = ''
        return
    # 前maxlevel个点
    if level <= para.maxLevel:
        sumTemp = 0
        cellA = int(array[level - 1])
        timeA = int(timeArray[level - 1])
        for i in para.neighbor[cellA]:
            if i == -1:
                break
            for j in (timeA, timeA + 1):
                if j > para.numtimeInterval - 1:
                    continue
                if not ((i == cellA) and (j == timeA)):
                    if level >= len(array):
                        print('----')
                    array[level] = i
                    timeArray[level] = j
                    node = createNode(array, timeArray, 0.0, 0.0, level)
                    tCount = int(hashArray.getENoiseCount(node))
                    sumTemp += tCount
                    writeTrajecoryLevelMarkov4(array, timeArray, level + 1, level, tCount, flag)

        array[level] = para.endSign
        timeArray[level] = para.endSign
        node = createNode(array, timeArray, 0.0, 0.0, level)
        tCount = int(cCount - sumTemp)
        writeTrajecoryLevelMarkov4(array, timeArray, level + 1, level, tCount, flag)
        sumTemp += tCount
    #    print('sum - sumTemp ', cCount - sumTemp)

    # 开始预测之后的点
    else:
        sumTemp2 = 0
        tempArray = ['' for i in range(para.tmaxLevel + 2)]
        tempTimeArray = ['' for i in range(para.tmaxLevel + 2)]
        tempArray[0] = para.aSign
        tempTimeArray[0] = para.aSign

        temp = curlen - para.tmaxLevel + 2
        for i in range(1, para.tmaxLevel):
            tempArray[i] = array[temp]
            tempTimeArray[i] = timeArray[temp]
            temp += 1
        cellA = array[level - 1]
        timeA = timeArray[level - 1]

        ncCount = getNewCountMarkov4(tempArray[:], tempTimeArray[:], cCount, cellA, timeA)
        for i in para.neighbor[cellA]:
            if i == -1:
                break
            if i == cellA:
                for j in range(1, para.numstep+1):

                    preTime = timeA + j

                    if preTime > para.numtimeInterval - 1:
                        continue
                    if not ((i == cellA) and (preTime == timeA)):
                        array[level] = i
                        timeArray[level] = preTime
                        tempArray[para.tmaxLevel] = i
                        tempTimeArray[para.tmaxLevel] = preTime
                        node = createNode(tempArray, tempTimeArray, 0.0, 0.0, para.tmaxLevel)
                        tCount = int(hashArray.getENoiseCount(node) * ncCount)
                        sumTemp2 += tCount
                        #        if  tCount > 0:
                        #            print('level ', level - 1, ' i j ', i, j, ' tCount ', tCount)
                        writeTrajecoryLevelMarkov4(array, timeArray, level + 1, level, tCount, flag, pre)
            elif i != cellA:
                for preTime in (timeA, timeA+1):
                    # preTime = timeA + 1

                    if preTime > para.numtimeInterval - 1:
                        continue

                    array[level] = i
                    timeArray[level] = preTime
                    tempArray[para.tmaxLevel] = i
                    tempTimeArray[para.tmaxLevel] = preTime
                    node = createNode(tempArray, tempTimeArray, 0.0, 0.0, para.tmaxLevel)
                    tCount = int(hashArray.getENoiseCount(node) * ncCount)
                    sumTemp2 += tCount
                    #        if  tCount > 0:
                    #            print('level ', level - 1, ' i j ', i, j, ' tCount ', tCount)
                    writeTrajecoryLevelMarkov4(array, timeArray, level + 1, level, tCount, flag, pre)
        array[level] = para.endSign
        timeArray[level] = para.endSign
        tempArray[para.tmaxLevel] = para.endSign
        tempTimeArray[para.tmaxLevel] = para.endSign
        node = createNode(tempArray, tempTimeArray, 0.0, 0.0, para.tmaxLevel)
        tCount = int(cCount - sumTemp2)
        #    if tCount > 0:
        #       print('level ', level - 1, ' #', ' tCount ', tCount)
        writeTrajecoryLevelMarkov4(array, timeArray, level + 1, level, tCount, flag, pre)
        sumTemp2 += tCount
        #    print('cCount - sumTemp2 ', end='')
        #   print(cCount - sumTemp2)
        return


def write2File(array, timeArray, tCount, curlen):
    global number_Tra
    tC = int(tCount)
    # if tC > 0:
    #     print(tC)
    for i in range(0, tC):

        print('#%d:' % number_Tra, file=write)
        number_Tra += 1
        print('>0:', end='', file=write)
        for j in range(curlen):
            print('%d,%d;' % (int(array[j]), int(timeArray[j])), end='', file=write)
        if curlen == 2:
            print('%d,%d;' % (int(array[1]), int(timeArray[1])), end='', file=write)
        print('', file=write)
    return


def getNewCountMarkov4(tempArray, tempTimeArray, cCount, cellA, timeA):
    newCCount = int(cCount) - 1
    sumTemp2 = 0
    tTemp = 1.0

    #   print('cCount ', cCount)
    while sumTemp2 <= cCount:
        if tTemp > 0:
            tTemp = 0
            newCCount = newCCount + 1
            sumTemp2 = 0
            for i in para.neighbor[cellA]:
                if i == -1:
                    break
                if i == cellA:
                    for j in range(1, para.numstep+1):
                        preTime = timeA + j
                        if preTime > para.numtimeInterval - 1:
                            continue
                        if not ((i == cellA) and (preTime == timeA)):
                            tempArray[para.tmaxLevel] = i
                            tempTimeArray[para.tmaxLevel] = preTime
                            node = createNode(tempArray, tempTimeArray, 0.0, 0.0, para.tmaxLevel)
                            sumTemp2 = sumTemp2 + int(hashArray.getENoiseCount(node) * newCCount)
                            tTemp += hashArray.getENoiseCount(node)
                elif i != cellA:
                    for j in range(2):
                        preTime = timeA + j
                        if preTime > para.numtimeInterval - 1:
                            continue
                        if not ((i == cellA) and (preTime == timeA)):
                            tempArray[para.tmaxLevel] = i
                            tempTimeArray[para.tmaxLevel] = preTime
                            node = createNode(tempArray, tempTimeArray, 0.0, 0.0, para.tmaxLevel)
                            sumTemp2 = sumTemp2 + int(hashArray.getENoiseCount(node) * newCCount)
                            tTemp += hashArray.getENoiseCount(node)

            tempArray[para.tmaxLevel] = para.endSign
            tempTimeArray[para.tmaxLevel] = para.endSign
            node = createNode(tempArray, tempTimeArray, 0.0, 0.0, para.tmaxLevel)
            sumTemp2 = sumTemp2 + int(hashArray.getENoiseCount(node) * newCCount)
            tTemp += hashArray.getENoiseCount(node)
        else:
            newCCount = cCount + 1
            break

        if newCCount > cCount + 100:
            newCCount = cCount + 1
            print('####################### tempArray ', tempArray)
            print('####################### tempTimeArray ', tempTimeArray)
            break
    return newCCount - 1


def LapLaceNoise(epsilon, sensitivity):
    d = random.random()
    uniform = d - 0.5
    s = sensitivity
    nc = -s / epsilon * sign(uniform) * math.log(1.0 - 2.0 * math.fabs(uniform))
    return nc


def sign(t):
    if t < 0:
        return -1.0
    else:
        return 1.0


def methodNew():
    """
    Average distribution
    :return:
    """
    startPoint()
    print('--------------------- buile startPoint over ---------------------')
    loadDataStartPoint()
    print('--------------------- Load over ---------------------')
    addNoiseStartPoint()

    print('--------------------- add noise over ---------------------')
    enforceConsistency()
    print('--------------------- enforceConsistency over ---------------------')

    buildMarkov3()
    print('--------------------- buileMarkov3 over ---------------------')
    loadData2Markov3()
    print('--------------------- loadData2Markov3 over ---------------------')
    addNoise2Markov3()
    print('--------------------- addNoise2Markov3 over ---------------------')
    normalizeMarkov3()
    print('--------------------- normalizeMarkov3 over ---------------------')
    writeTrajecoryM4()


if __name__ == '__main__':
    """
    Steps：
    1.Modify the parameters in the '. /data/parameters/' , 'parameters.py',
      boundary：range of trajectory space
      cellSize：grid division
      time：range of trajectory time
      timeStep：The duration of the interval(minutes)
      
      
    2.The '. /data/raw_data/' folder is to store the data source files to be processed
      Original.txt
      
    3.To process the data, run the PreProcess() function, passing in the following parameters:
      dataset = 'name'
      eps: overall privacy budget
      times: cycle number
    """
    print('Start')
    dataset = 'Porto'
    PreProcess(dataset)
    for eps in [1.0, 0.5]:
        times = 1
        while times != 2:  # Running times

            print('Start of the ' + str(times) + 'th run')
            para = Parameter()
            para.epsilon = eps
            para.epsilonPrefix = (1 / 2) * para.epsilon

            para.show()

            hashLen = 20
            l = pow(2, hashLen)
            hashArray = HashTableS(l)
            number_Tra = 0
            count = 0
            s = 0

            n = 0
            random.seed(time.time())

            write = open('data/output/writeTra-our.txt', 'w')
            # method
            methodNew()
            write.close()

            print('--------------------- writeTra over ---------------------')
            print('trans')
            trans(dataset, str(para.epsilon), str(para.cellH), str(para.numtimeInterval),
                  str(para.maxLevel), str(times))
            print('remove time')
            removeTime(dataset, str(para.epsilon), str(para.cellH), str(para.numtimeInterval),
                       str(para.maxLevel), str(times))
            times += 1

