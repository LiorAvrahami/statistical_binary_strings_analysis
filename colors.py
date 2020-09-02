import itertools
alpha = 0.5
def make_iter():
    return itertools.cycle([(0.9,0.1,0.1,alpha),(0.1,0.9,0.1,alpha),(0.1,0.1,0.9,alpha),(0.7,0.7,0.1,alpha),(0.7,0.1,0.7,alpha),(0.1,0.7,0.7,alpha),(0.5,0.5,0.5,alpha)])
colors = make_iter()
