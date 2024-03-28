DROP DATABASE If EXISTS food_trucks;

DROP TABLE IF EXISTS transaction_type CASCADE;
DROP TABLE IF EXISTS truck CASCADE;
DROP TABLE IF EXISTS transaction CASCADE;

CREATE TABLE transaction_type(
    id INT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(50),
    PRIMARY KEY (id),
    UNIQUE (name)
);

CREATE TABLE truck(
    id INT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(250),
    description TEXT,
    card_reader BOOLEAN,
    fsa_rating SMALLINT,
    PRIMARY KEY (id),
    UNIQUE (name, description)
);

CREATE TABLE transaction(
    id INT GENERATED ALWAYS AS IDENTITY,
    timestamp timestamptz,
    type_id INT,
    total DECIMAL(6,2),
    truck_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (type_id) REFERENCES type(id),
    FOREIGN KEY (truck_id) REFERENCES truck(id)
);