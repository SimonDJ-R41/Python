import sys
def srange( s, e = None, step = 1 ,sj=0, ej=0 ): # [s+sj;e+ej;step[
    r = range( ord( s ) + sj, ord( e ) + ej, step ) if e else range( 0, ord( s ) + sj, step )
    return [ chr( x ) for x in r ]

hitchars = [ srange( "a", "z", ej = 1 ), #[a;z+1[, Range of all lowercase characters
            srange( "A", "Z", ej = 1 ), #[A;Z+1[, Range of all uppercase characters
            ]

def cypher( n, s, tables = hitchars):
    def table(l):
        return { ord(x):y for x, y in
                    zip( l, #Original l (list).
                    l[ n: ] + l[ :n ] #Rotated l (list).
                )}
    def merge(l):
        i = iter( l ) # Greate iterator for l (list).
        z = next( i ).copy() # Get the first element from the iterator and copy it.
        for x in i: # Get the remaining elements.
            z.update( x ) # Update the copied element(z) with the remaining elements in the iterator
        return z
    s = s.translate( merge( ( table( l ) for l in tables ) ) )
    return s

def decypher( n, s, tables = hitchars):
    return cypher( -n, s, tables)

if __name__ == "__main__":
    import argparse,sys
    parser = argparse.ArgumentParser(description='Run a ceasar cypher.')
    parser.add_argument('key', metavar='N', type=int, help='The key for shifting the charaters')
    args = parser.parse_args()
    print(cypher(args.key,sys.stdin.read()))
