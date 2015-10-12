/*
	Initialize the table
*/
drop table Temperature
create table Temperature(city varchar(50), state varchar(50), day int, temp int)

insert into Temperature values ('Stanford','CA',100,36)
insert into Temperature values ('Stanford','CA',101,38)
insert into Temperature values ('Stanford','CA',106,26)
insert into Temperature values ('Stanford','CA',1,3)
insert into Temperature values ('Stanford','CA',12,5)
insert into Temperature values ('Stanford','CA',12,5)
insert into Temperature values ('Stanford','CA',13,6)
insert into Temperature values ('Stanford','CA',14,8)
insert into Temperature values ('Stanford','CA',15,12)
insert into Temperature values ('Stanford','CA',16,3)
insert into Temperature values ('Stanford','CA',17,7)
insert into Temperature values ('New York','NY',12,8)
insert into Temperature values ('New York','NY',13,9)
insert into Temperature values ('New York','NY',14,2)
insert into Temperature values ('New York','NY',15,3)
insert into Temperature values ('New York','NY',16,5)
insert into Temperature values ('New York','NY',17,6)
insert into Temperature values ('Queens','NY',11,15)
insert into Temperature values ('Queens','NY',13,6)
insert into Temperature values ('Queens','NY',14,4)
insert into Temperature values ('Queens','NY',15,13)
insert into Temperature values ('Queens','NY',16,6)
insert into Temperature values ('Queens','NY',18,16)
insert into Temperature values ('Long Island','NY',111,25)
insert into Temperature values ('Long Island','NY',13,6)
insert into Temperature values ('Long Island','NY',114,24)
insert into Temperature values ('Long Island','NY',15,17)
insert into Temperature values ('Long Island','NY',16,11)
insert into Temperature values ('Long Island','NY',118,16)
insert into Temperature values ('Stanford','CA',16,3)
insert into Temperature values ('Palo Alto','CA',16,15)
insert into Temperature values ('Palo Alto','CA',16,15)
insert into Temperature values ('Berkeley','CA',26,28)

/* 
	This is the solution for 1A 
	- very simple solution, doesn't need comment
*/
select t.state, MIN(t.temp) as low, MAX(t.temp) as high, AVG(t.temp) as avg
from Temperature as t
group by t.state

/* 
	This is the solution for 1B 
	- First get the min temp for each city
	- Then get the max temp for the whole database
	- Then select the one within 30 degree
*/
select te.groupedCity
from (select t.city as groupedCity, MIN(t.temp) as minTemp
from Temperature as t
group by t.city) as te, (select MAX(t.temp) as maxTemp
from Temperature as t) as ma
where (maxTemp - te.minTemp) < 30 

/* 
	This is the solution for 1C 
	- The same as the previous problem
	- Except replace the Min and Max
	- Implement the Min and Max by ask the temp to less then or great then all other temp
*/
select distinct tempMin.city
from (select t.temp as maxTemp
		from Temperature as t
		where t.temp >= all(select te.temp
							from Temperature as te)) as tempMax, 
	  (select t.city, t.temp as minTemp
		from Temperature as t
		where t.temp <= all(select te.temp
							from Temperature as te
							where te.city = t.city)) as tempMin
where (tempMax.maxTemp - tempMin.minTemp) < 30 