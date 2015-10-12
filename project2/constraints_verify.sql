select *
from Classification as c
where not exists 
(
	select *
	from Item as i
	where c.ItemID = i.ItemID
);

select *
from Auction as a
where not exists
(
	select * 
	from Item as i
	where a.ItemID = i.ItemID
)
or not exists
(
	select *
	from AuctionUser as u
	where u.UserID = a.SellerID
);

select *
from Bid as b
where not exists
(
	select *
	from Auction as a
	where a.AuctionID = b.AuctionID
)
or not exists
(
	select *
	from AuctionUser as u
	where b.BidderID = u.UserID
);
