/*
	Initialize the table
*/
drop table Median
create table Median( Number int)

insert into MEDIAN values (1)
insert into MEDIAN values (2)
insert into MEDIAN values (3)
insert into MEDIAN values (4)
insert into MEDIAN values (6)
insert into MEDIAN values (8)
insert into MEDIAN values (9)
insert into MEDIAN values (12)
insert into MEDIAN values (15)

/* 
	This is the solution for 2 
	- I tried to create a new table with the index and the number
	- The index is gotten by count how many tuples has the value large than the number
	- Then I select the one which index is half of the number of Number plus 1
*/
select indexedNumber.Number
from (
	select count(m2.Number) as numberIndex, m1.Number
	from Median as m1, Median as m2
	where m1.Number >= m2.Number
	group by m1.Number
	) as indexedNumber
where indexedNumber.numberIndex = ((select count(m.Number) as total
									from Median as m)/2 + 1)