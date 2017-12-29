import kirkpatrick
# main goes here

from kirkpatrick import simplices as S

t1 = S.Triangle([S.Point(-1, 0), S.Point(0, 2), S.Point(1, 0)])
print(t1.contains(S.Point(-1, -1)))
