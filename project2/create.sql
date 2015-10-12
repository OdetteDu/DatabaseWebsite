drop table if exists CurrentTime;
create table CurrentTime(currentTime text);
insert into CurrentTime values ('2001-12-20 00:00:01');
select *
from CurrentTime;

drop table if exists AuctionUser;
create table AuctionUser(UserID text PRIMARY KEY, Rating int NOT NULL, Location text, Country text);

drop table if exists Item;
create table Item(ItemID int PRIMARY KEY, Name text, Description text);

drop table if exists Classification;
create table Classification(Category text, ItemID int not null, foreign key(ItemID) references Item(ItemID), primary key(Category, ItemID));

drop table if exists Auction;
create table Auction(AuctionID int PRIMARY KEY, ItemID int, SellerID text, TimeStart text, TimeEnd text, BuyPrice real, FirstBid real, Currently real, NumberOfBids int, foreign key(ItemID) references Item(ItemID), foreign key(SellerID) references AuctionUser(UserID), check(TimeStart < TimeEnd));

drop table if exists Bid;
create table Bid(AuctionID int, BidderID text, Time text, Amount real, foreign key(AuctionID) references Auction(AuctionID), foreign key(BidderID) references AuctionUser(UserID), primary key(AuctionID, Time), unique(AuctionID, BidderID, Amount));




