#!/usr/bin/python
"""
Bloom filters in Python, using SHA-1 and Python longs.

My first attempt stored the whole filter in a single arbitrary-size integer,
but for some reason that was 100x slower than storing it in a bunch of 256-bit
integers.
"""
from hashlib import sha1

def nbits_required(n):
    """ Calculate the number of bits required to represent any integer in [0, n). """
    n -= 1
    rv = 0
    while n:
        n >>= 1
        rv += 1
    return rv

class Bloom:
    """
    Bloom filter: compact hash table for membership tests with false positive.
    false positive: false records in reference are classified as True in response."""

    def __init__(self, max_decimal, nhashes, bucketbits=256):
        """
        hashbits: # of bits, that is, the length of bit array.
        max_decimal: equals 1 << hashbits
        nhashes: # of hash functions.

        Making nhashes larger will make it slower.  There are also tradeoffs
        between max_decimal, performance, and false-positive rate, which you can look
        up elsewhere.

        default bits per bucket is 256 to cut down on pickle overhead
        """
        self.bucketbits = bucketbits
        self.filter = [0L] * int((max_decimal + bucketbits - 1) / bucketbits)
        
        self.max_decimal = max_decimal
        self.nhashes = nhashes
        self.hashbits = nbits_required(max_decimal)
        assert self.hashbits * nhashes <= 160  # 160's all we get with SHA1
        
        print "[INFO]bucketbits == %s" % self.bucketbits
        print "[INFO]filter == %s" % self.filter
        print "[INFO]# of hash functions: ", self.nhashes
        print "[INFO]# of hash bits: ", self.hashbits
        print "[INFO]max decimal: ", self.max_decimal

    def add(self, astr):
        """ Add a string to the membership of the filter. """
        print "[INFO]_hashes: ", self._hashes(astr)
        assert len(self._hashes(astr)) == self.nhashes
        
        for offset in self._hashes(astr):
            bucket, bit = divmod(offset, self.bucketbits)
            self.filter[bucket] |= (1L << bit)
            
            print "[INFO] bucket == %s" % bucket
            print "[INFO] bit == %s" % bit
            print "[INFO]filter == %s" % self.filter

    def __contains__(self, astr):
        """ Returns true if the string is in the filter or it feels like it. """
        for offset in self._hashes(astr):
            bucket, bit = divmod(offset, self.bucketbits)
            if not self.filter[bucket] & (1L << bit):
                return 0
        return 1

    def _hashes(self, astr):
        """ The hashes of a particular string. """
        digest = sha1(astr).digest()
        # is there no better way to convert a byte string into a long?!
        hashlong = 0L
        for ch in digest:
            hashlong = (hashlong << 8) | ord(ch)

        rv = []
        mask = (1L << self.hashbits) - 1
        for _ in range(self.nhashes):
            # Note that this will give substantially nonuniform results if
            # self.max_decimal is not a power of 2, in order to avoid wasting hash
            # bits or doing long division:
            rv.append((hashlong & mask) % self.max_decimal)
            hashlong >>= self.hashbits
        return rv

def test_bloom():
    """ Very basic sanity test for Bloom filter implementation. """
    print 'runnning test_bloom...'

    def ok(a, b):
        assert a == b, (a, b)
    ok(map(nbits_required, range(1, 10)), [0, 1, 2, 2, 3, 3, 3, 3, 4])
    ok(nbits_required(131072), 17)
    ok(nbits_required(131073), 18)

    b = Bloom(1024, 5)
    assert 'asdf' not in b
    assert 'fdsa' not in b
    b.add('a')
    assert 'a' in b
    assert 'fdsa' not in b

    print 'pass.'
	
if __name__ == "__main__":
	test_bloom()