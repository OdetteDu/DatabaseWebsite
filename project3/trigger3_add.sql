-- description: <This trigger will check if the newly inserted bid's time is within the range of the auction>

PRAGMA foreign_keys = ON;

drop trigger if exists BidTimeWithinRange;
create trigger BidTimeWithinRange
before insert on Bid
when ( new.Time < (
		select a.TimeStart
		from Auction as a
		where a.AuctionID = new.AuctionID) or
		new.Time > (
			select a.TimeEnd
			from Auction as a
			where a.AuctionID = new.AuctionID)
	)
begin
	select raise(rollback, 'Bid time cannot be before the auction started, or after the auction ends!');
end;
