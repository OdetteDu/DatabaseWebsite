/* Create the table T, and insert the values without violate the FD */
drop table if exists T;
create table T(A int, B int, C int, D int)

/* Problem 1a: Check the FD A->D satisfied*/
insert into T values (1, 1, 1, 1)
insert into T values (1, 2, 3, 1)
insert into T values (4, 6, 8, 10)

select *
from T as t
where exists (select * 
from T as tt
where t.A = tt.A and t.D <> tt.D)

/* Problem 1a: Check the FD A->D not satisfied */
insert into T values (1, 2, 3, 2)

select *
from T as t
where exists (select * 
from T as tt
where t.A = tt.A and t.D <> tt.D)

/* Problem 1b: Check A->B and B -> C satisfied*/
delete from T
where A = 1 and B = 1 and C=1 and D=1
insert into T values (2, 2, 3, 6)

select *
from T as t
where exists 
(
	select *
	from T as tt
	where (t.A = tt.A and (t.B <> tt.B or t.C <> tt.C)) or (t.A <> tt.A and t.B = tt.B and t.C <> tt.C)
)

/* Problem 1b: Check A->B and B -> C not satisfied*/
insert into T values (1, 3, 3, 6)
insert into T values (4, 2, 2, 6)

select *
from T as t
where exists 
(
	select *
	from T as tt
	where (t.A = tt.A and (t.B <> tt.B or t.C <> tt.C)) or (t.A <> tt.A and t.B = tt.B and t.C <> tt.C)
)

/* Problem 1c: Check AB ->> C satisfied */
delete from T
insert into T values (1, 2, 3, 1)
insert into T values (1, 2, 5, 2)
insert into T values (1, 2, 5, 1)
insert into T values (1, 2, 3, 2)

select *
from T as t1, T as t2
where t1.A = t2.A and t1.B = t2.B and (t1.C <> t2.C or t1.D <> t2.D) 
and not exists
(
select *
from T as t
where t.A = t1.A and t.B = t1.B and t.C = t1.C and t.D = t2.D
)

/* Problem 1c: Check AB ->> C not satisfied */
delete from T
insert into T values (1, 2, 3, 1)
insert into T values (1, 2, 5, 2)

select *
from T as t1, T as t2
where t1.A = t2.A and t1.B = t2.B and (t1.C <> t2.C or t1.D <> t2.D) 
and not exists
(
select *
from T as t
where t.A = t1.A and t.B = t1.B and t.C = t1.C and t.D = t2.D)

/* Problem 1d: Check inclusion dependency satisfied */
delete from T
insert into T values (1, 2, 3, 1)
insert into T values (1, 2, 5, 2)

drop table if exists U
create table U(D int, E int)
insert into U values (1, 6)
insert into U values (2, 8)

select *
from U as u
where not exists 
(
	select *
	from T as t
	where u.D = t.D
)

/* Problem 1d: Check inclusion dependency not satisfied */
insert into U values (3, 9)

select *
from U as u
where not exists 
(
	select *
	from T as t
	where u.D = t.D
)