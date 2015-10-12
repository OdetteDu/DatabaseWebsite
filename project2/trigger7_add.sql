-- description: <This trigger will check if the bid time matches the current time>

PRAGMA foreign_keys = ON;

drop trigger if exists BidTimeMatch;
create trigger BidTimeMatch
before insert on Bid
when ( new.Time <> 
		(
			select *
			from CurrentTime
		) 
	)
begin
	select raise(rollback, 'The bid time does not match the current time');
end;
