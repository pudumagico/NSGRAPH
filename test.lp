node(modernist,shabby,false,false,rocknroll,mccaords,small).
node(concrete,dirty,false,false,none,mcgudy,tiny).
node(victorian,shabby,true,false,swing,gluek,large).
node(concrete,ratinfested,true,true,electronic,schroalls,mediumsized).
edge(green,id828c2fcf861748c7acf4a87d27dc1fb7,greensceusk,schroalls,gluek).
edge(cyan,id5983b75b6d054b3f81f43bb1a0233217,cyanhydraav,mcgudy,schroalls).
edge(green,id828c2fcf861748c7acf4a87d27dc1fb7,greensceusk,gluek,mccaords).
line(70,green,false,id828c2fcf861748c7acf4a87d27dc1fb7,greensceusk).
line(80,cyan,true,id5983b75b6d054b3f81f43bb1a0233217,cyanhydraav).

end(3).count(3,2).withinHops(2,1, 2).station(1,0,schroalls). 

start(NAME) :- withinHops(T+1,T, S), station(T,ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
finish(Y) :- start(X), node(ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,Y,SIZE), X!=Y.

0 { selected(X,S1,S2); selected(X,S2,S1) } 1 :- edge(COLOR,LINEID,LINENAME,S1,S2) , finish(X).
path(X, A,B) :- selected(X,A,B).
path(A,X,Z) :- path(A, X,Y), path(A,Y,Z).
path (X,Y):- path(Y,X,Y).
:- start(X), finish(Y), not path(Y,X,Y).
dist(X, Y, C) :- C = #count { Y,A,B : selected(Y,A,B) }, start(X), finish(Y).
#minimize { X,Y,C : dist(X, Y, C) }.


station(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE) :- station(T,0,NAME), node(ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).


nearby(T+2,C) :- count(T+2,T+1), withinHops(T+1,T, S), C = #count{1,X,Y,D : dist(X,Y,D), D <= S} , start(X).
ans(V) :- end(T), nearby(T,V).

#show ans/1.
#show start/1.
#show finish/1.
#show dist/3.


sp(T+1, NAME, NAME') :- shortestPath(T+1,T), station(T,ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE) , station(T,ARCHITECTURE',CLEANLINESS',DISACCESS',RAIL',MUSIC',NAME',SIZE'), NAME<NAME'.
start(NAME):- sp(T, NAME, NAME').
finish(NAME'):- sp(T, NAME, NAME').

0 { selected(S1,S2); selected(S2,S1) } 1 :- edge(COLOR,LINEID,LINENAME,S1,S2), sp(T, NAME, NAME').
path(X,Y) :- selected(X,Y).
path(X,Z) :- path(X,Y), path(Y,Z).
:- start(X), finish(Y), not path(X,Y).
cost(T+1, C) :- count(T+1,T), C = #count { X,Y : selected(X,Y) }, sp(T,NAME,NAME').
#minimize { C : cost(T, C) }.

ans(V-1) :- end(T+1), cost(T,V).
