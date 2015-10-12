select count(r.Category)
from
(
select c.Category 
from Auction as a, Classification as c
where a.ItemID = c.ItemID and a.AuctionID in
(
	select b.AuctionID
	from Bid as b
	where b.Amount > 100
)
group by c.Category
) as r;
