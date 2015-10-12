select count(r.ItemID)
from
(
select c.ItemID
from Classification as c
group by c.ItemID
having count(c.category) = 4) as r;
