drop database rpr;
create database rpr;
use rpr;

create table user (
    username varchar(255) primary key,
    password varchar(255)
);

create table written (
    paper varchar(255),
    author varchar(255),
    primary key (paper, author),
    foreign key (author) references user(username)
);

