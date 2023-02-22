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


arqs(A)     :- node(A,C,D,R,M,N,S).
cleans(C)   :- node(A,C,D,R,M,N,S).
dissas(D)   :- node(A,C,D,R,M,N,S).
rails(R)    :- node(A,C,D,R,M,N,S).
musics(M)   :- node(A,C,D,R,M,N,S).
sizes(S)    :- node(A,C,D,R,M,N,S).

station(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE) :- station(T,0,NAME), node(ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
line(T, BUILT,COLOR,AIRCON,ID,NAME)                                 :- line(T,0,NAME), line(BUILT,COLOR,AIRCON,ID,NAME).

architecture(T+1, ARCHITECTURE) :- pick_architecture(T+1,T), station(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
cleanliness(T+1, CLEANLINESS)   :- pick_cleanliness(T+1,T), station(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
disaccess(T+1, DISACCESS)       :- pick_disabled_access(T+1,T), station(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
has_rail(T+1, RAIL)             :- pick_has_rail(T+1,T), station(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
music(T+1, MUSIC)               :- pick_music(T+1,T), station(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
size(T+1, SIZE)                 :- pick_size(T+1,T), station(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
id(T+1,ID)                      :- pick_id(T+1,T), line(T, BUILT,COLOR,AIRCON,ID,NAME).


edge(T+1, COLOR,LINEID,LINENAME,NAME,NAME')  :-  edges(T+1,T), station(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE),
                                                        edge(COLOR,LINEID,LINENAME,NAME,NAME').
edge(T+1, COLOR,LINEID,LINENAME,NAME',NAME)  :-  edges(T+1,T), station(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE),
                                                        edge(COLOR,LINEID,LINENAME,NAME',NAME).


edge(T+1, COLOR,LINEID,LINENAME,STATION1,STATION2)  :- allEdges(T+1,T), edge(COLOR,LINEID,LINENAME,STATION1,STATION2).
edge(T+1, COLOR,ID,LINENAME,STATION1,STATION2)      :- filter_line_id(T+1,T), id(T,ID), edge(T,COLOR,ID,LINENAME,STATION1,STATION2).

node(T+1, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,STATION1,SIZE)  :- nodes(T+1,T), edge(T, COLOR,ID,LINENAME,STATION1,STATION2), 
                                                                        node(ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,STATION1,SIZE).
node(T+1, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,STATION2,SIZE)  :- nodes(T+1,T), edge(T, COLOR,ID,LINENAME,STATION1,STATION2), 
                                                                        node(ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,STATION2,SIZE).

architecture(T+1, NAME, ARCHITECTURE)   :- pluck_architecture(T+1,T), node(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
music(T+1, NAME, MUSIC)                 :- pluck_music(T+1,T), node(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
size(T+1, NAME, SIZE)                   :- pluck_size(T+1,T), node(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
disaccess(T+1, NAME, DISACCESS)         :- pluck_disabled_access(T+1,T), node(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
rail(T+1, NAME, RAIL)                   :- pluck_has_rail(T+1,T), node(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
cleanliness(T+1, NAME, CLEANLINESS)     :- pluck_cleanliness(T+1,T), node(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
                                            
                                        
linename(T+1, LINENAME)     :- pluck_line_name(T+1,T), edge(T,_,_,LINENAME,_,_).


uniqued(T+1, ARCHITECTURE)              :- unique(T+1,T), architecture(T, NAME, ARCHITECTURE).
uniqued(T+1, MUSIC)                     :- unique(T+1,T), music(T, NAME, MUSIC).
uniqued(T+1, SIZE)                      :- unique(T+1,T), size(T, NAME, SIZE).
uniqued(T+1, LINENAME)                  :- unique(T+1,T), linename(T, LINENAME).
uniqued(T+1, NODENAME)                  :- unique(T+1,T), node(T, ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NODENAME,SIZE).

counted(T+1, C) :- count(T+1,T), C = #count{VAL: uniqued(T, VAL)}.
counted(T+1, C) :- count(T+1,T), C = #count{1,(NAME,NAME'): cost(T+2, (NAME, NAME'), V), sp(T,(NAME,NAME')), V <= X}, withinHops(T,T-1, X).
% counted(T+1, C) :- count(T+1,T), C = #count{1,(NAME,NAME'): cost(T+2, (NAME, NAME'), V), sp(T,(NAME,NAME')), V <= X}, withinHops(T,T-1, X).

counted(T+1, C) :- countIfEqual(T+1, T, RAIL), rails(RAIL), C = #count{NAME,RAIL: rail(T, NAME, RAIL)}.
counted(T+1, C) :- countIfEqual(T+1, T, SIZE), sizes(SIZE), C = #count{NAME,SIZE: size(T, NAME, SIZE)}.
counted(T+1, C) :- countIfEqual(T+1, T, MUSIC), musics(MUSIC), C = #count{NAME,MUSIC: music(T, NAME, MUSIC)}.
counted(T+1, C) :- countIfEqual(T+1, T, CLEANLINESS), cleans(CLEANLINESS), C = #count{NAME,CLEANLINESS: cleanliness(T, NAME, CLEANLINESS)}.
counted(T+1, C) :- countIfEqual(T+1, T, DISACCESS), dissas(DISACCESS), C = #count{NAME,DISACCESS: disaccess(T, NAME, DISACCESS)}.


sp(T+1, (NAME, NAME'))      :-      shortestPath(T+1,T), station(T,ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE), 
                                station(T,ARCHITECTURE',CLEANLINESS',DISACCESS',RAIL',MUSIC',NAME',SIZE'), NAME<NAME'.

sp(T+1, (NAME, NAME'))    :-  shortestPathOnlyUsingcleanliness(T+1,T,C), 
                            station(T,ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE), 
                            station(T,ARCHITECTURE',CLEANLINESS',DISACCESS',RAIL',MUSIC',NAME',SIZE'), NAME<NAME'.

sp(T+1, (NAME, NAME'))    :-    withinHops(T+1,T, X),    station(T,ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE),
                                node(ARCHITECTURE',CLEANLINESS',DISACCESS',RAIL',MUSIC',NAME',SIZE'),
                                NAME!=NAME'.

%to be implemented
p(T+1, (NAME, NAME'))      :-   paths(T+1,T), station(T,ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE), 
                                station(T,ARCHITECTURE',CLEANLINESS',DISACCESS',RAIL',MUSIC',NAME',SIZE'), NAME<NAME'.


%cycle
sp(T+1, (NAME, NAME))      :-   cycle(T+1,T), station(T,ARCHITECTURE,CLEANLINESS,DISACCESS,RAIL,MUSIC,NAME,SIZE).
bool(T+1, true) :- cycle(T+1,T), path((NAME, NAME), NAME,NAME).
bool(T+1, false) :- cycle(T+1,T), not bool(T+1,true).

bool(T+1,true) :- equal(T+1,T, V), cost(T+1,(NAME,NAME'),C), C=V-1.
bool(T+1,false) :- equal(T+1,T, V), not bool(T+1,true).

0 { selected((NAME, NAME'),S1,S2); selected((NAME, NAME'),S2,S1) } 1 :- edge(COLOR,LINEID,LINENAME,S1,S2), sp(T, (NAME, NAME')).
path((NAME, NAME'),A,B)             :- selected((NAME, NAME'),A,B).
path((NAME, NAME'),X,Z)             :- path((NAME, NAME'),X,Y), path((NAME, NAME'),Y,Z).
:- sp(T, (NAME, NAME')), not path((NAME, NAME'), NAME, NAME').
cost(T+2, (NAME, NAME'), C) :- count(T+1,T), C = #count { (NAME, NAME'),X,Y : selected((NAME, NAME'),X,Y) }, sp(T,(NAME, NAME')).

sumcost(X) :- X = #sum{ V,(NAME,NAME'): cost(_,(NAME,NAME'),V), sp(_,(NAME,NAME')) }.
% #minimize { C : cost(T, (NAME, NAME'), C) }.
#minimize { X : sumcost(X) }.


% end(6).pluck_name(6,5).unique(5,4).nodes(4,3).filter_line_id(3,2).allEdges(2,1).pick_id(2,1).line(1,0,cyansynians).
edge(T+1, COLOR,LINEID,LINENAME,STATION1,STATION2)  :-  filter_line_id(T+1,T), 
                                                        edge(T, COLOR,LINEID,LINENAME,STATION1,STATION2), 
                                                        id(T,LINEID).  
uniqued(T+1,N)                        :-    pluck_name(T+1,T), uniqued(T,N).






#show cost/3.
% #show sumcost/1.
% #show counted/2.
% #show uniqued/2.
% #show edge/6.

ans(V) :- end(T), has_rail(T,V).
ans(V) :- end(T), disaccess(T,V).
ans(V) :- end(T), architecture(T,V).
ans(V) :- end(T), music(T,V).
ans(V) :- end(T), size(T,V).
ans(V) :- end(T), cleanliness(T,V).
ans(V) :- end(T), counted(T,V).
ans(V) :- end(T), uniqued(T,V).
ans(V) :- end(T), cost(T,(_,_),V).






















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