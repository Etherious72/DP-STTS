import re


def removeTime(dataset, epsilon, cellH, numtimeInterval, h, times):
    output = open(
        './data/output/' + dataset + '_' + cellH + '_' + numtimeInterval + 'maxLevel' + h + '_totalBudget_Location'
        + str(epsilon) + '_' + times + '.txt', 'w')
    with open('./data/output/' + dataset + '_' + cellH + '_' + numtimeInterval + '_maxLevel' + h + '_totalBudget'
              + str(epsilon) + '_' + times + '.txt') as input:
        content = input.readlines()
    line = '\\,[0-9]{4}\\-[0-9]{2}\\-[0-9]{2}\\s[0-9]+\\:[0-9]{2}\\:[0-9]{2}'
    for s in content:
        num = re.sub(line, "", s, count=0, flags=0)
        output.write(num)
    output.close()


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
