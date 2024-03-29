ATTACH DATABASE draft.db;

CREAT TABLE IF NOT EXISTS links
(
    link_id INTEGER PRIMARY KEY AUTOINCREMENT,
    link TEXT
);

CREATE TABLE IF NOT EXISTS requests
(
    request_id INTEGER PRIMARY KEY,
    request_datetime TEXT,
    request_status TEXT 
);

CREATE TABLE IF NOT EXISTS regions
(
    region_id INTEGER PRIMARY KEY,
    region_name TEXT,
    link_id INTEGER
);

CREATE TABLE IF NOT EXISTS universities
(
    university_id INTEGER PRIMARY KEY,
    university_name TEXT,
    region_id INTEGER,
    link_id
)