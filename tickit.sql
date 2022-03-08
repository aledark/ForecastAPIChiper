create table categories(
catid SMALLINT NOT NULL AUTO_INCREMENT,
catgroup VARCHAR(10),
catname VARCHAR(10),
catdesc VARCHAR(50),
PRIMARY KEY(catid)
);

create table users(
userid INT NOT NULL AUTO_INCREMENT,
username CHAR(8),
firstname VARCHAR(30),
lastname VARCHAR(30),
city VARCHAR(30),
state CHAR(2),
email VARCHAR(100),
phone CHAR(14),
likesports BOOLEAN,
likeconcerts BOOLEAN,
likejazz BOOLEAN,
likeclassical BOOLEAN,
likeopera BOOLEAN,
likerock BOOLEAN,
likevegas BOOLEAN,
likebroadway BOOLEAN,
likemusicals BOOLEAN,
PRIMARY KEY(userid)
);

create table venues(
venueid SMALLINT NOT NULL AUTO_INCREMENT,
venuename VARCHAR(100),
venuecity VARCHAR(30),
venuestate CHAR(2),
venueseats INT,
PRIMARY KEY(venueid)
);

create table dates(
dateid SMALLINT NOT NULL AUTO_INCREMENT,
caldate DATE NOT NULL,
day CHAR(3) NOT NULL,
week SMALLINT NOT NULL,
month CHAR(5) NOT NULL,
qtr CHAR(5) NOT NULL,
year SMALLINT NOT NULL,
holiday BOOLEAN DEFAULT 0,
PRIMARY KEY(dateid)
);

create table events(
eventid INT NOT NULL AUTO_INCREMENT,
venueid SMALLINT NOT NULL,
catid SMALLINT NOT NULL,
dateid SMALLINT NOT NULL,
eventname VARCHAR(100),
starttime TIMESTAMP WITHOUT TIME ZONE,
PRIMARY KEY(eventid),
FOREIGN KEY(venueid) REFERENCES venues(venueid),
FOREIGN KEY(catid) REFERENCES categories(catid)
FOREIGN KEY(dateid) REFERENCES dates(dateid)
);

create table listings(
listid INT NOT NULL AUTO_INCREMENT,
sellerid INT NOT NULL,
eventid INT NOT NULL,
dateid SMALLINT NOT NULL,
numtickets SMALLINT NOT NULL,
priceperticket NUMERIC,
totalprice NUMERIC,
listtime TIMESTAMP WITHOUT TIME ZONE,
PRIMARY KEY(listid),
FOREIGN KEY(sellerid) REFERENCES users(userid),
FOREIGN KEY(eventid) REFERENCES events(eventid)
FOREIGN KEY(dateid) REFERENCES dates(dateid)
);

create table sales(
salesid INT NOT NULL AUTO_INCREMENT,
listid INT NOT NULL,
sellerid INT NOT NULL,
buyerid INT NOT NULL,
eventid INT NOT NULL,
dateid SMALLINT NOT NULL,
qtysold SMALLINT NOT NULL,
pricepaid NUMERIC,
comission NUMERIC,
saletime TIMESTAMP WITHOUT TIME ZONE,
PRIMARY KEY(salesid),
FOREIGN KEY(listid) REFERENCES listings(listid),
FOREIGN KEY(sellerid) REFERENCES users(userid),
FOREIGN KEY(buyerid) REFERENCES users(userid),
FOREIGN KEY(eventid) REFERENCES events(eventid)
FOREIGN KEY(dateid) REFERENCES dates(dateid)
);
