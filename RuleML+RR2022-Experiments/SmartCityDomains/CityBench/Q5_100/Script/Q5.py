import haversine as hs

def areClose(Lat1, Lon1, Lat2, Lon2):
    loc1=(float(Lat1),float(Lon1))
    loc2=(float(Lat2),float(Lon2))
    return hs.haversine(loc1,loc2) <= 1

def float_division(VC,DM):
    CL=VC/DM
    return "{:.3f}".format(CL)