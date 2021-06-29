CREATE table users(
    chat_id integer primary key,
    types_activities text
);

CREATE table activities(
    id integer,
    user_chat_id integer,
    type_activities varchar(255),
    start datetime,
    stop datetime,
    FOREIGN KEY(user_chat_id) REFERENCES users(chat_id),
    PRIMARY KEY (id)
);