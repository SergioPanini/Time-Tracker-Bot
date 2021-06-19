CREATE table users(
    chat_id integer primary key,
    types_activities text
);

CREATE table activities(
    user_chat_id integer,
    type_activities varchar(256),
    start datetime,
    stop datetime,
    FOREIGN KEY(user_chat_id) REFERENCES user(chat_id)
);