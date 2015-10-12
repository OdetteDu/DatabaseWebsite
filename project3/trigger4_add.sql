-- description: <This trigger will update the number of bids according the number of bids in the database>

PRAGMA foreign_keys = ON;

drop trigger if exists UpdateNumberBidsWhenAddBid;
create trigger UpdateNumberBidsWhenAddBid
after insert on Bid
begin
update Auction
set NumberOfBids = (
						select count(b.AuctionID)
						from Bid as b
						where b.AuctionID = new.AuctionID
					)
where AuctionID = new.AuctionID;
end;
