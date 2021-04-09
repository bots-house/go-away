create schema if not exists go_away;

create table if not exists go_away.hits
(
    id            serial                   not null,
    at            timestamp with time zone not null,
    redirect_to   varchar(600)             not null,
    redirect_from varchar(600),
    user_id       uuid                     not null,
    ip            text                     not null,
    user_agent    text                     not null,
    other_params  jsonb
);

create unique index if not exists hits_id_uindex
    on go_away.hits (id);
