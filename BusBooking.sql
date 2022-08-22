create database BusBooking;
use BusBooking;
create table User(
Name varchar(50) default null,
Age int default 0,
Gender varchar(10) default null,
Email varchar(50) default null,
MobileNum varchar(10) primary key default null,
Password varchar(100) default null
);
create table BookStatus(
SeatNo varchar(3) primary key default null,
PassengerName varchar(50) default null,
PassengerAge int default null,
PassengerGender varchar(10) default null,
BookingStatus varchar(10) default 'unBooked',
TimeStamp datetime default current_timestamp,
No int default null,
Gen varchar(50) default 'Nothing'
);
INSERT INTO BookStatus (SeatNo,No) VALUES ('L1',1);
INSERT INTO BookStatus (SeatNo,No) VALUES ('L2',2);
INSERT INTO BookStatus (SeatNo,No) VALUES ('L3',3);
INSERT INTO BookStatus (SeatNo,No) VALUES ('L4',4);
INSERT INTO BookStatus (SeatNo,No) VALUES ('L5',5);
INSERT INTO BookStatus (SeatNo,No) VALUES ('L6',6);
INSERT INTO BookStatus (SeatNo,No) VALUES ('L7',7);
INSERT INTO BookStatus (SeatNo,No) VALUES ('L8',8);
INSERT INTO BookStatus (SeatNo,No) VALUES ('L9',9);
INSERT INTO BookStatus (SeatNo,No) VALUES ('L10',10);
INSERT INTO BookStatus (SeatNo,No) VALUES ('L11',11);
INSERT INTO BookStatus (SeatNo,No) VALUES ('L12',12);
INSERT INTO BookStatus (SeatNo,No) VALUES ('L13',13);
INSERT INTO BookStatus (SeatNo,No) VALUES ('L14',14);
INSERT INTO BookStatus (SeatNo,No) VALUES ('L15',15);
INSERT INTO BookStatus (SeatNo,No) VALUES ('L16',16);
INSERT INTO BookStatus (SeatNo,No) VALUES ('L17',17);
INSERT INTO BookStatus (SeatNo,No) VALUES ('L18',18);
INSERT INTO BookStatus (SeatNo,No) VALUES ('U1',19);
INSERT INTO BookStatus (SeatNo,No) VALUES ('U2',20);
INSERT INTO BookStatus (SeatNo,No) VALUES ('U3',21);
INSERT INTO BookStatus (SeatNo,No) VALUES ('U4',22);
INSERT INTO BookStatus (SeatNo,No) VALUES ('U5',23);
INSERT INTO BookStatus (SeatNo,No) VALUES ('U6',24);
INSERT INTO BookStatus (SeatNo,No) VALUES ('U7',25);
INSERT INTO BookStatus (SeatNo,No) VALUES ('U8',26);
INSERT INTO BookStatus (SeatNo,No) VALUES ('U9',27);
INSERT INTO BookStatus (SeatNo,No) VALUES ('U10',28);
INSERT INTO BookStatus (SeatNo,No) VALUES ('U11',29);
INSERT INTO BookStatus (SeatNo,No) VALUES ('U12',30);
INSERT INTO BookStatus (SeatNo,No) VALUES ('U13',31);
INSERT INTO BookStatus (SeatNo,No) VALUES ('U14',32);
INSERT INTO BookStatus (SeatNo,No) VALUES ('U15',33);
INSERT INTO BookStatus (SeatNo,No) VALUES ('U16',34);
INSERT INTO BookStatus (SeatNo,No) VALUES ('U17',35);
INSERT INTO BookStatus (SeatNo,No) VALUES ('U18',36);