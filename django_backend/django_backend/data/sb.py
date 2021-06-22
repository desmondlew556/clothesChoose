from collections import defaultdict

ranking_initializer = lambda x: dict({'rank_'+str(rank+1):0 for rank in range(10)})
def initializer():
    return {'rank_'+str(rank+1):0 for rank in range(10)}

print(initializer())