create table AuctionUser(UserID text PRIMARY KEY, Rating int NOT NULL, Location text, Country text);
create table Item(ItemID int PRIMARY KEY, Name text, Description text);
create table Classification(Category text, ItemID int, foreign key(ItemID) references Item(ItemID), primary key(Category, ItemID));
create table Auction(AuctionID int PRIMARY KEY, ItemID int, SellerID text, TimeStart text, TimeEnd text, BuyPrice real, FirstBid real, Currently real, NumberOfBids int, foreign key(ItemID) references Item(ItemID), foreign key(SellerID) references AuctionUser(UserID));
create table Bid(AuctionID int, BidderID text, Time text, Amount real, foreign key(AuctionID) references Auction(AuctionID), foreign key(BidderID) references AuctionUser(UserID), primary key(AuctionID, BidderID, Time));


