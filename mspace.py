#!/usr/bin/python -tt 
# -*- coding: utf-8 -*- 
 
# mspace.py - An implementation of metric space indexes for efficient 
# similarity search 
# 
# Copyright (C) 2007s2012 Jochen Spieker 
# 
# This program is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public License version 2 as 
# published by the Free Software Foundation. 
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU 
# General Public License for more details. 
# 
# You should have received a copy of the GNU General Public License 
# along with this program; if not, write to the Free Software 
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, 
# USA. 
 
""" 
 
Metric Spaces 
============== 
 
.. contents:: 
 
Introduction 
------------- 
 
This module provides efficient similarity search by implementing 
different data structures for indexing metric spaces.  You can use it to 
index an arbitrary number of objects which you later want to search for 
objects "similar" to a given other object. 
 
For this module to be useful, you need a function with metric properties 
(see below for a definition) which you can apply to the type of objects 
you want to search for. The only pre-defined metric funtion in this 
module is `levenshtein`, which is a common metric to calculate the 
(dis)similarity of two strings. 
 
Beware that the indexing phase might take a long time, depending on the 
number of objects you want to index and the runtime of your metric 
distance function. Indexing only pays off when you are planning to do a 
lot of searches. 
 
Definitions 
............ 
 
A metric space is a pair ``(S, f)`` where ``S`` is an abritrary 
(possibly infinite) set of objects and ``f`` is a function which returns 
a "distance" for any two objects ``x``, ``y`` in ``S``. This distance is 
a number used to express the similarity between the two objects. The 
larger the distance, the more they differ. A distance of zero means they 
are considered equal. 
 
The function ``f`` has to be a "metric", i.e. the following conditions 
have to be met for all ``x``, ``y``, ``z`` in ``S``: 
 
-  ``f(x, y) >= 0`` 
 
   (positivity) 
 
-  ``f(x, y) == f(y, x)`` 
 
   (symmetry) 
 
-  ``f(x, z) <= f(x, y) + f(y, z)`` 
 
   (triangle inequality) 
 
This definition adheres to most people's intuitive understanding of the 
distance between two points in a Euclidian space (of arbitrary 
dimensionality).  [#euclid]_ Imagine you have three points in a 
2-dimensional space like this:: 
 
    A-------B 
     \     / 
      \   / 
       \ / 
        C 
 
It is evident that the distance between two of these points is 
necessarily larger than (or equal to) zero, and that the direction you 
take for measuring (from ``A`` to ``B`` or vice versa) has no influence 
on the distance. The third condition, the triangle inequality is easy to 
grasp, too: if you know the distances between ``A`` and ``B`` and 
between ``B`` and ``C``, you can be sure that their sum is equal to or 
larger than the distance between ``A`` and ``C``. Voila, there's your 
metric space. 
 
In many cases, metric distance functions take a long time to compute. 
Because of this, data structures used to index metric spaces are 
designed to minimize the number of distance computations necessary for 
searching the whole space by using the properties of its metric function 
(most notably the triangle inequality) to discard as many objects as 
possible after every computation. 
 
.. [#euclid] In fact, Euclidian spaces are one type of metric space. 
 
 
Use cases & caveats 
.................... 
 
Metric distance functions can be defined for objects other than points 
in Euclidian space, too.  One very well known distance function is the 
Levenshtein distance, which is applicable to arbitrary strings. Since it 
is quite popular and indexing strings is one of the major use cases for 
metric spaces, an implementation of this function is included in this 
module. Other metric distance functions for strings are the 
Damerau-Levenshtein variant and Hamming distance. These can be used for 
a variety of tasks, such as spell-checking, record linkage (or 
"deduplication"), error detection etc. 
 
Please note that indexing a large number of objects usually takes a 
considerable amount of time *and* memory. Indexing only pays off if you 
are going to do *a lot* of searches in the index. If you just want to 
search a set of objects for all objects similar to one or a few other 
objects, you are better off comparing them sequentially by hand with 
your distance function. 
 
Installation 
............. 
 
.. _Psyco: http://psyco.sourceforge.net/ 
 
This file is a stand-alone module for Python 2.4 and later which you 
only have to save somewhere in your ``PYTHONPATH``. [#pythonpath]_ No 
installation is necessary. The only tight dependencies are the modules 
``sys``, ``random`` and ``weakref`` which are most probably already 
included in your Python installation. 
 
If you are using this on a 32 Bit i386 machine running Windows or Linux, 
you probably also want to install Psyco_ which speeds up execution times 
quite noticeably (in exchange for only a slightly increased memory 
usage). Psyco will be used automatically if it is available. 
 
.. [#pythonpath] Run ``python -c "import sys; print sys.path"`` to learn 
  where Python currently looks for modules. 
 
The most current version is always available from this site: 
 
http://well-adjusted.de/mspace.py/ 
 
The project is currently kept in SVN and may be obtained from the 
following URL: 
 
svn://svn.well-adjusted.de/mspace/trunk 
 
Basic usage 
------------ 
 
Index creation 
............... 
 
Say you have a dictionary file containing one or more words per line. 
You can make an index of all the words in it by doing: 
 
.. python:: 
 
    >>> import mspace 
    >>> mydict = file('dictionary.txt') 
    >>> words = mspace.tokenizer(mydict) 
    >>> index = mspace.VPTree(words, mspace.levenshtein) 
 
You can delay the time-comsuming construction phase by creating the 
index without any parameters and explicitly calling ``construct`` at a 
later time: 
 
.. python:: 
 
    >>> index = mspace.VPTree() 
    >>> index.construct(words, mspace.levenshtein) 
 
Please note that the index' content is dismissed on every call to 
``construct``. The index is built from scratch with only the objects and 
distance function passed as parameters. 
 
Performing range-searches 
.......................... 
 
After you have built the index (and got yourself some coffee if the 
index is large) you may search it for all objects having distance to a 
given other object between arbitrary bounds: 
 
.. python:: 
 
    >>> index.range_search('WOOD', min_dist=0, max_dist=1) 
    ['GOOD', 'WOOD', 'WOOL', 'MOOD'] 
 
In this case, you received four results: the object you searched for 
(apparently it has been in your dictionary, too) and two other objects 
"GOOD" and "WOOL", both of which have the requested maximum distance of 
one to your query object. Result lists are unordered and do not contain 
information about their contents' distance to the query object. If you 
need this, you have to calculate it by hand. 
 
Both ``min_dist`` and ``max_dist`` are optional parameters defaulting to 
zero. Thus, if you leave them out, a search for objects which are 
exactly equal (as defined by your distance function) to the query object 
is performed. For historical reasons, and since range-searching with a 
minimum distance of zero and a maximum greater than zero is quite 
common, there is a shortcut to search with ``min_dist=0``: 
 
.. python:: 
 
    >>> index.search('WOOD', 1) 
    ['GOOD', 'WOOD', 'WOOL', 'MOOD'] 
 
 
Performing nearest-neighbour-searches 
...................................... 
 
The second type of search you can perform is "k-nearest-neighbour" 
search. It returns a given number of objects from the index that are 
closest to the query object. Search results are guaranteed to never 
contain an object with a distance to the query object that is larger 
than that of any other object in the tree. 
 
Result lists are composed of ``(object, distance)`` tuples, sorted 
ascendingly by the distance. If you don't specify a maximum number of 
matches to return, it defaults to one: 
 
.. python:: 
 
    >>> index.nn_search('WOOD') 
    [('WOOD', 0)] 
    >>> index.nn_search('WOOD', 5) 
    [('WOOD', 0), ('WOOL', 1), ('GOOD', 1), ('MOOD', 1), ('FOOT', 2)] 
 
Note that the index may contain other objects with a distance of two to 
the query object ``'WOOD'`` (e.g. ``'FOOL'``). They have just been cut 
off because a maximum of five objects has been requested. You have no 
influence on the choice of representatives that is made. 
 
Note that you must not expect this method to always return a list of 
length ``num`` because you might ask for more objects than are currently 
in the index. 
 
 
Advanced usage 
--------------- 
 
Indexing complex objects 
......................... 
 
If you have "complex" objects which you want to index by only one 
specific attribute, you can write a simple wrapper around `levenshtein` 
(or some other function applicable to the attribute) which extracts this 
attribute from your objects and returns the distance between their 
attributes' value.  This way you can search for and retrieve complex 
objects from the index while comparing only a single attribute 
 
.. python:: 
 
    >>> import mspace 
    >>> 
    >>> class Record(object): 
    ...     def __init__(self, firstname, surname): 
    ...         self._firstname, self._surname = firstname, surname 
    ... 
    >>> def firstnameLev(r1, r2): 
    ...     return mspace.levenshtein(r1._firstname, r2._firstname) 
    ... 
    >>> index = mspace.VPTree(listOfRecords, firstnameLev) 
    >>> rec = Record("Paul", "Brady") 
    >>> index.search(rec, 2) 
    [<Record: 'Paula Bean'>, <Record: 'Raoul Perky'>, <Record: 'Paul Simon'>] 
 
Of course you can also use more advanced techniques like writing a 
function factory which returns a function that extracts arbitrary 
attributes from your objects and applies a metric function to it: 
 
.. python:: 
 
    >>> def metric_using_attr(metric, attr): 
    ...     def f(one, other, attr=attr): 
    ...         attr1, attr2 = getattr(one, attr), getattr(other, attr) 
    ...         return metric(attr1, attr2) 
    ...     return f 
    ... 
    >>> metric = metric_using_attr(mspace.levenshtein, "_firstname") 
    >>> metric( Record("Paul", "Brady"), Record("Paul", "Simon") ) 
    0 
 
(Note that the inner function ``f`` in this example deviates from the 
standard protocol by accepting an optional third parameter.  This is 
done here only to pull the name ``attr`` into the inner function's 
namespace to save some time when looking up its associated value.  No 
index structure in this module will ever call its distance function with 
more than two parameters anyway, so that whatever you passed as ``attr`` 
to ``metric_using_attr`` when creating your function will be used when 
this function gets called by an index. Got it?) 
 
Reverse indexes 
................ 
 
Of course you can use a similar technique to avoid full indexes and 
instead create an index which only contains references to your data (in 
a database, text file, somewhere on the net etc.). Your distance 
function would then use the supplied values to fetch the objects to 
compare from your data source.  But, I cannot stress this enough, your 
distance function's performance is absolutely crucial to efficient 
indexing and searching. Therefore you should make sure that your way of 
accessing the data is really fast. 
 
Choice of data structure 
------------------------- 
 
This module currently gives you two data structures to choose from. 
While the underlying algorithms are different, their search results 
(given the same set of objects to index, distance function and maximum 
distance) are exactly the same. If you find a scenario where this is not 
the case, please let me know because this would be a serious bug. 
 
Capabilities 
............. 
 
The algorithms implemented in this module have different capabilities 
which are displayed in the table below: 
 
+--------------------+-------+-------+ 
|                    |VPTree |BKTree | 
+====================+=======+=======+ 
|non-discrete metric |     X |       | 
+--------------------+-------+-------+ 
|insertion           |       |     X | 
+--------------------+-------+-------+ 
|deletion            |       |       | 
+--------------------+-------+-------+ 
 
The first row is about the value returned by the distance function the 
index uses. BKTrees are not prepared to handle non-discrete distances 
(for example floats) and will most probably perform really bad when they 
occur. 
 
The other two rows describe what you can do with the indexes *after* 
they have been constructed. Please note that neither of them may shrink 
over time. Only BKTrees are able to handle insertion efficiently. 
 
Performance 
............ 
 
[In short: you are probably better off using BKTrees unless you need a 
non-discrete metric. When in doubt, test both options.] 
 
Obviously, the whole point of this module is to speed up the process of 
finding objects similar to one another. And, as you can imagine, the 
different algorithms perform differently when exposed to a specific 
problem. 
 
Here's an example: I took the file ``american-english-large`` from the 
Debian package ``wamerican-large`` and did some time measurements of 
indexing and searching a random subset of it. The machine I used is an 
1.1GHz Pentium3 running Python 2.4 from Debian stable **with Psyco 
enabled**. Please note that the following numbers have been determined 
completely unscientifical. I only show them to give you an idea of what 
to expect. For serious benchmarking, I should have used the ``timeit`` 
module. Nevertheless, this is it: 
 
 
+------+------------------------+------------------------+ 
|      |BKTree                  |VPTree                  | 
+======+======+=========+=======+=======+========+=======+ 
|size  |time  |per node |height |time   |per node|height | 
+------+------+---------+-------+-------+--------+-------+ 
| 5000 |  2.92|0.000584 |11     |   7.40|0.001480|     21| 
+------+------+---------+-------+-------+--------+-------+ 
|10000 |  6.32|0.000632 |14     |  16.02|0.001602|     22| 
+------+------+---------+-------+-------+--------+-------+ 
|15000 |  9.95|0.000663 |14     |  28.35|0.001890|     24| 
+------+------+---------+-------+-------+--------+-------+ 
|20000 | 13.70|0.000685 |14     |  41.40|0.002070|     24| 
+------+------+---------+-------+-------+--------+-------+ 
|25000 | 17.46|0.000699 |15     |  50.63|0.002025|     25| 
+------+------+---------+-------+-------+--------+-------+ 
|30000 | 21.81|0.000727 |15     |  55.47|0.001849|     25| 
+------+------+---------+-------+-------+--------+-------+ 
|35000 | 25.77|0.000736 |16     |  64.43|0.001841|     26| 
+------+------+---------+-------+-------+--------+-------+ 
|40000 | 29.40|0.000735 |16     |  75.45|0.001886|     26| 
+------+------+---------+-------+-------+--------+-------+ 
|45000 | 41.28|0.000917 |16     |  96.36|0.002141|     26| 
+------+------+---------+-------+-------+--------+-------+ 
|50000 | 37.62|0.000752 |16     |  95.31|0.001906|     28| 
+------+------+---------+-------+-------+--------+-------+ 
 
 
This table shows construction times (total and per node in seconds) for 
data sets of a given size. Additionally, you can see the height 
[#height]_ of the trees.  Apparently, BKTrees can be constructed a lot 
faster than VPTrees. Both of them need an increasing time per node with 
growing data sets. This is expected since construction complexity is 
``O(n log(n))`` in both cases. 
 
+---------------+-----------------+-----------------+ 
|               |BK, size: 50,000 |VP, size: 50,000 | 
+------+--------+-------+---------+-------+---------+ 
|k     |results |  time |  # dist |  time |  # dist | 
+------+--------+-------+---------+-------+---------+ 
|0     |   0.89 |0.0008 |    8.14 | 0.0019|    17.28| 
+------+--------+-------+---------+-------+---------+ 
|1     |   4.07 |0.1670 | 1583.77 | 0.2801|  1933.64| 
+------+--------+-------+---------+-------+---------+ 
|2     |  38.10 |1.1687 |10353.31 | 1.4413| 13845.67| 
+------+--------+-------+---------+-------+---------+ 
|3     | 304.57 |2.5614 |22202.28 | 3.0497| 27514.51| 
+------+--------+-------+---------+-------+---------+ 
|4     |1584.86 |3.8727 |32376.54 | 4.1518| 36877.62| 
+------+--------+-------+---------+-------+---------+ 
|5     |5317.03 |4.4182 |39616.04 | 4.9935| 42720.38| 
+------+--------+-------+---------+-------+---------+ 
 
This table shows the runtime of searches done in the trees (in seconds), 
the number of distance calculations done and the number of results for 
growing error tolerance. All values are given as average over 100 random 
searches (from the same file, but not necessarily from the set of 
indexed objects).  As you can see, search runtime (tightly connected to 
the number of distance calculations) literally explodes for larger 
values of ``k``.  This growth only fades when an increased part of the 
complete search space is examined (the number of distance calculations 
equals the number of nodes compared with the query object). 
 
As you can see, too, long search runtimes for large values of ``k`` 
don't actually hurt usability very much since you only get a usable 
number of results for small ``k`` anyway. This is of course due to the 
nature of the data set and the distance function used in this example. 
Your application may vary greatly. 
 
You also have to keep in mind that the dictionary I used contains almost 
no duplicates. If you used the words of a real document as your data 
set, your tree would have significantly less nodes than the number of 
words in your document since you typically repeat a lot of words very 
often. A quick test with my diploma thesis revealed only 4400 distinct 
words in a document with 14,000 words (including LaTeX commands). This 
makes searching much faster because equal objects (as defined by the 
distance function) are only evaluated once. 
 
.. [#height] If you look closely, you can see that the VPTree's height 
   doesn't grow continuously when the data set grows. The reason for 
   that phenomenon is that this implementation does not try very hard to 
   pick a good vantage point which is the key factor to get 
   well-balanced trees. So, in some cases, a vantage point may be chosen 
   that may result in trees which are higher than strictly necessary. 
 
Optimization potential (or: Why the f*ck is this so slow!?) 
------------------------------------------------------------ 
 
Ok, you have tried to index your small dictionary file and start to 
wonder why this easy task takes several minutes. Here are a couple of 
(possible) reasons: 
 
- Indexing takes ``O(n log(n))`` for all data structures currently 
  implemented. So yes, doubling the number of indexed objects will 
  necessarily more than double your runtime for indexing, sorry. 
 
- Python is slow. I have written an implementation very similar to this 
  one in Java which is significantly faster (by a factor of about 15 to 
  25, even when using Psyco_!).  But the java implementation eats more 
  memory and unfortunately I cannot release it under a free license. 
 
- Recursion is slow in Python. Recursion is the most natural way to 
  create and search trees and this code uses it a lot. Most of the 
  recursion in this module is "tail recursion", but the Python 
  interpreter is not able to optimize it into loops. 
 
  [Note: as of revision 60, searching in both trees and inserting into 
  BKTrees has been rewritten using loops instead of recursion. 
  Perfomance gain is quite small, though.] 
 
- The distance distribution in your metric space is too dense. This 
  leads to the data structures being unable to discard large parts of 
  the indexed space while searching. In pathological cases, you may end 
  up with data structures resembling linked lists. 
 
- Your distance function is non-discrete, i.e. it returns floats. How 
  well this is supported depends on the index structure in use. 
 
- Your metric function is very expensive. Remember that this function 
  has to be called *very often* during indexing. You may use this 
  module's attribute ``dist_ctr`` to get an idea how often this is done. 
  It is incremented by one on every call to your distance function and 
  is otherwise unused. 
 
- You are searching for non-similar objects. If you, for example,  have 
  an index of strings with an average length of six characters and you 
  are continuously searching for strings with a maximum distance of 
  three or more, do not expect the search to be significantly faster 
  than linear testing of the complete search space. It may even be 
  slower. 
 
Possible solutions include: 
 
- Rewrite in C. Since I cannot be bothered to learn C, someone else 
  would have to do this. 
 
- Use Pyrex or Psyco_. Quick tests with Psyco suggest that indexing 
  becomes about 3-4 times faster. This is as easy as doing an ``import 
  psyco; psyco.full()`` in your program. Read Psyco's manual for tuning 
  options. 
 
  [Note: as of about revision 46, on module loading an attempt is made 
  to import and enable Psyco for levenshtein and the tree classes. If it 
  doesn't succeed, you'll get a performance warning on ``stderr`` but 
  everything will continue to work flawlessly.] 
 
- Pickle trees for static data sets. Pickling and unpickling indexes 
  using Python's standard ``pickle`` module is quite fast. But beware 
  that a pickled index takes a lot more space than your plain data. 
 
- Rewrite tree construction and searching using loops. I am not sure 
  whether this will be faster, but it will probably take less memory 
  than the current approach and fix the problem with Python's recursion 
  limit. I fear that code readibility will suffer, though. The current 
  implementations are quite close to the original descriptions of the 
  algorithms. 
 
  [Note: partially done, see above.] 
 
- Optimize the distance function in use. Since I do not know your 
  distance function, I cannot help you with this. 
 
  As for `levenshtein`: the algorithm implemented in this module is the 
  classical dynamic programming variant with ``O(|n|*|m|)`` time 
  complexity (and ``O(min(|n|, |m|))`` for space).  Other algorithms for 
  Levenshtein try not to compute the whole matrix but only the values 
  around the diagonal of the matrix that are strictly necessary. By 
  doing this, the average ``O(|n|*|m|)`` of the classical dynamic 
  programming algorithm could be improved to something like 
  ``O(k*|n|)``. While it isn't obvious how much wall clock time this 
  approarch saves in reality, it may be in fact a whole lot faster 
  because ``k`` is usually only a fraction of the length of the input 
  strings. 
 
  And if you take a close look at the algorithms, you may realize that 
  searching may be sped up by using an algorithm that doesn't actually 
  compute the distance between two strings, but one that only answers 
  whether two strings have a distance less than or equal to a specified 
  maximum distance. This can be done in ``O(k^2)`` and should boost 
  search performance quite noticeably. 
 
  .. _Citeseer: http://citeseer.ist.psu.edu/navarro99guided.html 
 
 
  If you are interested in any of these optimizations, I suggest reading 
  Gonzalo Navarro's excellent survey "Guided Tour To Approximate String 
  Matching" which you can get from Citeseer_. 
 
  Currently, this module always uses the same function for searching and 
  indexing. If you want to test your own implementations, you have to 
  replace your index object's ``_func`` attribute after indexing and 
  before searching. 
 
 
Contact 
-------- 
 
For comments, patches, flames and hugs send mail to: 
jrspieker@well-adjusted.de. 
 
""" 
 
__docformat__ = 'restructuredtext en' 
__author__    = '$Author: jrschulz $' 
__version__   = '$Revision: 119 $' 
__date__      = '$Date: 2012-09-17 02:13:52 +0200 (Mon, 17 Sep 2012) $' 
__license__   = "GPL" 
 
import sys, random, weakref 
 
class MetricTree(object): 
    """ 
 
    Base class for metric space indexes which have tree-like properties. 
    It's implementation is not complete enough to make it actually 
    usable, but it should make it quite easy to implement other indexing 
    and searching strategies. In an ideal case, all you have to do is to 
    derive from this class, implement the methods `construct`, 
    `_get_child_candidates` and optionally `insert` and make `children` 
    an attribute or property returning all child nodes of the current 
    node. If you need an ``__init__`` method, you should call 
    ``super(YourClass, self).__init__(objects, func, parent)`` in its 
    end as well. 
 
    Instances of this class (and its subclasses, of course) are supposed 
    to be recursive data structures. This means that they may be treated 
    like the root of a tree whether they have a parent or not. This 
    means every node has: 
 
    - a list of `_values` with every element of that list having a 
      distance of zero to all other elements in the list. Because of 
      triangle inequality, you only need to check this condition against 
      one element of this list. 
 
    - a `_parent` (`None` for root nodes) 
 
    - a list of `children` (empty list for leaf nodes) 
 
    - a `_height` (one for trees consisting of only one node) 
 
    - a number of nodes `_num_nodes` (the total number of nodes in this 
      subtree) 
 
    - a `_size` (the total number of objects stored in this subtree) 
 
    Note that in many (most? some?) cases, implementors don't have to 
    fiddle with these values directly. Instead, there are some helper 
    methods like `_incr_node_counter` and `_incr_size` that may be 
    called at appropriate times. If in doubt, just implement what you 
    strictly need first and then take a look whether node, size and 
    height counting works as expected (and whether you care). 
 
    As a bonus, this class implements some of python's magic methods so 
    that you can iterate over its instances' content and use the ``in`` 
    operator to test for the existence of an object using the distance 
    function. 
 
    """ 
 
    _parent = None 
    """ 
 
    The parent of this node. ``None`` for root nodes. 
 
    """ 
 
    _values = list() 
    """ 
 
    A list of values in this subtree. All objects in this list are 
    considered equal by the distance function in use. 
 
    """ 
 
    _size = 0 
    """ 
 
    The number of objects in this subtree. 
 
    """ 
 
    _func = 0 
    """ 
 
    The distance function used for indexing and searching. It has to 
    accept any two objects from the list of objects you are indexing as 
    arguments and return a non-negative integer (or long). 
 
    """ 
 
    _height = 0 
    """ 
    """ 
 
    _num_nodes = 0 
    """ 
    """ 
 
    def __init__(self, objects=None, func=None, parent=None): 
        """ 
 
        Create a new metric tree. If ``objects`` and ``func`` are given, 
        the given objects will be indexed immediately using the distance 
        function which makes it possible to immediately start so search 
        for other objects in it. Otherwise, you have to call `construct` 
        later in order to make use of this metric tree. 
 
        """ 
        self._values = list() 
        self._size = 0 
        self._height = 1 
        self._func = func 
        self.parent = parent 
        self._num_nodes = 0 
        self._incr_node_counter() 
        self._calculate_height() 
        if objects and func: 
            self.construct(objects, func) 
 
    def range_search(self, obj, min_dist=0, max_dist=0): 
        """ 
 
        Return a list of all objects in this subtree whose distance to 
        `obj` is at least `min_dist` and at most `max_dist`.  `min_dist` 
        and `max_dist` have to satisfy the condition ``0 <= min_dist <= 
        max_dist``. 
 
        If this metric tree is empty, an empty list is returned, 
        regardless of whether this tree has been previously constructed 
        or not. 
 
        If calling the distance function fails for any reason, 
        `UnindexableObjectError` will be raised. 
 
        """ 
        assert( 0 <= min_dist <= max_dist ) 
        if not self: return list() 
        result, candidates = list(), [self] 
        while candidates: 
            node = candidates.pop() 
            distance = node._get_dist(obj) 
            if min_dist <= distance <= max_dist: 
                result.extend(node._values) 
            candidates.extend( node._get_child_candidates( 
                distance, min_dist, max_dist)) 
        return result 
 
    def search(self, obj, max_dist): 
        """ 
 
        Equivalent to range_search(obj, min_dist=0, max_dist). 
 
        """ 
        return self.range_search(obj, max_dist=max_dist) 
 
    def nn_search(self, obj, num=1): 
        """ 
 
        Perform a k-nearest-neighbour search and return a sorted list of 
        at most ``num`` objects together with their distance to the 
        query object (``(object, distance)`` tuples). Sorting is done by 
        the distance (ascending). Of course, `num` has to be an ``int`` 
        (or ``long``, for that matter) larger than zero. 
 
        For obvious reasons, this method cannot return more objects than 
        are currently present in the tree. That means, if ``num > 
        len(self)``, only ``len(self)`` pairs of ```(object, distance)`` 
        will be returned. 
 
        If this metric tree is empty, an empty list is returned, 
        regardless of whether this tree has been previously constructed 
        or not. 
 
        If several objects in this tree share the same maximum distance 
        to `obj`, no guarantee is given about which of these objects 
        will be returned and which are left out. 
 
        If calling the distance function fails for any reason, 
        `UnindexableObjectError` will be raised. 
 
        """ 
        if num < 1: return list() 
        if not self: return list() 
        neighbours = list() # list of (value, distance) tuples 
        candidates = [self] 
        def cmp_neighbours(a, b): return cmp(a[1], b[1]) 
        while candidates: 
            cand = candidates.pop() 
            distance = cand._get_dist(obj) 
            candidate_is_neighbour = bool([1 for n in neighbours 
                if distance < n[1]]) 
            if candidate_is_neighbour or len(neighbours) < num: 
                neighbours.extend([(v, distance) for v in cand._values]) 
                neighbours.sort(cmp_neighbours) 
            if len(neighbours) > num: 
                neighbours = neighbours[:num] 
            elif len(neighbours) == num: 
                max_dist = neighbours[-1][1] 
                if max_dist == 0: 
                    break 
                candidates.extend( 
                    node._get_child_candidates( distance, 0, max_dist)) 
            else: 
                candidates.extend(node.children) 
        return neighbours 
 
    def _get_child_candidates(self, distance, min_dist, max_dist): 
        """ 
 
        Return a sequence of child nodes that may contain objects with a 
        distance difference between (inclusive) ``min`` and ``max`` to a 
        certain query object.  Note that the query object is *not* 
        passed to this method.  Instead, ``distance`` is the query 
        object's previously calculated distance to this node. 
 
        """ 
        raise NotImplementedError() 
 
    def construct(self, objects, func): 
        """ 
 
        (Re)Index this space with the given ``objects`` using the 
        distance function ``func``.  Previous contents will be 
        discarded.  ``objects`` has to be a sequence or an iterable. The 
        distance function ``func`` needs to be applicable to all objects 
        contained in ``objects``. 
 
        If calling the distance function fails for any reason, 
        `UnindexableObjectError` will be raised. 
 
        """ 
        raise NotImplementedError() 
 
    def insert(self, obj): 
        """ 
 
        Insert a single object into the metric tree.  Returns ``self``, 
        i.e. the tree itself. 
 
        This method may not be implemented by all subclasses of 
        `MetricTree` since not all data structures allow to do this 
        efficiently.  `NotImplementedError` will be raised when this is 
        the case. 
 
        If calling the distance function fails for any reason, 
        `UnindexableObjectError` will be raised. 
 
        """ 
        raise NotImplementedError() 
 
    def is_root(self): 
        """ 
 
        Answer whether this node is the root of a tree (i.e. it has no 
        parent). 
 
        """ 
        return self.parent is None 
 
    def is_leaf(self): 
        """ 
 
        Answer whether this node is a leaf node (i.e. it has no 
        children) 
 
        """ 
        return not self.children 
 
    def __children(self): 
        """ 
 
        A sequence of this node's children. 
 
        The possible number of children per node is 
        implementation-dependent. Leaf nodes return an empty sequence. 
 
        """ 
        raise NotImplementedError() 
    children = property(__children) 
 
    def __num_nodes(self): 
        """ 
 
        The number of nodes in this tree. 
 
        This may be different from the number of objects contained in 
        this tree in cases where two or more of these objects are 
        considered equal by the distance function in use (i.e., for two 
        objects ``p`` and ``q``, calling ``self._func(p, q)`` returns 
        ``0`` and when the tree is empty, i.e. there is one node (the 
        root node) but it doesn't contain any values. 
 
        """ 
        return self._num_nodes 
    num_nodes = property(__num_nodes) 
 
 
    def __height(self): 
        """ 
 
        The height of this tree. 
 
        Empty trees have a height of ``0``, trees containing one or more 
        objects have a height ``>= 1``. 
 
        """ 
        return self._height 
    height = property(__height) 
 
    def __parent(self): 
        """ 
 
        The parent of this node. `None` if this node is the root 
        of a tree. 
 
        """ 
        return self._parent 
 
    def __set_parent(self, parent): 
        """ 
 
        Set the parent of this node. 
 
        Parent references are stored as "weak references" to avoid 
        circular references which the garbage collector cannot dissolve 
        by itself. 
 
        """ 
        if parent is None: 
            self._parent = None 
        else: 
            # the callback ensures that the weakref is deleted 
            # as soon as the parent node disappears so that this 
            # node recognizes it is the new root. 
            callback = lambda proxy: self.__set_parent(None) 
            self._parent = weakref.proxy(parent, callback) 
 
    parent = property(__parent, __set_parent) 
 
    def _incr_size(self, incr=1): 
        """ 
 
        Increment the size counter for this node and all its parents 
        recursively. 
 
        Should be called whenever an object is inserted into the tree. 
 
        """ 
        def f(node, incr=incr): node._size += incr 
        self._apply_upwards(f) 
 
    def _calculate_height(self, recursive=True): 
        """ 
 
        Set this node's height to one and (if `recursive` is `True`) 
        propagate this change upwards in the tree. 
 
        """ 
        self._height = height = 1 
        if recursive: 
            node = self.parent 
            while node is not None: 
                height += 1 
                if node._height < height: 
                    node._height = height 
                    node = node.parent 
                else: 
                    node = None 
 
    def _incr_node_counter(self, incr=1): 
        """ 
 
        Increment the node counter for this node and all its parents 
        recursively. 
 
        Should be called whenever a new child of this node is created. 
 
        """ 
        def f(node, incr=incr): node._num_nodes += incr 
        self._apply_upwards(f) 
 
    def _apply_upwards(self, func, **args): 
        """ 
 
        Helper method to apply a function to this node and all its 
        parents recursively. The given function must accept one node as 
        the first parameter and may accept arbitrary keyword parameters 
        as well. 
 
        """ 
        node = self 
        func(node, **args) 
        while not node.is_root(): 
            node = node.parent 
            func(node, **args) 
 
    def _get_dist(self, obj): 
        """ 
 
        Apply this node's distance function to the given object and one 
        of this node's values. 
 
        Raises `UnindexableObjectError` when distance computation fails. 
 
        """ 
        global dist_ctr 
        try: 
            distance = self._func(self._values[0], obj) 
            dist_ctr += 1 
        except IndexError, e: 
            sys.stderr.write("Node is empty, cannot calculate distance!\n") 
            raise e 
        except Exception, e: 
            raise UnindexableObjectError(e, "Cannot calculate distance" 
                    + " between objects %s and %s using %s" 
                        % (self._values[0], obj, self._func)) 
        return distance 
 
    def __iter__(self): 
        """ 
 
        A generator that yields all objects in this node and its 
        children by doing recursive pre-order traversal. Implementors 
        might choose to use another traversal method which better suits 
        their data structure. 
 
        Note that objects are returned in no specific order. 
 
        This implementation will always return objects in the same order 
        as long as the tree's content does not change and the 
        implementation of `children` always returns the children in the 
        same order. If `children` is not implemented at all, 
        `NotImplementedError` will be raised. 
 
        """ 
        for obj in self._values: 
            yield obj 
        for child in self.children: 
            for obj in child: 
                yield obj 
 
    itervalues = __iter__ 
 
    def iternodes(self): 
        """ 
 
        A generator that yields all nodes in this subtree by doing 
        recursive pre-order traversal. Implementors might choose to use 
        another traversal method which better suits their data 
        structure. 
 
        Note that objects are returned unordered. 
 
        This implementation will always return nodes in the same order 
        as long as the tree's content does not change and the 
        implementation of `children` always returns the children in the 
        same order. If `children` is not implemented at all, 
        `NotImplementedError` will be raised. 
 
        """ 
        yield self 
        for child in self.children: 
            for node in child.iternodes(): 
                yield node 
 
    def __nonzero__(self): 
        """ 
 
        Return True if this node contains any objects. 
 
        """ 
        return len(self._values) > 0 
 
    def __len__(self): 
        """ 
 
        Return the number of objects in this subtree 
 
        """ 
        return self._size 
 
    def __contains__(self, item): 
        """ 
 
        Search for objects with a distance of zero to `item` and return 
        True if something is found, otherwise False. 
 
        Note that this does **not** check for object identity! Instead, 
        the definition of equality is delegated to the distance function 
        in use. 
 
        """ 
        return len(self.range_search(item)) > 0 
 
    def __repr__(self): 
        if self: 
            return str(self.__class__) + ": " + str(self._values[0]) 
        else: 
            return "<empty node>" 
 
 
class BKTree(MetricTree): 
    """ 
 
    "Burkhard-Keller Trees" are unbalanced multiway trees and may grow 
    over time. They belong to the first general solutions to index 
    arbitrary metric spaces. 
 
    Every node in a BKTree stores a list of objects which all have a 
    distance of zero to each other, i.e. all objects are considered to 
    be equal by the distance function in use.  Additionally, every node 
    keeps a dictionary. In this dictionary, every child is stored, 
    referenceable by its distance to its parent. 
 
    Essentially, every node in a BKTree divides its data set ``S`` into 
    subsets ``S^i`` so that every element in ``S^i`` has the distance 
    ``i`` to one object arbitrarily picked from ``S`` (and stored in 
    this node).  For each ``S^i``, a new child node is created and its 
    parent keeps a reference to this child together with its distance. 
 
    Insertion of a single object ``o`` in a node ``n`` is quite easy: 
 
    1. If ``n`` is empty, store ``o`` in ``n``. That's it. 
 
    2. Otherwise, calculate its distance to ``o``. 
 
    3. If the distance is zero, append this object to the list of 
       objects in this node and return. 
 
    4. Otherwise, look for a child of ``n`` with the calculated distance 
       to ``n``. If there is such a child, go back to 1. with this child 
       being the new ``n``. 
 
    5. Otherwise, create a new node containing ``o`` and store it as a 
       child of ``n`` with it's calculated distance. 
 
    Searching is done recursively by first calculating the distance of 
    the query object to the current node and then using the triangle 
    inequality to determine which children may contain other search 
    results. 
 
    Runtime complexity for the construction phase is ``O(n log(n))``, 
    searching is ``O(n^a)`` where ``0 <= a <= 1``. Space requirement is 
    ``O(n)``. 
 
    This implementation is close to the original description of the 
    algorithm and can only handle discrete distances. If your distance 
    function returns floating point values, it will appear to work at 
    indexing time but will most probably be horribly slow when 
    searching. 
 
    """ 
 
    __slots__ = [ '_parent', '_values', '_size', '_func', '_height', 
            '_num_nodes', '_children' ] 
 
    def __init__(self, objects=None, func=None, parent=None): 
        self._children = {} 
        if callable(objects): 
            random.shuffle(list(objects())) 
        super(BKTree, self).__init__(objects, func, parent) 
 
    def construct(self, objects, func): 
        self._func = func 
        self._children = {} 
        for o in objects: 
            self.insert(o) 
        return self 
 
    def insert(self, obj): 
        if not self: 
            self._values.append(obj) 
            self._incr_size() 
            return self 
        node = self 
        while True: 
            distance = node._get_dist(obj) 
            if distance == 0: 
                node._values.append(obj) 
                node._incr_size() 
                break 
            child = node._children.get(distance, None) 
            if child is None: 
                child = BKTree([obj], node._func, node) 
                node._children[distance] = child 
                break 
            node = child 
        return self 
 
    def _get_child_candidates(self, distance, min_dist, max_dist): 
        assert( min_dist <= max_dist ) 
        return (child for dist, child in self._children.iteritems() 
                if distance - max_dist <= dist <= distance + max_dist) 
 
    def __children(self): 
        children = self._children 
        sorted_dists = sorted(children.keys()) 
        return [children[dist] for dist in sorted_dists] 
    children = property(__children) 
 
class FastBKTree(object): 
    """ 
 
    Simpler version of BKTree. The tree's content is kept in nested 
    dictionaries where a "node"'s value is simply stored at key -1 and 
    its children are stored using their distance to the value as the 
    key. Example: 
 
    self.root = { -1: 'ABC', 
                   0: { -1: 'ABC' } 
                   1: { -1: 'ABCD', 
                         1: { -1: 'ABCE' } 
                      } 
                   2: { -1: 'A', 
                         1: { -1: 'B', 
                               1: { -1: 'C' }  
                            } 
                      } 
                } 
 
    """ 
 
 
    def __init__(self, objects, metric): 
        self.root = None 
        self.metric = metric 
        self.size = 0 
        self.height = 0 
        self.num_nodes = 0 
        for o in objects: 
            self.insert(o) 
 
    def insert(self, obj): 
        global dist_ctr 
        #value_of = lambda node: node[-1] 
        #new_node = lambda obj: { -1: obj } 
        self.size += 1 
        if self.root is None: 
            self.root = { -1: obj } 
            return 
        node = self.root 
        while True: 
            distance = self.metric(node[-1], obj) 
            dist_ctr += 1 
            if distance in node: 
                node = node[distance] 
            else: 
                node[distance] = { -1: obj } 
                break 
 
    def range_search(self, obj, min_dist=0, max_dist=0): 
        global dist_ctr 
        candidates = [self.root] 
        result = [] 
        while candidates: 
            node = candidates.pop() 
            distance = self.metric(node[-1], obj) 
            dist_ctr += 1 
            if min_dist <= distance <= max_dist: 
                result.append(node[-1]) 
            candidates.extend( child for dist, child in node.iteritems() 
                if distance - max_dist <= dist <= distance + max_dist 
                    and dist != -1) 
        return result 
 
    def search(self, obj, max_dist): 
        return self.range_search(obj, min_dist=0, max_dist=max_dist) 
 
    def nn_search(self, obj, num=1): 
        if not self: return list() 
        global dist_ctr 
        neighbours = list() # list of (value, distance) tuples 
        candidates = [self.root] 
        def cmp_neighbours(a, b): return cmp(a[1], b[1]) 
        while candidates: 
            cand = candidates.pop() 
            distance =self.metric(node[-1], obj) 
            dist_ctr += 1 
            candidate_is_neighbour = any(1 for n in neighbours 
                    if distance < n[1]) 
            if candidate_is_neighbour or len(neighbours) < num: 
                neighbours.append(cand[-1]) 
                neighbours.sort(cmp_neighbours) 
            if len(neighbours) > num: 
                    neighbours = neighbours[:num] 
            elif len(neighbours) == num: 
                max_dist = max([n[1] for n in neighbours]) 
                candidates.extend( 
                    child for dist, child in node.iteritems() 
                    if distance - max_dist <= dist <= distance + max_dist 
                        and dist != -1) 
            else: 
                candidates.extend(child for child, dist in 
                        node.iteritems() if child != 1) 
        return neighbours 
 
 
    def __len__(self): 
        return self.size 
 
 
class VPTree(MetricTree): 
 
    """ 
 
    .. _Jeffrey K. Uhlmann: http://www.pnylab.com/pny/papers/vptree/vptree/ 
 
    .. _Peter Yianilos: http://www.intermemory.net/pny/papers/vptree/vptree.ps 
 
    A "Vantage Point Tree" is a static, balanced, binary tree which can 
    be used to index metric spaces with a non-discrete distance 
    function.  It has been independently described by both `Jeffrey K. 
    Uhlmann`_ (1991) and `Peter Yianilos`_ (1993). 
 
    Construction is done by picking one object (the "vantage point") 
    from the set of objects to index and then determining the distance 
    of all remaining objects to the vantage point. The median distance 
    is calculated and the set of remaining objects is split in two: 
    objects whose distance to the vantage point is smaller than the 
    median distance and the rest (objects whose distance to the vantage 
    point is larger than or equal to the median). Yianilos called this 
    process "ball decomposition". For both of the resulting sets new 
    child nodes, called "left" and "right", are created recursively. The 
    vantage point and the previously calculated median distance are 
    stored in the current node. 
 
    When searching a node, the distance between the current node's value 
    and the search object is calculated. If it is ``<= k`` (the given 
    maximum distance), this node's value is added to the list of search 
    results.  Searching proceeds recursively into the left subtree if 
    ``distance - k < median`` and into the right subtree if ``distance + 
    k >= median``. 
 
    Since the construction phase takes advantage of the median of all 
    distances, VPTrees do a fairly good job of balancing their subtrees. 
    Only the fact that you have to put all objects whose distance to the 
    vantage point equals the median distance always have to be put on 
    the same side makes VPTrees tend to hang to the side containing 
    these objects when using discrete distance functions. 
 
    Runtime complexity for the construction phase is ``O(n log(n))``, 
    searching is ``O(log(n))``. Space requirement is ``O(n)``. 
 
    """ 
 
    __slots__ = [ '_parent', '_values', '_size', '_func', '_height', 
            '_num_nodes', '_median', '_leftchild', '_rightchild' ] 
 
    def __init__(self, objects=None, func=None, parent=None): 
        self._median = None 
        self._leftchild = None 
        self._rightchild = None 
        super(VPTree, self).__init__(objects, func, parent) 
 
    def construct(self, objects, func): 
        self._func = func 
        if objects: 
            if self.is_root(): 
                # when building the root of the tree, we make sure `objects` 
                # is a shuffled list to improve VP picking and make 
                # decomposing easier. 
                objects = list(objects) 
                #random.shuffle(objects) 
            self._values = [self._pick_VP(objects)] 
            left, right = self._decompose(objects) 
            del objects # we don't need that list anymore so release it 
                        # before doing recursive calls 
            self._incr_size(len(self._values)) 
            if left: 
                self._leftchild = VPTree(left, func, self) 
            if right: 
                self._rightchild = VPTree(right, func, self) 
        return self 
 
    def _pick_VP(self, objects): 
        # this probably makes no sense whatsoever, simply pop()ing would 
        # do just as well, I guess. Need to think about good strategies. 
        if len(objects) > 15: 
            sample = objects[:5] 
            max_diff = -1 
            vp = None 
            for o in sample: 
                dists = [ self._func(other, o) for other in sample 
                          if other is not o] 
                diff = max(dists) - min(dists) 
                if diff > max_diff: 
                    max_diff, vp = diff, o 
            objects.remove(vp) 
            return vp 
        else: 
            return objects.pop() 
 
    def _decompose(self, objects): 
        """ 
 
        Perform the process called "ball decomposition" by Peter 
        Yianilos. 
 
        `objects` has to be an iterable that yields objects applicable 
        to the metric function in use. The return value is a tuple of 
        two lists: one list that contains all elements having a distance 
        smaller than the median distance to this node's value, the 
        second list contains all objects whose distance is equal to or 
        larger than the median distance of all given `objects` to this 
        node's value. 
 
        """ 
        dist_per_obj = list() 
        for obj in objects: 
            distance = self._get_dist(obj) 
            if distance == 0: 
                self._values.append(obj) 
            else: 
                dist_per_obj.append( (distance, obj) ) 
        if dist_per_obj: 
            self._median = VPTree.determine_median(zip(*dist_per_obj)[0]) 
            left  = [ obj for dist, obj in dist_per_obj 
                      if dist < self._median ] 
            right = [ obj for dist, obj in dist_per_obj  
                      if dist >= self._median ] 
        else: 
            left, right = None, None 
        return left, right 
 
    @staticmethod 
    def determine_median(numbers): 
        """ 
 
        Determine the median from a sequence of numbers (or anything 
        else that can be ``sorted()``). 
 
        This does not use an optimal ``O(n)`` algorithm but instead 
        relies on CPython's speed when sorting (``O(n log(n))``). 
 
        """ 
        return sorted(numbers)[ len(numbers) / 2  ] 
 
    def _get_child_candidates(self, distance, min_dist, max_dist): 
        if self._leftchild and distance - max_dist < self._median: 
            yield self._leftchild 
        if self._rightchild and distance + max_dist >= self._median: 
            yield self._rightchild 
 
    def __children(self): 
        return [child for child in (self._leftchild, self._rightchild) 
                if child] 
    children = property(__children) 
 
 
#class BSTree(object): 
# 
#    class Sector(object):  
#        """ 
# 
#        * _values contains objects with distance == 0 to each other 
# 
#        * _radius is the largest distance of all objects to this node's 
#          values. 
# 
#        * _child is a reference to a BSTree. 
# 
#        * _node is a reference to the BSTree this Sector belongs to. 
# 
#        """ 
# 
#        __slots__ = [ '_values', '_radius', '_child', '_node' ] 
# 
#        def __init__(self, node, *values): 
#            self._node = node 
#            self._values = list(values) 
# 
#        def insert(self, obj): 
#            if not self._values: 
#                self._values = [obj] 
#                return self._node 
#            else: 
#                distance = MetricTree._get_dist(self, obj) 
#                self._radius = max(self._radius, distance) 
#                return self._child.insert(obj) 
# 
#        def __contains__(self, obj): 
#            return MetricTree.__contains__(self, obj) 
# 
# 
#    __slots__ = [ 
#            '_parent', '_size', '_func', '_height', '_num_nodes', 
#            '_left_sector', '_right_sector' 
#            ] 
# 
#    def __init__(self, objects=None, func=None, parent=None): 
#        self._left_sector = Sector() 
#        self._right_sector = Sector() 
#        super(BSTree, self).__init__(objects, func, parent) 
# 
#    def construct(self, objects, func): 
#        split = ([], []) 
#        if not self._left_values or not self._right_values: 
#            pass # TODO 
#        for obj in objects: 
#            to_left = this._func(self._left_values[0]) 
#            to_right = this._func(self._right_values[0]) 
# 
#    def decompose(self, objects): 
#        return objects.pop() 
# 
#    def pick_good_sector_values(self, objects): 
#        return objects.pop(), objects.pop() 
# 
#    def __nonzero__(self): 
#        pass 
# 
#    def __iter__(self): 
#        pass 
# 
#    def __repr__(self): 
#        pass 
 
class UnindexableObjectError(Exception): 
    """ 
 
    This Exception is thrown when the call to the distance function in 
    use by a metric space throws an exception. This should not happen 
    during regular usage and is a hint that either your distance 
    function is buggy or you tried to index objects which your distance 
    function cannot handle. 
 
    """ 
 
    def __init__(self, msg, e): 
        self.orig_exception = e 
        Exception.__init__(self, msg) 
 
    orig_exception = None 
    """ The exception that has triggered this exception.  """ 
 
    pass 
 
 
def levenshtein(x, y): 
    """ 
 
    Compute Levenshtein (or "edit") distance between two strings. 
    Levenshtein distance between two strings ``x`` and ``y`` is defined 
    as the minimal number of operations on single characters that it 
    takes to transform ``x`` into ``y`` (or vice versa). 
 
    Allowed operations are: 
 
    - Insertion, 
    - Deletion and 
    - Replacement 
 
    of a single character. 
 
    Levenshtein distance has all the properties of a strictly positive 
    metric. That means for all x, y, z it holds: 
 
    -  x == y <=> levenshtein(x, y) == 0 
    -  x != y <=> levenshtein(x, y) > 0 (positivity) 
    -  levenshtein(x, y) == levenshtein(y, x) (symmetry) 
    -  levenshtein(x, z) <= levenshtein(x, y) + levenshtein(y, z) 
 
    The upper bound for Levenshtein distance is the length of the longer 
    string: ``max(len(x), len(y))``. A general lower bound is 
    ``abs(len(x) - len(y))``. This is the case where one string is the 
    pre-/postfix of the other one. 
 
    Incidentally, this implementation not only works for strings, but 
    for all types of sequences. Objects in the given sequences are 
    compared for equality using '==' to determine whether an edit 
    operation is needed. 
 
    """ 
    if x == y:  
        return 0           # equal strings have distance zero 
    m, n = len(x), len(y) 
    if not (m and n):      # if one of the lengths is zero, 
        return m or n      # we can return the other one. 
    if n > m: 
        x, y = y, x        # switch m and n so that n 
        m, n = n, m        # is the smaller one (saves space for cur and prev) 
    cur = range(n+1) 
    prev = [0] * (n+1) 
    for i, char_x in enumerate(x): 
        prev[0] = i+1 
        for j, char_y in enumerate(y): 
            if char_x == char_y: 
                prev[j+1] = cur[j] 
            else: 
                prev[j+1] = min(prev[j], cur[j], cur[j+1]) + 1 
        cur, prev = prev, cur 
    return cur[-1] 
 
def tokenizer(textfile, separator=None): 
    """ 
 
    Simple generator that tokenizes sequences of strings (or file-like 
    objects) into uppercase words using the optional `separator`.  This 
    `separator` is passed directly to str.split so ``split``'s behaviour 
    concerning `None` as separator applies here as well. 
 
    After the last token has been returned, there is an attempt to close 
    `textfile`. If this yields an `AttributeError`, it will be silently 
    ignored. 
 
    """ 
    for line in textfile: 
        for token in line.split(separator): 
            yield token.upper() 
    try: 
        textfile.close() 
    except AttributeError, e: 
        pass 
 
dist_ctr = 0 
 
try: 
    import psyco 
    psyco.bind(levenshtein) 
    psyco.bind(VPTree) 
    psyco.bind(BKTree) 
    psyco.bind(FastBKTree) 
except ImportError, e: 
    sys.stderr.write("Psyco not available, proceeding without it.\n") 
 
if __name__ == '__main__': 
    import codecs, time, pdb
    dumpfilename = "vptree.dump" 
    #f = codecs.open(sys.argv[1], encoding="iso-8859-1") 
#     f = codecs.open('samples.txt', encoding="iso-8859-1")
#     names = tokenizer(f) 

    names = ['objects', 'object', 'objetc']
    
    t = BKTree() 
    t.construct(names, levenshtein) 
#     f.close() 
    print type(t) 
    s = raw_input("press enter") 
    print "t height: %s" % t.height 
    print "t size: %s" % len(t) 
    print "t nodes %s" % t.num_nodes 
 
    #print "results: %s " % t.search("MARTIN", 1) 
 
    #f = codecs.open(sys.argv[1], encoding="iso-8859-1")
#     f = codecs.open('samples.txt', encoding="iso-8859-1")
#     names = list(tokenizer(f))
    random.shuffle(names) 
    
    pdb.set_trace()
    
    start = time.time() 
    while names:
        t.search(names.pop(), 1) 
    end = time.time() 
    print end - start