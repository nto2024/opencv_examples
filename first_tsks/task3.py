import numpy as np

def sol():
    f = np.load('var016.npz')
    a = f['arr_0']
    ans = []
    for fig in a:
        ansf = []
        zs = [[], [], [], [], [], [], [], [], []]
        print(zs)
        for i in range(11):
            for j in range(11):
                zlast = -1
                for z in range(9):
                    if fig[z, i, j] == 1.:
                        if zlast != -1:
                            for k in range(zlast + 1, z):
                                zs[k].append([k, i, j])
                        zlast = z
        for i in zs:
            for j in i:
                ansf.append(j)
        if ansf == []: 
            ansf = [0]
        ans.append(ansf)
    return ans
