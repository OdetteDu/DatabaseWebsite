-- description: <This trigger adjust the current price in the Auction table when there is a legal bid inserted into the Bid table with the bid's amount>

PRAGMA foreign_keys = ON;

drop trigger if exists AdjustCurrentPrice;
create trigger AdjustCurrentPrice
after insert on Bid
begin
update Auction
set Currently = new.Amount
where AuctionID = new.AuctionID;
end;
