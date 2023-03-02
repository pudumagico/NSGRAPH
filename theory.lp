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

% 15 end(3).countIfEqual(2,shabby).lineNodes(1).line(0,cyanszirry).

counted(T+1, C) :- countIfEqual(T,X), cleans(X), C = #count{S: station(T,S), hasClean(S,X)}.
counted(T+1, C) :- countIfEqual(T,X), sizes(X), C = #count{S: station(T,S), hasSize(S,X)}.

counted(T+1, C) :- countIfEqual(T,da), C = #count{S: station(T,S), hasDA(S,true)}.
counted(T+1, C) :- countIfEqual(T,ra), C = #count{S: station(T,S), hasRA(S,true)}.

sp((N, N'))  :- shortestPath(T), station(T-1,N), station(T-1,N'), N<N'.
sp((N, N'))  :- withinHops(T, X), station(T-1,N), node(A,C,D,R,M,N',S), N!=N'.
 
countedNodes(T+1, C-1)        :- countNodesBetween(T), sp((N, N')), cost((N,N'), C).
countedWithinHops(T+1, C)     :-    withinHops(T, X), 
                                    C = #count{1,(N,N'): cost((N, N'), V), sp((N,N')), V <= X}.

%21 end(2).paths(1).station(0,dynaiarry).station(0,pruomp).
p((N,N')) :- paths(T), station(T-1,N), station(T-1,N'), N<N'.

sp((N,N)):- cycle(T), station(T-1,N).
cycleAns(T+1,true) :- cycle(T), path((N,N), N,N).

sp((N,N')):- adjacent(T), station(T-1,N), station(T-1,N'), N<N'.
adjacentAns(T+1, true) :- adjacent(T), cost(_,C), C=1.
adjacentAns(T+1, false) :- adjacent(T), not adjacentAns(T+1, true).

sp((N,N')):- adjacentTo(T), station(T-1,N), station(T-1,N'), N<N'.
adjacentToAns(T+1, X) :- path((N,N'),N,X), path((N,N'),X,N'), adjacentTo(T), station(T-1,N), station(T-1,N'), N<N'.

0 { pselected((N, N'),S1,S2); pselected((N, N'),S2,S1) } 1 :- edge(C,LID,LNAME,S1,S2), p((N, N')).
path((N, N'),A,B)             :- pselected((N, N'),A,B).
path((N, N'),X,Z)             :- path((N, N'),X,Y), path((N, N'),Y,Z).
:- p((N, N')), not path((N, N'), N, N').
:- p((N, N')), path((N, N'), X, Z), path((N, N'), Y, Z), X!=Y.

0 { selected((N, N'),S1,S2); selected((N, N'),S2,S1) } 1 :- edge(C,LID,LNAME,S1,S2), sp((N, N')).
path((N, N'),A,B)             :- selected((N, N'),A,B).
path((N, N'),X,Z)             :- path((N, N'),X,Y), path((N, N'),Y,Z).
:- sp((N, N')), not path((N, N'), N, N').

cost((N, N'), C) :- C = #count { (N, N'),X,Y : selected((N, N'),X,Y)}, sp((N, N')).
% #minimize { C : cost((N, N'), C) }.

sumcost(S) :- S = #sum{ V,(N,N'): cost((N,N'),V)}, sp((N,N')).
#minimize { S : sumcost(S) }.

ans(V) :- end(T), attribute(T,V).
ans(V) :- end(T), counted(T,V).
ans(V) :- end(T), countedNodes(T,V).
ans(V) :- end(T), countedWithinHops(T,V).
ans(V) :- end(T), cycleAns(T,V).
ans(V) :- end(T), adjacentAns(T,V).
ans(V) :- end(T), adjacentToAns(T,V).

% #show p/1.
% #show path/3.
#show ans/1.