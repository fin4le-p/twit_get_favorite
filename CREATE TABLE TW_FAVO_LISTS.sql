create table TW_FAVO_LISTS(
    tw_favo_list_id serial PRIMARY KEY not null,
    user_id varchar(20) not null,
    tweet_data timestamp not null,
    tweet_text varchar(600) not null,
    fav integer not null,
    rt integer not null,
    created_at timestamp not null,
    updated_at timestamp not null,
    deleted_at timestamp
)