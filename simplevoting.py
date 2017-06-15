import copy

def first(vote):
    size = vote['size']
    votes = [0] * size
    for i in vote['votes']:
        votes[i['order'][0]] += i['percentage']
    maxpos = -1
    maxvote = -1
    for i in xrange(size):
        if maxvote < votes[i]:
            maxpos = i
            maxvote = votes[i]
    return (maxpos, maxvote)

def tworounds(vote):
    # Calculate percentages per choice
    size = vote['size']
    votes = [0] * size
    for i in vote['votes']:
        votes[i['order'][0]] += i['percentage']
    # Sort by said percentages
    ordered = [x for (y, x) in sorted(zip(votes, range(size)), reverse=True)]
    # Now eliminate all choices but the first two
    newvotes = copy.deepcopy(vote['votes'])
    filter = ordered[:2]
    for v in newvotes:
        tmp = v['order']
        v['order'] = [x for x in tmp if x in filter]
        #print v['percentage'], ":", v['order']
    # Now do the percentages again
    votes = [0] * size
    for i in newvotes:
        votes[i['order'][0]] += i['percentage']
    maxpos = -1
    maxvote = -1
    for i in xrange(size):
        if maxvote < votes[i]:
            maxpos = i
            maxvote = votes[i]
    return (maxpos, maxvote)

# Top gets (size-1 * percentage) points, bottom gets zero
def borda(vote):
    size = vote['size']
    votes = [0] * size
    for i in vote['votes']:
        score = size - 1
        for j in i['order']:
            votes[j] += score * i['percentage']
            score = score - 1
    maxpos = -1
    maxvote = -1
    for i in xrange(size):
        if maxvote < votes[i]:
            maxpos = i
            maxvote = votes[i]
    return (maxpos, maxvote)

def aggregate(vote):
    size = vote['size']
    agg = []
    for i in xrange(size):
        agg.append([0] * (size+1))
    for v in vote['votes']:
        tmp = v['order']
        for i in xrange(size - 1):
            for j in xrange(i + 1, size):
                agg[tmp[i]][tmp[j]] += v['percentage']
    for i in xrange(size):
        total_wins = 0
        for j in xrange(size):
            total_wins += agg[i][j]
        agg[i][size] = total_wins
    print 'Aggregated', agg
    vote['aggregated']  = agg

def detect_condorcet(vote):
    size = vote['size']
    agg = copy.deepcopy(vote['aggregated'])
    agg.sort(key = lambda x: x[size], reverse=True)
    print agg
