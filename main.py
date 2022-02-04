import random


class MatrixError(Exception):
    pass


class Matrix(object):

    def __init__(self, m, n, init=True):
        if init:
            self.rows = [[0] * n for x in range(m)]
        else:
            self.rows = []
        self.m = m
        self.n = n

    def __getitem__(self, idx):
        return self.rows[idx]

    def __setitem__(self, idx, item):
        self.rows[idx] = item

    def __str__(self):
        s = '\n'.join([' '.join([str(item) for item in row]) for row in self.rows])
        return s + '\n'

    def __repr__(self):
        s = str(self.rows)
        rank = str(self.getRank())
        rep = "Матрица: \"%s\", размерность: \"%s\"" % (s, rank)
        return rep

    def reset(self):
        """ сбросить данные матрицы """
        self.rows = [[] for x in range(self.m)]

    def transpose(self):
        """ Транспонирование матрицы  """

        m, n = self.n, self.m
        mat = Matrix(m, n)
        mat.rows = [list(item) for item in zip(*self.rows)]

        return mat

    def get_rank(self):
        """ Возвращает размерность матрицы """
        return self.m, self.n

    def __eq__(self, mat):
        return mat.rows == self.rows

    def __add__(self, mat):
        """ Сложение матриц """

        if self.get_rank() != mat.get_rank():
            raise MatrixError("Размеры матриц не совпадают!")

        ret = Matrix(self.m, self.n)

        for x in range(self.m):
            row = [sum(item) for item in zip(self.rows[x], mat[x])]
            ret[x] = row

        return ret

    def __sub__(self, mat):
        """ Вычитание матрицы """

        if self.get_rank() != mat.get_rank():
            raise MatrixError("Нельзя вычесть матрицы разных размерностей")

        ret = Matrix(self.m, self.n)

        for x in range(self.m):
            row = [item[0] - item[1] for item in zip(self.rows[x], mat[x])]
            ret[x] = row

        return ret

    def __mul__(self, mat):
        """ Умножение матрицы, возвращает новую матрицу"""

        matm, matn = mat.get_rank()

        if self.n != matm:
            raise MatrixError("Нельзя умножить матрицы!")

        mat_t = mat.transpose()
        multmat = Matrix(self.m, matn)

        for x in range(self.m):
            for y in range(mat_t.m):
                multmat[x][y] = sum([item[0] * item[1] for item in zip(self.rows[x], mat_t[y])])

        return multmat

    def save(self, filename):
        """Сохранить матрицу в файл """
        open(filename, 'w').write(str(self))

    @classmethod
    def _make_matrix(cls, rows):
        """Создание  матрицы """
        m = len(rows)
        n = len(rows[0])
        # Validity check
        if any([len(row) != n for row in rows[1:]]):
            raise MatrixError("строки не равны")
        mat = Matrix(m, n, init=False)
        mat.rows = rows

        return mat

    @classmethod
    def make_random(cls, m, n, low=0, high=10):
        """Создание рандомной матрицы """

        obj = Matrix(m, n, init=False)
        for x in range(m):
            obj.rows.append([random.randrange(low, high) for i in range(obj.n)])

        return obj

    @classmethod
    def make_zero(cls, m, n):
        """ Создать нулевую матрицу """

        rows = [[0] * n for x in range(m)]
        return cls.from_list(rows)

    @classmethod
    def read_grid(cls, fname):
        """ Прочитать матрицу из файла """

        rows = []
        for line in open(fname).readlines():
            row = [int(x) for x in line.split()]
            rows.append(row)

        return cls._make_matrix(rows)

    @classmethod
    def from_list(cls, listoflists):
        """ создать матрицу из списка списков """

        # например: Matrix.from_list([[1, 2, 3], [4,5,6], [7,8,9]])

        rows = listoflists[:]
        return cls._make_matrix(rows)


if __name__ == '__main__':
    m1 = Matrix.from_list([[1, 2, 3], [4, 5, 6]])
    m2 = Matrix.from_list([[7, 8, 9], [10, 11, 12]])
    m3 = Matrix.__add__(m1,m2)
    print(m3)
    print(Matrix.__sub__(m2,m1))
    m1 = Matrix.make_random(3, 3)
    print(m1)
    zero_ = Matrix.make_zero(2, 2)
    print(zero_)
    #m2 = m1 + zero_
    #print(m2)
    print(m1.transpose())
    print(m1.get_rank())
    m5 = Matrix.make_random(3, 3)
    print(Matrix.__mul__(m1,m5))


