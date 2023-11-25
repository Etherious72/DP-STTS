import sys
import math
from datetime import datetime, timedelta
from parameters import Parameter
from TransPorto import CutTrajectories
sys.setrecursionlimit(6000)


class Point(object):
    class Struct(object):
        def __init__(self, x, y, time, cellIndex, timeIndex, next):
            self.x = x
            self.y = y
            self.time = time
            self.cellIndex = cellIndex
            self.timeIndex = timeIndex
            self.next = next


def row(i):
    return int(i / para.cellW)


def col(i):
    return int(i - row(i) * para.cellH)


def read_tra(str):
    """
    :param input_path:
    :return:
    """
    data = []
    coordinates = list(map(lambda s: tuple(s.split(',')),
                           filter(lambda l: len(l) > 1, str.split(';'))))
    data.append(coordinates)
    return data


def CellIndex1(longitude, latitude):
    """
    get cell index
    :param longitude:
    :param latitude:
    :return:
    """
    incre = 0.0005
    longitude = float(longitude)
    latitude = float(latitude)
    height = float((para.top - para.bottom) / para.cellH)
    width = float((para.right - para.left) / para.cellW)
    rowIndex = int(math.floor((latitude - para.bottom) / height))
    columnIndex = int(math.floor((longitude - para.left) / width))
    rowIndex1 = int(math.floor((latitude - para.bottom - incre) / height))
    columnIndex1 = int(math.floor((longitude - para.left - incre) / width))
    rowIndex2 = int(math.floor((latitude - para.bottom + incre) / height))
    columnIndex2 = int(math.floor((longitude - para.left + incre) / width))
    if math.fabs(rowIndex * height + para.bottom - latitude) < pow(10, -6):
        rowIndex -= 1
    if math.fabs(columnIndex * width + para.left - longitude) < pow(10, -6):
        columnIndex -= 1
    if rowIndex1 != rowIndex2:
        if rowIndex1 < 0:
            rowIndex = rowIndex2
            latitude += incre
        else:
            rowIndex = rowIndex1
            latitude -= incre
    if columnIndex1 != columnIndex2:
        if columnIndex1 < 0:
            columnIndex = columnIndex2
            longitude += incre
        else:
            columnIndex = columnIndex1
            longitude -= incre
    if rowIndex < 0:
        rowIndex = 0
    if columnIndex < 0:
        columnIndex = 0
    if rowIndex >= para.cellH:
        rowIndex = para.cellH - 1
    if columnIndex >= para.cellW:
        columnIndex = para.cellW - 1
    cellIndex = rowIndex * para.cellW + columnIndex
    if cellIndex >= para.cellH * para.cellW:
        print('something is wrong \n')
    return cellIndex, longitude, latitude


def CellIndex(longitude, latitude):
    """
    get cell index
    :param longitude:
    :param latitude:
    :return:
    """
    incre = 0.0005
    longitude = float(longitude)
    latitude = float(latitude)
    height = float((para.top - para.bottom) / para.cellH)
    width = float((para.right - para.left) / para.cellW)
    rowIndex = int(math.floor((latitude - para.bottom) / height))
    columnIndex = int(math.floor((longitude - para.left) / width))
    rowIndex1 = int(math.floor((latitude - para.bottom - incre) / height))
    columnIndex1 = int(math.floor((longitude - para.left - incre) / width))
    rowIndex2 = int(math.floor((latitude - para.bottom + incre) / height))
    columnIndex2 = int(math.floor((longitude - para.left + incre) / width))
    if math.fabs(rowIndex * height + para.bottom - latitude) < pow(10, -6):
        rowIndex -= 1
    if math.fabs(columnIndex * width + para.left - longitude) < pow(10, -6):
        columnIndex -= 1
    if rowIndex1 != rowIndex2:
        if rowIndex1 < 0:
            rowIndex = rowIndex2
            latitude += incre
        else:
            rowIndex = rowIndex1
            latitude -= incre
    if columnIndex1 != columnIndex2:
        if columnIndex1 < 0:
            columnIndex = columnIndex2
            longitude += incre
        else:
            columnIndex = columnIndex1
            longitude -= incre

    if rowIndex < 0:
        rowIndex = 0
    if columnIndex < 0:
        columnIndex = 0
    if rowIndex >= para.cellH:
        rowIndex = para.cellH - 1
    if columnIndex >= para.cellW:
        columnIndex = para.cellW - 1
    cellIndex = rowIndex * para.cellW + columnIndex
    if cellIndex >= para.cellH * para.cellW:
        print('something is wrong \n')
    return cellIndex


def TimeIndex(time):
    """
    :param time:
    :return: timeIndex
    """
    start = datetime.combine(time.date(), para.startTime.time())
    delta = (time - start).seconds / 60
    timeIndex = int(delta / para.timestep)
    if (time - (timedelta(minutes=(timeIndex * para.timestep)) + start)).seconds < pow(10, -5):
        timeIndex -= 1
    if timeIndex < 0:
        timeIndex = 0
    return timeIndex


def PointInsertion(preLoc, head, tail):
    # incre = 0.0005
    if math.isclose(head.cellIndex, tail.cellIndex, rel_tol=pow(10, -6)) and \
            math.isclose(head.timeIndex, tail.timeIndex, rel_tol=pow(10, -6)):
        return
    else:

        headr = int(head.cellIndex / para.cellW)
        headc = int(head.cellIndex - headr * para.cellH)
        tailr = int(tail.cellIndex / para.cellH)
        tailc = int(tail.cellIndex - tailr * para.cellH)
        delta_T = (tail.time - head.time).seconds
        # Determine if the cell is adjacent or if the time period meets the requirements
        if math.fabs(headr - tailr) <= 1 and math.fabs(headc - tailc) <= 1 and \
                math.fabs(head.timeIndex - tail.timeIndex) <= para.numstep:
            return
        else:
            mid = Point()
            midx = (head.x + tail.x) / 2
            midy = (head.y + tail.y) / 2
            midt = head.time + timedelta(seconds=int(delta_T / 2))

            mid.cellIndex, midx, midy = CellIndex1(midx, midy)
            timeIndex = TimeIndex(midt)

            mid.x = midx
            mid.y = midy
            mid.time = midt
            mid.timeIndex = timeIndex

            # print(mid.x, mid.y, mid.time, mid.cellIndex, mid.timeIndex)
            mid.next = tail
            head.next = mid

            PointInsertion(preLoc, head, mid)
            PointInsertion(preLoc, mid, tail)
    return


def removeDup(head):
    """
    Removal of adjacent duplicate elements

    :param head:
    :return:
    """
    if head is None or head.next is None:
        return head
    p = head
    while p.next:
        if (p.cellIndex == p.next.cellIndex) and (p.timeIndex == p.next.timeIndex):
            p.next = p.next.next
        else:
            p = p.next
    return head


def getNeighbor(cellCount):
    """
    Get the adjacent cellIndex of each current cell
    :param cellCount: parameter
    :return:
    """
    outpath = open('data/parameters/neighborFile_' + str(cellCount) + '.txt', 'w')
    for i in range(0, para.cellCount):
        count = 0
        flag = 0
        rowi = row(i)
        coli = col(i)
        for j in range(0, para.cellCount):
            rowj = row(j)
            colj = col(j)
            if abs(rowi - rowj) <= 1 and abs(coli - colj) <= 1:
                count += 1
                if count <= 8:
                    print("%d" % j, end='', file=outpath)
                    print(' ', end='', file=outpath)
                if count == 9:
                    print("%d" % j, end='', file=outpath)
                    print('', file=outpath)
                    flag = 1
        if flag == 0:
            while count < 9:
                print("-1", end='', file=outpath)
                print(' ', end='', file=outpath)
                count += 1
            print('', file=outpath)
    outpath.close()


def interpolation(dataset):
    """

    :param dataset:
    :return:
    """

    print('start time: %s ' % para.startTime)
    print('end time: %s ' % para.endTime)
    print('timeInterval: ' + str(para.timestep) + ' min')

    input_path = './data/output/TestData.txt'

    ori_out = open('./data/output/' + dataset + '_out.txt', 'w')
    with open(input_path) as input:
        content = input.readlines()

    line_number = 0
    number = 0
    i = 0

    while i < len(content):
        line_number = line_number + 1
        if (line_number % 2) == 0:
            s = content[i][3:]
            ori_data = read_tra(s)
            # number = number + 1
            if number % 5000 == 0:
                print('----------------NO: %d ---------------' % (number))
            flag = 0
            count = 0
            for j in range(len(ori_data[0])):
                x2 = float(ori_data[0][j][0])
                y2 = float(ori_data[0][j][1])
                t2 = datetime.strptime(ori_data[0][j][2], "%Y-%m-%d %H:%M:%S")
                count += 1
                if count == 1:
                    x1 = x2
                    y1 = y2
                    t1 = t2
                head = Point()
                preLoc = Point()
                tail = Point()
                head.x = x1
                head.y = y1
                head.time = t1
                if (x1 <= para.right) and (x1 >= para.left) and (y1 <= para.top) and (y1 >= para.bottom):
                    head.cellIndex = CellIndex(x1, y1)
                else:
                    head.cellIndex = -1
                s_time = datetime.combine(t1.date(), para.startTime.time())
                e_time = datetime.combine(t1.date(), para.endTime.time())
                if e_time >= t1 >= s_time:
                    head.timeIndex = TimeIndex(t1)
                else:
                    head.timeIndex = -1

                preLoc.cellIndex = head.cellIndex
                preLoc.timeIndex = head.timeIndex
                tail.x = x2
                tail.y = y2
                tail.time = t2
                if (x2 <= para.right) and (x2 >= para.left) and (y2 <= para.top) and (y2 >= para.bottom):
                    tail.cellIndex = CellIndex(x2, y2)
                else:
                    tail.cellIndex = -1
                s_time = datetime.combine(t2.date(), para.startTime.time())
                e_time = datetime.combine(t2.date(), para.endTime.time())
                if e_time >= t2 >= s_time:
                    tail.timeIndex = TimeIndex(t2)
                else:
                    tail.timeIndex = -1

                if tail.cellIndex == -1 or tail.timeIndex == -1:
                    continue

                tail.next = None
                head.next = tail
                PointInsertion(preLoc, head, tail)

                p = head
                while p:
                    if p.cellIndex != -1 and p.timeIndex != -1:
                        if flag == 0:
                            if number != 0:
                                print('', file=ori_out)
                            print('#%d:' % number, file=ori_out)
                            print('>0:', end='', file=ori_out)
                            flag = 1
                            number += 1
                        print("%.8f,%.8f,%s;" % (p.x, p.y, p.time), end='', file=ori_out)
                    p = p.next
                x1 = x2
                y1 = y2
                t1 = t2
        i += 1
    ori_out.close()


def middle(dataset):
    """
    :return:
    """
    # 数据集的名称

    input_path = './data/output/' + dataset + '_out.txt'

    out_mid_path = open('./data/output/' + 'middleFile.txt', 'w')
    out_len_path = open('./data/output/' + 'traLenFile.txt', 'w')

    with open(input_path) as input:
        content = input.readlines()

    line_number = 0
    i = 0
    number = 0
    while i < len(content):
        line_number = line_number + 1
        if (line_number % 2) == 0:
            s = content[i][3:]
            data = read_tra(s)

            head = Point()
            head.next = None
            tail = head
            if number % 50000 == 0:
                print('--------------------NO: %d --------------------' % number)
            print('#%d:' % number, file=out_mid_path)
            print('>0:', end='', file=out_mid_path)
            # print(data[0])
            for j in range(len(data[0])):
                # this = head.next
                this = Point()
                this.x = data[0][j][0]
                this.y = data[0][j][1]
                this.time = datetime.strptime(data[0][j][2], "%Y-%m-%d %H:%M:%S")
                d = this.time.date()
                this.cellIndex = CellIndex(this.x, this.y)
                this.timeIndex = TimeIndex(this.time)
                tail.next = this
                tail = this
            tail.next = None
            removeDup(head.next)
            p = head.next
            count = 0
            while p:
                count += 1
                print('%d,%d;' % (p.cellIndex, p.timeIndex), end='', file=out_mid_path)
                p = p.next
            print('%d' % count, file=out_len_path)
            print('', file=out_mid_path)
            number += 1
        i += 1

    out_mid_path.close()
    out_len_path.close()


def PreProcess(dataset):
    # para = Parameter()
    para.show()
    # Trans Porto
    CutTrajectories()
    # get neighborFile
    print('------------------neighbor start---------------------')
    getNeighbor(para.cellW)
    print('------------------neighbor over ---------------------')
    # get interpolationFile
    print('------------------interpolation start---------------------')
    interpolation(dataset)
    print('------------------interpolation over ---------------------')
    # get middleFile
    print('------------------middle start---------------------')
    middle(dataset)
    print('------------------middle over ---------------------')


para = Parameter()
