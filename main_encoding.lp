% Show only ans atom
#show ans/1.
% #show cost/2.
% #show selected/2.
% #show start/1.
% #show end/1.
% #show sp/3.
% #show path/2.
% #show edge/5.
% #show station/8
% #show counted/2.
% #show cleanliness/3.
% #show countIfEqual/3.
% #show counted/2.
% #show architecture/2.

%Can you get rail connections at Schwoold?
%end(2).pick_has_rail(2,1).station(1,0,schwoold).
station(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE) :- station(T,0,NAME), node(ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
has_rail(T+1, RAIL) :- pick_has_rail(T+1,T), station(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
ans(V) :- end(T), has_rail(T,V).

%How many architectural styles does Red Skeary pass through?
%end(7).count(7,6).unique(6,5).pluck_architecture(5,4).nodes(4,3).filter_line_id(3,2).allEdges(2,1).pick_id(2,1).line(1,0,redskeary).

line(T, BUILT,COLOR,AIRCON,ID,NAME) :- line(T,0,NAME), line(BUILT,COLOR,AIRCON,ID,NAME).
id(T+1,ID) :- pick_id(T+1,T), line(T, BUILT,COLOR,AIRCON,ID,NAME).
edge(T+1, COLOR,LINEID,LINENAME,STATION1,STATION2) :- allEdges(T+1,T), edge(COLOR,LINEID,LINENAME,STATION1,STATION2).
edge(T+1, COLOR,ID,LINENAME,STATION1,STATION2) :- filter_line_id(T+1,T), id(T,ID), edge(T,COLOR,ID,LINENAME,STATION1,STATION2).
node(T+1, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,STATION1,SIZE) :- nodes(T+1,T), edge(T, COLOR,ID,LINENAME,STATION1,STATION2), node(ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,STATION1,SIZE).
node(T+1, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,STATION2,SIZE) :- nodes(T+1,T), edge(T, COLOR,ID,LINENAME,STATION1,STATION2), node(ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,STATION2,SIZE).
architecture(T+1, NAME, ARCHITECTURE) :- pluck_architecture(T+1,T), node(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
uniqued(T+1, ARCHITECTURE) :- unique(T+1,T), architecture(T, NAME, ARCHITECTURE).
counted(T+1,C) :- count(T+1,T), C=#count{1,VAL: uniqued(T, VAL)}.
ans(V) :- end(T), counted(T,V).


%How many music styles does Red Skeary pass through?
%end(7).count(7,6).unique(6,5).pluck_music(5,4).nodes(4,3).filter_line_id(3,2).allEdges(2,1).pick_id(2,1).line(1,0,redskeary).
music(T+1, NAME, MUSIC) :- pluck_music(T+1,T), node(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
uniqued(T+1, MUSIC) :- unique(T+1,T), music(T, NAME, MUSIC).

%How many sizes of station does Pink Slaends pass through?
%end(7).count(7,6).unique(6,5).pluck_size(5,4).nodes(4,3).filter_line_id(3,2).allEdges(2,1).pick_id(2,1).line(1,0,pinkslaends).

size(T+1, NAME, SIZE) :- pluck_size(T+1,T), node(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
uniqued(T+1, SIZE) :- unique(T+1,T), size(T, NAME, SIZE).


% How many stations playing swing does Pink Slaends pass through?
% end(6).countIfEqual(6, 5, swing).pluck_music(5,4).nodes(4,3).filter_line_id(3,2).allEdges(2,1).pick_id(2,1).line(1,0,pinkslaends).

counted(T+1, C) :- countIfEqual(T+1, T, MUSIC), C = #count{1,NAME,MUSIC: music(T, NAME, MUSIC)}.

%How many derilict stations does Pink Slaends pass through?
%end(6).countIfEqual(6, 5, derilict).pluck_cleanliness(5,4).nodes(4,3).filter_line_id(3,2).allEdges(2,1).pick_id(2,1).line(1,0,pinkslaends).

% clean(T+1, NAME, CLEANLINESS) :- pluck_cleanliness(T+1,T), node(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
% counted(T+1, C) :- countIfEqual(T+1, T, CLEANLINESS), C = #count{1,NAME,CLEANLINESS: clean(T, NAME, CLEANLINESS)}.

%How many small stations does Pink Slaends pass through?
%end(6).countIfEqual(6, 5, small).pluck_size(5,4).nodes(4,3).filter_line_id(3,2).allEdges(2,1).pick_id(2,1).line(1,0,pinkslaends).

size(T+1, NAME, SIZE) :- pluck_size(T+1,T), node(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
counted(T+1, C) :- countIfEqual(T+1, T, SIZE), C = #count{1,NAME,SIZE: size(T, NAME, SIZE)}.

%How many stations with disabled access does Red Skeary pass through?
%end(6).countIfEqual(6, 5, true).pluck_disabled_access(5,4).nodes(4,3).filter_line_id(3,2).allEdges(2,1).pick_id(2,1).line(1,0,redskeary).

disaccess(T+1, NAME, DISACCESS) :- pluck_disabled_access(T+1,T), node(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
counted(T+1, C) :- countIfEqual(T+1, T, DISACCESS), C = #count{1,NAME,DISACCESS: disaccess(T, NAME, DISACCESS)}.

%How many stations with rail connections does Red Skeary pass through?
%end(6).countIfEqual(6, 5, true).pluck_has_rail(5,4).nodes(4,3).filter_line_id(3,2).allEdges(2,1).pick_id(2,1).line(1,0,redskeary).

rail(T+1, NAME, RAIL) :- pluck_has_rail(T+1,T), node(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
counted(T+1, C) :- countIfEqual(T+1, T, RAIL), C = #count{1,NAME,RAIL: rail(T, NAME, RAIL)}.

%0 How clean is Kriits?
%end(2).pick_cleanliness(2,1).station(1,0,kriits).

cleanliness(T+1, CLEANLINESS) :- pick_cleanliness(T+1,T), station(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
ans(V) :- end(T), cleanliness(T,V).

%How big is Kriits?
%end(2).pick_size(2,1).station(1,0,kriits).

size(T+1, SIZE) :- pick_size(T+1,T), station(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
ans(V) :- end(T), size(T,V).

%What music plays at Kriits?
%end(2).pick_music(2,1).station(1,0,kriits).

music(T+1, MUSIC) :- pick_music(T+1,T), station(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
ans(V) :- end(T), music(T,V).

%What architectural style is Scuys?
%end(2).pick_architecture(2,1).station(1,0,scuys).

architecture(T+1, ARCHITECTURE) :- pick_architecture(T+1,T), station(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
ans(V) :- end(T), architecture(T,V).

%Does Ghoow have disabled access?
%end(2).pick_disabled_access(2,1).station(1,0,ghoow).

disaccess(T+1, DISACCESS) :- pick_disabled_access(T+1,T), station(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
ans(V) :- end(T), disaccess(T,V).

% How many rat-infested stations does Green Sceusk pass through?
% end(6).countIfEqual(6, 5, rat-infested).pluck_cleanliness(5,4).nodes(4,3).filter_line_id(3,2).allEdges(2,1).pick_id(2,1).line(1,0,greensceusk).

cleanliness(T+1, NAME, CLEANLINESS) :- pluck_cleanliness(T+1,T), node(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
counted(T+1, C) :- countIfEqual(T+1, T, CLEANLINESS), C = #count{CLEANLINESS,NAME: cleanliness(T, NAME, CLEANLINESS)}.


%How many stations are between Mccaords and Schroalls?
%end(4).count(3,2).shortestPath(2,1).station(1,0,mccaords).station(1,0,schroalls).

sp(T+1, NAME, NAME') :- shortestPath(T+1,T), station(T,ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE) , station(T,ARCHITECTURE',CLEANLINESS',DISACCESS',RAIL',MUSIC',NAME',SIZE'), NAME<NAME'.
start(NAME):- sp(T, NAME, NAME').
finish(NAME'):- sp(T, NAME, NAME').

0 { selected(S1,S2); selected(S2,S1) } 1 :- edge(COLOR,LINEID,LINENAME,S1,S2), sp(T, NAME, NAME').
path(X, A,B) :- selected(X,A,B).
path(A,X,Z) :- path(A, X,Y), path(A,Y,Z).
:- start(X), finish(Y), not path(Y,X,Y).
cost(T+1, C) :- count(T+1,T), C = #count { X,Y : selected(X,Y) }, sp(T,NAME,NAME').
#minimize { C : cost(T, C) }.

ans(V) :- end(T+1), cost(T,V).

%How many stations are on the shortest path between Mcgudy and Gluek avoiding clean stations?
%end(4).count(3,2).shortestPathOnlyUsing_cleanliness(2, 1, clean).station(1,0,mcgudy).station(1,0,gluek).

sp(T+1, NAME, NAME') :- shortestPathOnlyUsing_cleanliness(T+1,T, X), station(T,ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE) , station(T,ARCHITECTURE',CLEANLINESS',DISACCESS',RAIL',MUSIC',NAME',SIZE'), NAME<NAME'.
0 { selected(S1,S2); selected(S2,S1) } 1 :- edge(COLOR,LINEID,LINENAME,S1,S2), sp(T, NAME, NAME'), shortestPathOnlyUsing_cleanliness(T,T-1, X),  station(ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,S1,SIZE),  station(ARCHITECTURE',CLEANLINESS',DISACCESS',RAIL',MUSIC',S2,SIZE'), CLEANLINESS!=X, CLEANLINESS'!=X.

%How many other stations are two stops or closer to Schroalls?
%end(3).count(3,2).withinHops(2,1, 2).station(1,0,schroalls).

start(NAME) :- withinHops(T+1,T, S), station(T,ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
finish(Y) :- start(X), node(ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,Y,SIZE), X!=Y.

0 { selected(X,S1,S2); selected(X,S2,S1) } 1 :- edge(COLOR,LINEID,LINENAME,S1,S2) , finish(X).
path(X, A,B) :- selected(X,A,B).
path(A,X,Z) :- path(A, X,Y), path(A,Y,Z).
path (X,Y) :- path(Y,X,Y).
:- start(X), finish(Y), not path(Y,X,Y).
dist(X, Y, C) :- C = #count { Y,A,B : selected(Y,A,B) }, start(X), finish(Y).
#minimize { X,Y,C : dist(X, Y, C) }.

nearby(T+2,C) :- count(T+2,T+1), withinHops(T+1,T, S), C = #count{1,X,Y,D : dist(X,Y,D), D <= S} , start(X).
ans(V) :- end(T), nearby(T,V).

#show dist/3.
% % Scene rule
% obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- scene(T,0), obj(0,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).

% % Uniqueness rule/constraint
% obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- unique(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).
% :- unique(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(T',ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2'), ID!=ID'.

% % Spatial relation rules
% obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- relate_left(T,T'), obj(0,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(T',ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2'), ID!=ID', X1<X1'.
% obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- relate_right(T,T'), obj(0,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(T',ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2'), ID!=ID', X1>=X1'.
% obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- relate_front(T,T'), obj(0,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(T',ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2'), ID!=ID', Y2>Y2'.
% obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- relate_behind(T,T'), obj(0,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(T',ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2'), ID!=ID', Y2<=Y2'.

% % Count rule
% int(T,V) :- count(T,T'), #count {ID:obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2)}=V.

% % Exist rule
% bool(T,true) :- exist(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).
% bool(T,false) :- exist(T,T'), not bool(T,true).

% % Filtering rules
% obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_large(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), SIZE=large.
% obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_small(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), SIZE=small.
% obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_gray(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), COLOR=gray.
% obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_red(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), COLOR=red.
% obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_blue(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), COLOR=blue.
% obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_green(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), COLOR=green.
% obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_brown(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), COLOR=brown.
% obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_purple(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), COLOR=purple.
% obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_cyan(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), COLOR=cyan.
% obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_yellow(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), COLOR=yellow.
% obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_metal(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), MATERIAL=metal.
% obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_rubber(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), MATERIAL=rubber.
% obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_sphere(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), SHAPE=sphere.
% obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_cylinder(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), SHAPE=cylinder.
% obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_cube(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), SHAPE=cube.

% % Query functions
% size(T,SIZE) :- query_size(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).
% color(T,COLOR) :- query_color(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).
% material(T,MATERIAL) :- query_material(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).
% shape(T,SHAPE) :- query_shape(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).

% % Logical operators
% obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- and(T,T',T''), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(T'',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).

% {or(T,T');or(T,T'')}=2 :- or(T,T',T'').
% obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- or(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).

% % Same-attribute relations
% obj(T+1,ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2') :- same_size(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(0,ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2'), ID!=ID', SIZE=SIZE'.
% obj(T+1,ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2') :- same_color(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(0,ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2'), ID!=ID', COLOR=COLOR'.
% obj(T+1,ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2') :- same_material(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(0,ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2'), ID!=ID', MATERIAL=MATERIAL'.
% obj(T+1,ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2') :- same_shape(T,T'), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(0,ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2'), ID!=ID', SHAPE=SHAPE'.

% % Integer comparison
% bool(T,true) :- equal_integer(T,T',T''), int(T',V'), int(T'',V''), V'=V''.
% bool(T,false) :- equal_integer(T,T',T''), not bool(T,true).

% bool(T,true) :- less_than(T,T',T''), int(T',V'), int(T'',V''), V'<V''.
% bool(T,false) :- less_than(T,T',T''), not bool(T,true).

% bool(T,true) :- greater_than(T,T',T''), int(T',V'), int(T'',V''), V'>V''.
% bool(T,false) :- greater_than(T,T',T''), not bool(T,true).

% % Attribute comparison
% bool(T,true) :- equal_size(T,T',T''), size(T',V'), size(T'',V''), V'=V''.
% bool(T,false) :- equal_size(T,T',T''), not bool(T,true).

% bool(T,true) :- equal_color(T,T',T''), color(T',V'), color(T'',V''), V'=V''.
% bool(T,false) :- equal_color(T,T',T''), not bool(T,true).

% bool(T,true) :- equal_material(T,T',T''), material(T',V'), material(T'',V''), V'=V''.
% bool(T,false) :- equal_material(T,T',T''), not bool(T,true).

% bool(T,true) :- equal_shape(T,T',T''), shape(T',V'), shape(T'',V''), V'=V''.
% bool(T,false) :- equal_shape(T,T',T''), not bool(T,true).

% % Derive answer (T must equal the last point in time)
% ans(V) :- end(T), size(T,V).
% ans(V) :- end(T), color(T,V).
% ans(V) :- end(T), material(T,V).
% ans(V) :- end(T), shape(T,V).
% ans(V) :- end(T), bool(T,V).
% ans(V) :- end(T), int(T,V).

% :- not ans(_).

% obj(0,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- label(0,img,ID,obj(ID,SHAPE,SIZE,COLOR,MATERIAL,X1,Y1,X2,Y2)).