%node(name,color)
%edge(s1,s2,color)
%line(color)

hasNodes(C,N) :- line(C), node(N,C).
e(S1,S2) :- edge(S1,S2,C).
e(S2,S1) :- e(S1,S2).

sp((N, N'))  :- shortestPath(T), station(T-1,N), station(T-1,N'), N<N'.
0 { selected((N, N'),S1,S2); selected((N, N'),S2,S1) } 1 :- edge(S1,S2,C), sp((N, N')).
path((N, N'),A,B)             :- selected((N, N'),A,B).
path((N, N'),X,Z)             :- path((N, N'),X,Y), path((N, N'),Y,Z).
:- sp((N, N')), not path((N, N'), N, N').

cost((N, N'), C) :- C = #count { X,Y : selected((N, N'),X,Y) }, sp((N, N')).
#minimize { C,N,N' : cost((N, N'), C) }.

hops(N,0)       :- withinHops(T, X), station(T-1,N).
hops(N,1)       :- not hops(N,0), hops(S,0), e(S,N).
hops(N,2)       :- not hops(N,1), hops(S,1), e(S,N).

minHops(N,V) :- V = #min{ X: hops(N,X) }, node(N,C), withinHops(_,_).
countedWithinHops(T+1, C-1)     :-    withinHops(T, X), 
                                    C = #count{N,V: minHops(N,V), V <= X}.

countedNodes(T+1, C-1)        :- countNodesBetween(T), sp((N, N')), cost((N,N'), C).
countedNodes(T+1, C-1)        :- countNodesBetween(T), spa((N, N'), _), cost((N,N'), C).

p((N,N'))   :- paths(T), station(T-1,N), station(T-1,N'), N<N'.

sp((N,N))   :- cycle(T), station(T-1,N).
cycleAns(T+1,true)  :- cycle(T), path((N,N), N,N).

sp((N,N'))  :- adjacent(T), station(T-1,N), station(T-1,N'), N<N'.
adjacentAns(T+1, true)  :- adjacent(T), cost(_,C), C=1.
adjacentAns(T+1, false) :- adjacent(T), not adjacentAns(T+1, true).

adjacentArchAns(T+1,N') :- adjacentArch(T, X), station(T-1,N), e(N,N').
adjacentToAns(T+1,X)    :- adjacentTo(T), station(T-1,N), station(T-1,N'), N<N', e(N,X), e(N',X).

start(S1)   :- p((S1,S2)).
finish(S2)  :- p((S1,S2)).
{ in(X,Y) : e(X,Y) }.
:- in(X,Y), in(Z,Y), X != Z.
:- in(X,Y), in(X,Z), Y != Z.
:- start(Y), in(_,Y).
:- finish(X), in(X,_).
reach(X) :- start(X), in(X,_).
reach(Y) :- in(X,Y), reach(X).
:- finish(X), not reach(X).
:- in(X,Y), not reach(X).
:- in(X,Y), not reach(Y).

sameLineAns(T+1,true)   :-  sameLine(T), station(T-1,N), station(T-1,N'), 
                            hasNodes(L,N), hasNodes(L,N'), N<N'.
sameLineAns(T+1,false)  :-  sameLine(T), not sameLineAns(T+1,true).

sp((N,N'))  :- commonStation(T), station(T-1,N), station(T-1,N'), N<N'.
commonStationAns(T+1, true)     :- commonStation(T), cost((N,N'), C), C = 2.
commonStationAns(T+1, false)    :- commonStation(T), not commonStationAns(T+1, true).

lineOnAns(T+1,LN)   :- linesOnNames(T), station(T-1,N), hasNodes(LN,N).
lineOnAns(T+1,C)    :- linesOnCount(T), station(T-1,N), C=#count{LNAME : hasNodes(LNAME,N)}.

existAns(T+1,true)  :- exist(T), station(T-1,N), node(N,C).
existAns(T+1,false) :- exist(T), not existAns(T+1,true).

stationsAns(T+1, N) :- stations(T), line(T-1,LN), hasNodes(LN,N).

ans(V) :- end(T), countedNodes(T,V).
ans(V) :- end(T), countedWithinHops(T,V).
ans(V) :- end(T), cycleAns(T,V).
ans(V) :- end(T), adjacentAns(T,V).
ans(V) :- end(T), adjacentToAns(T,V).
ans(V) :- end(T), sameLineAns(T,V).
ans(V) :- end(T), commonStationAns(T,V).
ans(V) :- end(T), lineOnAns(T,V).
ans(V) :- end(T), existAns(T,V).
ans(V) :- end(T), adjacentArchAns(T,V).
ans(V) :- end(T), stationsAns(T,V).

#show ans/1.