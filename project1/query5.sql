select count(u.UserID)
from AuctionUser as u
where u.UserID in 
(
	select a.SellerID
	from Auction as a
)
and u.Rating > 1000;
