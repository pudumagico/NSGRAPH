archs(A)    :- node(A,C,D,R,M,N,S).
cleans(C)   :- node(A,C,D,R,M,N,S).
dissas(D)   :- node(A,C,D,R,M,N,S).
rails(R)    :- node(A,C,D,R,M,N,S).
musics(M)   :- node(A,C,D,R,M,N,S).
sizes(S)    :- node(A,C,D,R,M,N,S).

hasArch(N,A)    :- node(A,C,D,R,M,N,S).
hasClean(N,C)   :- node(A,C,D,R,M,N,S).
hasDA(N,D)      :- node(A,C,D,R,M,N,S).
hasRA(N,R)      :- node(A,C,D,R,M,N,S).
hasMusic(N,M)   :- node(A,C,D,R,M,N,S).
hasSize(N,S)    :- node(A,C,D,R,M,N,S).

hasNodes(N,S1) :- line(Y,C,AC,ID,N), edge(C,ID,N,S1,S2).
hasNodes(N,S2) :- line(Y,C,AC,ID,N), edge(C,ID,N,S1,S2).

e(S1,S2) :- edge(C,ID,N,S1,S2).
e(S2,S1) :- e(S1,S2).

attribute(T+1, A)   :- pickArch(T), station(T-1, N), hasArch(N, A).
attribute(T+1, C)   :- pickClean(T), station(T-1, N), hasClean(N, C).
attribute(T+1, D)   :- pickDA(T), station(T-1, N), hasDA(N, D).
attribute(T+1, R)   :- pickRA(T), station(T-1, N), hasRA(N, R).
attribute(T+1, M)   :- pickMusic(T), station(T-1, N), hasMusic(N, M).
attribute(T+1, S)   :- pickSize(T), station(T-1, N), hasSize(N, S).

attribute(T+1,ID)   :- pickID(T), line(T-1, BUILT,COLOR,AIRCON,ID,NAME).

station(T+1,S) :- lineNodes(T), line(T-1, N), hasNodes(N,S).

counted(T+2, C) :- count(T+1), pluckArch(T), C = #count{A: station(T,S), hasArch(S,A)}.
counted(T+2, C) :- count(T+1), pluckMusic(T), C = #count{M: station(T,S), hasMusic(S,M)}.
counted(T+2, C) :- count(T+1), pluckSize(T), C = #count{S': station(T,S), hasSize(S,S')}.

counted(T+1, C) :- countIfEqual(T,X), cleans(X), C = #count{S: station(T,S), hasClean(S,X)}.
counted(T+1, C) :- countIfEqual(T,X), sizes(X), C = #count{S: station(T,S), hasSize(S,X)}.
counted(T+1, C) :- countIfEqual(T,X), musics(X), C = #count{S: station(T,S), hasMusic(S,X)}.
counted(T+1, 0) :- countIfEqual(T,X), not counted(T+1, _).

counted(T+1, C) :- countIfEqual(T,da), C = #count{S: station(T,S), hasDA(S,true)}.
counted(T+1, C) :- countIfEqual(T,ra), C = #count{S: station(T,S), hasRA(S,true)}.

sp((N, N'))  :- shortestPath(T), station(T-1,N), station(T-1,N'), N<N'.
sp((N, N'))  :- shortestPathAvoid(T,X), station(T-1,N), station(T-1,N'), N<N'.

hops(N,0)       :- withinHops(T, X), station(T-1,N).
hops(N,1)       :- not hops(N,0), hops(S,0), e(S,N).
hops(N,2)       :- not hops(N,1), hops(S,1), e(S,N).

minHops(N,V) :- V = #min{ X: hops(N,X) }, node(A,C,D,R,M,N,S), withinHops(_,_).
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

0 { selected((N, N'),S1,S2); selected((N, N'),S2,S1) } 1 :- edge(C,LID,LNAME,S1,S2), sp((N, N')).
path((N, N'),A,B)             :- selected((N, N'),A,B).
path((N, N'),X,Z)             :- path((N, N'),X,Y), path((N, N'),Y,Z).
:- sp((N, N')), not path((N, N'), N, N').

cost((N, N'), C) :- C = #count { X,Y : selected((N, N'),X,Y) }, sp((N, N')).
#minimize { C,N,N' : cost((N, N'), C) }.

sameLineAns(T+1,true)   :-  sameLine(T), station(T-1,N), station(T-1,N'), 
                            hasNodes(L,N), hasNodes(L,N'), N<N'.
sameLineAns(T+1,false)  :-  sameLine(T), not sameLineAns(T+1,true).

sp((N,N'))  :- commonStation(T), station(T-1,N), station(T-1,N'), N<N'.
commonStationAns(T+1, true)     :- commonStation(T), cost((N,N'), C), C = 2.
commonStationAns(T+1, false)    :- commonStation(T), not commonStationAns(T+1, true).

closestArchAns(T+1,N)   :- closestArch(T, A), station(T-1,N), hasArch(N,A).
sp((N,N'))              :- not closestArchAns(T+1,_), closestArch(T, A), station(T-1,N), hasArch(N',A), N!=N'.
closestArchAnsSP(T+1,S)   :- closestArch(T,_), X = #min{ C,(N,N') : cost((N,N'), C)}, cost((N,S), X).

lineOnAns(T+1,LN)   :- linesOnNames(T), station(T-1,N), hasNodes(LN,N).
lineOnAns(T+1,C)    :- linesOnCount(T), station(T-1,N), C=#count{LNAME : hasNodes(LNAME,N)}.

existAns(T+1,true)  :- exist(T), station(T-1,N), node(A,C,D,R,M,N,S).
existAns(T+1,false) :- exist(T), not existAns(T+1,true).

archCount(N,V)          :- mostArch(T,A), V=#count{1,N,S : hasNodes(N,S), hasArch(S,A)}, line(Y,C,AC,ID,N).
archCountAns(T+1,N')    :- mostArch(T,A), Z=#min{V : archCount(N,V)}, archCount(N',V), V=Z.

stationsAns(T+1, N) :- stations(T), line(T-1,LN), hasNodes(LN,N).

ans(V) :- end(T), attribute(T,V).
ans(V) :- end(T), counted(T,V).
ans(V) :- end(T), countedNodes(T,V).
ans(V) :- end(T), countedWithinHops(T,V).
ans(V) :- end(T), cycleAns(T,V).
ans(V) :- end(T), adjacentAns(T,V).
ans(V) :- end(T), adjacentToAns(T,V).
ans(V) :- end(T), sameLineAns(T,V).
ans(V) :- end(T), commonStationAns(T,V).
ans(V) :- end(T), closestArchAns(T,V).
ans(V) :- end(T), closestArchAnsSP(T,V).
ans(V) :- end(T), lineOnAns(T,V).
ans(V) :- end(T), existAns(T,V).
ans(V) :- end(T), archCountAns(T,V).
ans(V) :- end(T), adjacentArchAns(T,V).
ans(V) :- end(T), stationsAns(T,V).

#show ans/1.