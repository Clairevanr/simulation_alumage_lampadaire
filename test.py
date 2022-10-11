def estimation(it, nbr_u):
    tps = ((it + (nbr_u * 1)) * 3600) / 1000
    if (tps >= 86400) : # j
        tps = str(round(tps / 86400)) + "j"
    elif (tps >= 3600) : # h
        tps = str(round(tps / 3600)) + "h"
    elif (tps >= 60) : # min
        tps = str(round(tps / 60)) + "min"
    return tps  

print(estimation(100000, 1000))