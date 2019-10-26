import functools


@functools.total_ordering
class ScoreLine:
    def __init__(self, line=''):
        self.name = line.split('|')[1].strip()
        self.score = int(line.split('|')[2].strip())

    def get_line(self, position):
        return '{place:>5}|{nick:<16}|{score:>8}'.format(place=position,
                                                         nick=self.name,
                                                         score=self.score)

    def __eq__(self, other):
        return self.score == other.score

    def __lt__(self, other):
        return self.score < other.score


class Scores:
    def __init__(self, file):
        self.lines = [ScoreLine(line=i) for i in [j for j in file][5:]]

    def add_line(self, line):
        self.lines.append(ScoreLine(line))
        self.lines.sort(reverse=True)

    def write_to_file(self, file):
        file.write('===============================\n'
                   '==========Top Players==========\n'
                   '===============================\n'
                   'Place|    Nickname    |   Score\n'
                   '-------------------------------\n')
        place = 0
        for line in self.lines:
            place += 1
            file.write(line.get_line(place) + '\n')
