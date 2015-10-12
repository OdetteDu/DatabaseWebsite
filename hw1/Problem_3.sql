/*
	Initialize the table
*/
drop table Parent
create table Parent(P int, C int)

insert into PARENT values (1,2)
insert into PARENT values (1,3)
insert into PARENT values (1,4)
insert into PARENT values (2,5)
insert into PARENT values (2,6)
insert into PARENT values (2,7)
insert into PARENT values (2,8)
insert into PARENT values (2,9)
insert into PARENT values (3,10)
insert into PARENT values (3,11)
insert into PARENT values (4,12)
insert into PARENT values (4,13)
insert into PARENT values (5,14)
insert into PARENT values (6,15)
insert into PARENT values (6,16)
insert into PARENT values (6,17)
insert into PARENT values (6,18)
insert into PARENT values (7,19)
insert into PARENT values (7,20)
insert into PARENT values (7,21)
insert into PARENT values (8,22)
insert into PARENT values (14,23)
insert into PARENT values (14,24)
insert into PARENT values (15,25)
insert into PARENT values (16,26)
insert into PARENT values (16,27)
insert into PARENT values (14,23)
insert into PARENT values (14,24)
insert into PARENT values (15,25)
insert into PARENT values (16,26)
insert into PARENT values (16,27)

/* 
	This is the solution for 3A 
	- Since the tree has max height of four, I think there are only three possible combination for x and y
	- one is y is x's father, the other is y is x's grandfather, the rest is y is x' great grandfather
	- thus, I unioned the three situation

	- x = 15 y = 6
*/
select * 
from
((select p.P, p.C
from Parent as p
where p.C = 15) 
union
(select p1.P, p2.C
from Parent as p1, Parent as p2
where p1.C = p2.P and p2.C = 15
)
union
(select p1.p, p3.C
from Parent as p1, Parent as p2, Parent as p3
where p1.C = p2.P and p2.c = p3.P and p3.C = 15
))
as result
where result.p = 6

/* 
	This is the solution for 3B
	- Because I know how to determine if a is descendent of b
	- And I know if a is b's father, then the pathLength is 1, grandfather: 2, greatgrandfather: 3
	- Thus, I am trying to find the intersection of x's father or grandfather or greatgrandfather, and y's father or grandfather or greatgrandfather
	- If the intersection is not empty, then there exist path between x and y
	- At last, I add the pathLength between x and the common ancestor, and y and the common ancestor to get the totalPathLength
	- Then, I take the shorest path length

	- x = 23 y = 24
*/
select MIN(r1.pathLength + r2.pathLength) as ShortestPathLength
from
(
(select 23 as P, 23 as C, 0 as pathLength)
union 
(select p.P, p.C, 1 as pathLength
from Parent as p
where p.C = 23) 
union
(select p1.P, p2.C, 2 as pathLength
from Parent as p1, Parent as p2
where p1.C = p2.P and p2.C = 23
)
union
(select p1.p, p3.C, 3 as pathLength
from Parent as p1, Parent as p2, Parent as p3
where p1.C = p2.P and p2.c = p3.P and p3.C = 23
))
as r1,
(
(select 24 as P, 24 as C, 0 as pathLength)
union
(select p.P, p.C, 1 as pathLength
from Parent as p
where p.C = 24) 
union
(select p1.P, p2.C, 2 as pathLength
from Parent as p1, Parent as p2
where p1.C = p2.P and p2.C = 24
)
union
(select p1.p, p3.C, 3 as pathLength
from Parent as p1, Parent as p2, Parent as p3
where p1.C = p2.P and p2.c = p3.P and p3.C = 24
))
as r2
where r1.P = r2.P
