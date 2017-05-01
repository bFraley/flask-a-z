drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null
);


drop table if exists items;
create table items (
    id integer primary key autoincrement,
    name text not null,
    qty integer not null,
    year text not null
);








