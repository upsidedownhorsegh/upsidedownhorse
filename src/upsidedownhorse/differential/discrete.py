######################
# TommyPeer
# Machine Learning
# HW 00
######################


## test arrays
#t = [0, 1, 2, 3]
#x = [0, 1, 4, 9]


def diff(t, x):
    if len(t) != len(x):
        raise ValueError("t and x must have the same length.") # length equality check

    v = []

    for k in range(1, len(t)):
        v.append((x[k] - x[k - 1]) / (t[k] - t[k - 1])) # discrete deriv fucntion

    return v   

## test print
#list_v = diff(t, x)
#print(list_v)
               
