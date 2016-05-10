
def inch_to_mm(in_inches):
    try:
        i = iter(in_inches)
    except TypeError:
        return in_inches*25.4
    else:
        return [ inch_to_mm(x) for x in i ]

NO2_SCREW_R=inch_to_mm(0.04)
