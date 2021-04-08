create schema if not exists go_away;

create table if not exists go_away.hits
(
    id            serial                   not null,
    at            timestamp with time zone not null,
    redirect_to   varchar(600)             not null,
    redirect_from varchar(600),
    user_id       uuid                     not null,
    ip            varchar(15)              not null,
    user_agent    varchar(180)             not null,
    other_params  jsonb
);

create unique index if not exists hits_id_uindex
    on go_away.hits (id);
