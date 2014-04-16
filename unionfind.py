"""UnionFind.py

Union-find data structure. Based on Josiah Carlson's code,
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/215912
with significant additional changes by D. Eppstein.

Reference: http://www.cs.princeton.edu/~rs/AlgsDS07/01UnionFind.pdf
"""

class UnionFind(object):
    """Union-find data structure.

    Each unionFind instance X maintains a family of disjoint sets of
    hashable objects, supporting the following two methods:

    - X[item] returns a name for the set containing the given item.
      Each set is named by an arbitrarily-chosen one of its members; as
      long as the set remains unchanged it will keep the same name. If
      the item is not yet part of a set in X, a new singleton set is
      created for it.

    - X.union(item1, item2, ...) merges the sets containing each item
      into a single larger set.  If any item is not yet part of a set
      in X, it is added to X as one of the members of the merged set.
      
    - X.find(item1, item2) returns True when the two are in the same set,
      and vice verse.
    """

    def __init__(self):
        """Create a new empty union-find structure."""
        self.weights = {}
        self.parents = {}

    def __getitem__(self, obj):
        """Find and return the name of the set containing the object."""

        # check for previously unknown object
        if obj not in self.parents:
            self.parents[obj] = obj
            self.weights[obj] = 1
            return obj

        # find path of objects leading to the root
        path = [obj]
        root = self.parents[obj]
        while root != path[-1]:
            path.append(root)
            root = self.parents[root]

        # compress the path and return
        for ancestor in path:
            self.parents[ancestor] = root
        return root
        
    def __iter__(self):
        """Iterate through all items ever found or unioned by this structure."""
        return iter(self.parents)
    
    def find(self, obj1, obj2):
        return self.parents[obj1] is self.parents[obj2]

    def union(self, *objects):
        """Find sets containing the objects and merge them all."""
        roots = [self[x] for x in objects]
        
        # compare both the two elements in order
        heaviest = max([(self.weights[r], r) for r in roots])[1]
        for r in roots:
            if r != heaviest:
                self.weights[heaviest] += self.weights[r]
                self.parents[r] = heaviest

if __name__ == "__main__":
    
    unionFind = UnionFind()
    for i in range(10):
        unionFind[i]
        
#     unionFind.union(2,3,4,9)
#     unionFind.union(5,6)
#     
#     print unionFind.find(2,3) 
#     print unionFind.find(4,5)
#     print unionFind[3]
#     print unionFind[5]

    unionFind.union(1, 2, 3)
    unionFind.union(2, 9)
    print unionFind.weights.values()
    print unionFind.parents.values()
