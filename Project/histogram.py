from operator import itemgetter
from multiprocessing import Pool
import collections
from collections import OrderedDict
import statistics
from ceasar import hitchars,decypher

def find(c,ll):
    for i,l in enumerate(ll):
        if c in l:
            return i
    return -1

class histogram:
    def __init__ (self,ld,frac=False):
        if frac:
            self.stat = ld
            for d in self.stat:
                s = sum(d.values())
                for k in d:
                    d[ k ] = d[ k ]/s
        else:
            self.stat = ld

    def list(self):
        def f(d):
            return [ e[ 0 ] for e in sorted( d.items(), key = itemgetter( 1 ), reverse = True ) ]
        return [ f(d) for d in self.stat if d ]

    @staticmethod
    def compare(a,b): #Estimate shift.
        def dist(x,y,n):
            return ((hitchars[n].index(y) - hitchars[n].index(x)))%len(hitchars[n])
        def mode(l):
            return collections.Counter(l).most_common(1)[0]


        d = [dist(x,y,i) for i,ll in enumerate(zip(a,b)) for x,y in zip(ll[0],ll[1])]
        return mode(d)[0]

    @staticmethod
    def text(s,frac=False): # Create a histogram from a text.
        ld = [OrderedDict() for x in hitchars]
        for c in s:
            n = find(c,hitchars)
            if n>=0:
                ld[ n ][ c ] = ld[ n ].get( c, 0 ) + 1
        return histogram( ld, frac )

    @staticmethod
    def key(s,frac=False): # Create a histogram from a list of element and occurences.
        ld = [ OrderedDict() for x in hitchars ]
        for c,v in s:
            n = find(c,hitchars)
            if n>=0:
                ld[n][c] = float(v)
        return histogram(ld,frac)

    def __repr__(self,digits=3):
        return repr( [ { k : round( d[k], digits ) for k in d} for d in self.stat if d ] )

if __name__ == "__main__":
    with open("engelsk.dat") as f:
        eng = histogram.key(( filter( lambda s: len(s), x.split(" ")) for x in f ))

    with open("texts/engelsk.crypt") as f:
        s = f.read()

    t = histogram.text(s)
    decypher (histogram.compare(eng.list(),t.list()), s, f = "hello.txt" )
