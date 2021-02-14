create table TWITTER_FAVO_TIMELINE(
id varchar(20) character set utf8mb4,
user varchar(20) character set utf8mb4,
got_at datetime,
created_at datetime,
text varchar(600) character set utf8mb4,
fav int,
rt int
)CHARSET=utf8mb4;

alter table TWITTER_FAVO_TIMELINE add primary key (id,user);