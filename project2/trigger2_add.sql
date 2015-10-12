-- description: <This trigger checks if a bid is inserted where the bidder sells the same item>

PRAGMA foreign_keys = ON;

drop trigger if exists BothSellerAndBidder;
create trigger BothSellerAndBidder
before insert on Bid
when ( new.BidderID in (
		select a.SellerID
		from Auction as a
		where a.AuctionID = new.AuctionID))
begin
	select raise(rollback, 'Can not bid on the item you are selling!');
end;
