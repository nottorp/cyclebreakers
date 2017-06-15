import itertools
import random
import simplevoting

#TODO: Look into generating more uniform percentages
# This won't give an entry more than 49% - if one has over 50% it's probably pointless to analyze
def gendata(size):
    remaining = 100
    res = {'size': size }
    tmp = []
    for o in itertools.permutations(range(size)):
        p = random.randint(0, int((remaining - 1) / 2))
        remaining -= p
        tmp.append({'percentage': p, 'order': list(o)})
    res['votes'] = tmp
    return res

def test_condorcet_3():
    res = {'size': 3}
    tmp = [
        {'percentage': 33, 'order': [0, 1, 2]},
        {'percentage': 33, 'order': [1, 2, 0]},
        {'percentage': 33, 'order': [2, 0, 1]}
    ]
    res['votes'] = tmp
    return res

def test_condorcet_5():
    res = {'size': 5}
    tmp = [
        {'percentage': 33, 'order': [1, 2, 3, 0, 4]},
        {'percentage': 33, 'order': [2, 3, 1, 4, 0]},
        {'percentage': 33, 'order': [3, 1, 2, 0, 4]}
    ]
    res['votes'] = tmp
    return res

# For testing
if __name__ == "__main__":
    #aa = gendata(3)
    aa = test_condorcet_5()

    print aa
    simplevoting.aggregate(aa)
    print "----"
    print aa
    print "----"
    simplevoting.detect_condorcet(aa)

    for i in aa['votes']:
        print i['order'], ':', i['percentage']
    (pos, vote) = simplevoting.first(aa)
    print "Winner in one round:", pos, "with", vote
    (pos, vote) = simplevoting.tworounds(aa)
    print "Winner in two rounds:", pos, "with", vote
    (pos, vote) = simplevoting.borda(aa)
    print "Winner by Borda:", pos, "with", vote