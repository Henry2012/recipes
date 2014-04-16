#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: language_detector.lang_detector.py
Description: this program
Creation: 2014-1-7
Revision: 2014-1-7
"""

class NGram(object):
    def __init__(self, text, n=3):
        self.length = None
        self.n = n
        self.table = {}
        self.parse_text(text)
        self.calculate_length()

    def parse_text(self, text):
        chars = ' ' * self.n  # initial sequence of spaces with length n

        for letter in (" ".join(text.split()) + " "):
            chars = chars[1:] + letter  # append letter to sequence of length n
            self.table[chars] = self.table.get(chars, 0) + 1  # increment count

    def calculate_length(self):
        """ Treat the N-Gram table as a vector and return its scalar magnitude
        to be used for performing a vector-based search.
        """
        self.length = sum([x * x for x in self.table.values()]) ** 0.5
        return self.length

    def __sub__(self, other):
        """ Find the difference between two NGram objects by finding the cosine
        of the angle between the two vector representations of the table of
        N-Grams. Return a float value between 0 and 1 where 0 indicates that
        the two NGrams are exactly the same.
        """
        if not isinstance(other, NGram):
            raise TypeError("Can't compare NGram with non-NGram object.")

        if self.n != other.n:
            raise TypeError("Can't compare NGram objects of different size.")

        total = 0
        for k in self.table:
            total += self.table[k] * other.table.get(k, 0)

        return 1.0 - (float(total) / (float(self.length) * float(other.length)))

    def find_match(self, languages):
        """ Out of a list of NGrams that represent individual languages, return
        the best match.
        """
        return min(languages, lambda n: self - n)

    def test():
        en = Trigram('http://gutenberg.net/dirs/etext97/lsusn11.txt')
        #NB fr and some others have English license text.
        #   no has english excerpts.
        fr = Trigram('http://gutenberg.net/dirs/etext03/candi10.txt')
        fi = Trigram('http://gutenberg.net/dirs/1/0/4/9/10492/10492-8.txt')
        no = Trigram('http://gutenberg.net/dirs/1/2/8/4/12844/12844-8.txt')
        se = Trigram('http://gutenberg.net/dirs/1/0/1/1/10117/10117-8.txt')
        no2 = Trigram('http://gutenberg.net/dirs/1/3/0/4/13041/13041-8.txt')
        en2 = Trigram('http://gutenberg.net/dirs/etext05/cfgsh10.txt')
        fr2 = Trigram('http://gutenberg.net/dirs/1/3/7/0/13704/13704-8.txt')
        print "calculating difference:"
        print "en - fr is %s" % (en - fr)
        print "fr - en is %s" % (fr - en)
        print "en - en2 is %s" % (en - en2)
        print "en - fr2 is %s" % (en - fr2)
        print "fr - en2 is %s" % (fr - en2)
        print "fr - fr2 is %s" % (fr - fr2)
        print "fr2 - en2 is %s" % (fr2 - en2)
        print "fi - fr  is %s" % (fi - fr)
        print "fi - en  is %s" % (fi - en)
        print "fi - se  is %s" % (fi - se)
        print "no - se  is %s" % (no - se)
        print "en - no  is %s" % (en - no)
        print "no - no2  is %s" % (no - no2)
        print "se - no2  is %s" % (se - no2)
        print "en - no2  is %s" % (en - no2)
        print "fr - no2  is %s" % (fr - no2)
    
        print "\nmaking up English"
        print en.makeWords(30)
        print "\nmaking up French"
        print fr.makeWords(30)


if __name__ == '__main__':
    test()