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

INSERT INTO type (name)
VALUES
('cash'),
('card');

INSERT INTO truck (name, description, card_reader, fsa_rating)
VALUES
('Burrito Madness','An authentic taste of Mexico.', TRUE, 4),
('Kings of Kebabs', 'Locally-sourced meat cooked over a charcoal grill.', TRUE, 2),
('Cupcakes by Michelle','Handcrafted cupcakes made with high-quality, organic ingredients.', TRUE, 5),
('Hartmann''s Jellied Eels','A taste of history with this classic English dish.', TRUE, 4),
('Yoghurt Heaven','All the great tastes, but only some of the calories!', TRUE, 4),
('SuperSmoothie','Pick any fruit or vegetable, and we''ll make you a delicious, healthy, multi-vitamin shake. Live well; live wild.', FALSE, 3);