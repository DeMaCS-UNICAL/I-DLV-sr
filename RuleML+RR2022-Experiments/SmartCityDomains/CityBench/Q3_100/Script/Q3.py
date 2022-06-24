def float_division(VC, DM):
    CL = VC / DM
    return "{:.3f}".format(CL)


def float_sum(PSCL, CL):
    fsum = float(PSCL) + float(CL)
    return "{:.3f}".format(fsum)


def float_avg(S, X):
    favg = float(S) / float(X)
    return "{:.3f}".format(favg)
