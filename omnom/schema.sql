DROP TABLE IF EXISTS recipe;
DROP TABLE IF EXISTS food_type;

PRAGMA foreign_keys=ON;

CREATE TABLE food_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_type TEXT NOT NULL UNIQUE
);


CREATE TABLE recipe (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    type_id INTEGER,
    photo TEXT,
    FOREIGN KEY (type_id) REFERENCES food_type (id)
);
