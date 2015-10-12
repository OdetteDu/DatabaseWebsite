select a.AuctionID
from Auction as a
where not exists 
(select *
	from Auction as aa
	where aa.Currently > a.Currently);
