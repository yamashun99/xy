import numpy as np


class Conf:
    def __init__(self, J, L, M, beta):
        self.conf = (np.ones((L, M)) * -1).astype(int).tolist()
        self.L = L
        self.M = M
        self.J = J
        self.dtau = beta / M
        self._make_w()
        self.x = lambda x: x % L
        self.y = lambda y: y % M

    def _make_w(self):
        w_udud = np.cosh(self.J * self.dtau / 2.0)
        w_uddu = np.sinh(self.J * self.dtau / 2.0)
        self.w = {
            ((1, 1), (1, 1)): 1,
            ((-1, -1), (-1, -1)): 1,
            ((1, -1), (1, -1)): w_udud,
            ((-1, 1), (-1, 1)): w_udud,
            ((1, -1), (-1, 1)): w_uddu,
            ((-1, 1), (1, -1)): w_uddu,
        }

    def get_rn(self, i, j):
        w_old = self.w[
            (
                (self.conf[i][self.y(j + 2)], self.conf[self.x(i + 1)][self.y(j + 2)]),
                (self.conf[i][self.y(j + 1)], self.conf[self.x(i + 1)][self.y(j + 1)]),
            )
        ]
        w_new = self.w[
            (
                (self.conf[i][self.y(j + 2)], self.conf[self.x(i + 1)][self.y(j + 2)]),
                (
                    -self.conf[i][self.y(j + 1)],
                    -self.conf[self.x(i + 1)][self.y(j + 1)],
                ),
            )
        ]
        return w_new / w_old

    def get_rs(self, i, j):
        w_old = self.w[
            (
                (self.conf[i][j], self.conf[self.x(i + 1)][j]),
                (self.conf[i][self.y(j - 1)], self.conf[self.x(i + 1)][self.y(j - 1)]),
            )
        ]
        w_new = self.w[
            (
                (-self.conf[i][j], -self.conf[self.x(i + 1)][j]),
                (self.conf[i][self.y(j - 1)], self.conf[self.x(i + 1)][self.y(j - 1)]),
            )
        ]
        return w_new / w_old

    def get_re(self, i, j):
        w_old = self.w[
            (
                (
                    self.conf[self.x(i + 1)][self.y(j + 1)],
                    self.conf[self.x(i + 2)][self.y(j + 1)],
                ),
                (
                    self.conf[self.x(i + 1)][j],
                    self.conf[self.x(i + 2)][j],
                ),
            )
        ]
        w_new = self.w[
            (
                (
                    -self.conf[self.x(i + 1)][self.y(j + 1)],
                    self.conf[self.x(i + 2)][self.y(j + 1)],
                ),
                (
                    -self.conf[self.x(i + 1)][j],
                    self.conf[self.x(i + 2)][j],
                ),
            )
        ]
        return w_new / w_old

    def get_rw(self, i, j):
        w_old = self.w[
            (
                (
                    self.conf[self.x(i - 1)][self.y(j + 1)],
                    self.conf[i][self.y(j + 1)],
                ),
                (
                    self.conf[self.x(i - 1)][j],
                    self.conf[i][j],
                ),
            )
        ]
        w_new = self.w[
            (
                (
                    self.conf[self.x(i - 1)][self.y(j + 1)],
                    -self.conf[i][self.y(j + 1)],
                ),
                (
                    self.conf[self.x(i - 1)][j],
                    -self.conf[i][j],
                ),
            )
        ]
        return w_new / w_old

    def filpable(self, i, j):
        return (
            self.conf[i][j] == self.conf[i][self.y(j + 1)]
            and self.conf[self.x(i + 1)][j] == self.conf[self.x(i + 1)][self.y(j + 1)]
            and self.conf[i][j] != self.conf[self.x(i + 1)][j]
        )

    def flip(self, i, j):
        self.conf[i][j] = -self.conf[i][j]
        self.conf[i][self.y(j + 1)] = -self.conf[i][self.y(j + 1)]
        self.conf[self.x(i + 1)][j] = -self.conf[self.x(i + 1)][j]
        self.conf[self.x(i + 1)][self.y(j + 1)] = -self.conf[self.x(i + 1)][
            self.y(j + 1)
        ]

    def update(self, eo):
        for i in range(self.L // 2):
            for j in range(self.M // 2):
                ix, iy = 2 * i + eo - 1, 2 * j + eo
                if self.filpable(ix, iy):
                    rand = np.random.rand()
                    print(
                        self.get_rn(ix, iy)
                        * self.get_re(ix, iy)
                        * self.get_rs(ix, iy)
                        * self.get_rw(ix, iy)
                    )
                    if rand < self.get_rn(ix, iy) * self.get_re(ix, iy) * self.get_rs(
                        ix, iy
                    ) * self.get_rw(ix, iy):
                        self.flip(ix, iy)
