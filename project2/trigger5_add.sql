-- description: <This trigger will check if the newly inserted bid amount is larger than all the existing bid amount of the same auction>

PRAGMA foreign_keys = ON;

drop trigger if exists BidHighestAmount;
create trigger BidHighestAmount
before insert on Bid
when ( new.Amount <= 
		(
			select max(b.Amount)
			from Bid as b
			where b.AuctionID = new.AuctionID
		) 
	)
begin
	select raise(rollback, 'The Bid Amount is not larger than the previous Amount!');
end;
