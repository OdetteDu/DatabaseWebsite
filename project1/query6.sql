select count(u.UserID)
from AuctionUser as u
where u.UserID in
(
	select a.SellerID
	from Auction as a
) 
and u.UserID in
(
	select b.BidderID
	from Bid as b
);
