import numpy as np


# def update(conf, L, eo):
#    for i in range(L // 2):
#        for j in range(L // 2):
#            ix, iy = 2 * i + eo, 2 * j + eo
#            if (
#                conf[ix, iy] == conf[ix, (iy + 1) % L]
#                and conf[(ix + 1) % L, iy] == conf[(ix + 1) % L, (iy + 1) % L]
#                and conf[ix, iy] == -conf[(ix + 1) % L, iy]
#            ):
#                rand = np.random.rand()
#                if rand < 0.5:
#                    conf[ix, iy] = -conf[ix, iy]
#                    conf[ix, (iy + 1) % L] = -conf[ix, (iy + 1) % L]
#                    conf[(ix + 1) % L, iy] = -conf[(ix + 1) % L, iy]
#                    conf[(ix + 1) % L, (iy + 1) % L] = -conf[(ix + 1) % L, (iy + 1) % L]
#    return conf


def update(conf, L, eo):
    conf = conf.tolist()
    for i in range(L // 2):
        for j in range(L // 2):
            ix, iy = 2 * i + eo, 2 * j + eo
            if (
                conf[ix][iy] == conf[ix][(iy + 1) % L]
                and conf[(ix + 1) % L][iy] == conf[(ix + 1) % L][(iy + 1) % L]
                and conf[ix][iy] == -conf[(ix + 1) % L][iy]
            ):
                rand = np.random.rand()
                if rand < 0.5:
                    conf[ix][iy] = -conf[ix][iy]
                    conf[ix][(iy + 1) % L] = -conf[ix][(iy + 1) % L]
                    conf[(ix + 1) % L][iy] = -conf[(ix + 1) % L][iy]
                    conf[(ix + 1) % L][(iy + 1) % L] = -conf[(ix + 1) % L][(iy + 1) % L]
    conf = np.array(conf)
    return conf
