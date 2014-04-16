# -*- coding: utf-8 -*-

'''
Created on 2013-9-3

@author: Qiqun.H
'''


from collections import defaultdict
 
class Trie:
    def __init__(self):
        self.root = defaultdict(Trie)
        self.value = None

    def add(self, s, value):
        """Add the string `s` to the
        `Trie` and map it to the given value."""
        head, tail = s[0], s[1:]
        cur_node = self.root[head]
        if not tail:
            cur_node.value = value
            return  # No further recursion
        self.root[head].add(tail, value)

    def lookup(self, s, default=None):
        """Look up the value corresponding to
        the string `s`. Expand the trie to cache the search."""
        head, tail = s[0], s[1:]
        node = self.root[head]
        if tail:
            return node.lookup(tail)
        return node.value or default

    def remove(self, s):
        """Remove the string s from the Trie.
        Returns *True* if the string was a member."""
        head, tail = s[0], s[1:]
        if head not in self.root:
            return False  # Not contained
        node = self.root[head]
        if tail:
            return node.remove(tail)
        else:
            del node
            return True
    
    def prefix(self, s):
        """Check whether the string `s` is a prefix
        of some member. Don't expand the trie on negatives (cf.lookup)"""
        if not s:
            return True
        head, tail = s[0], s[1:]
        if head not in self.root:
            return False  # Not contained
        node = self.root[head]
        return node.prefix(tail)
    
    def items(self):
        """Return an iterator over the items of the `Trie`."""
        for char, node in self.root.iteritems():
            if node.value is None:
                yield node.items
            else:
                yield node
                
if __name__ == "__main__":
    t = Trie()
    t.add('I am a teacher', 1)
    for each in t.items():
        print each
