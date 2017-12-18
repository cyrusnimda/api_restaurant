CREATE TABLE table (
        id INTEGER NOT NULL,
        description VARCHAR(200),
        seats INTEGER,
        PRIMARY KEY (id)
);
CREATE TABLE user_role (
        id INTEGER NOT NULL,
        name VARCHAR(50),
        description VARCHAR(200),
        PRIMARY KEY (id),
        UNIQUE (name)
);
CREATE TABLE user (
        id INTEGER NOT NULL,
        name VARCHAR(50),
        password VARCHAR(80),
        token VARCHAR(80),
        role_id INTEGER NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(role_id) REFERENCES user_role (id)
);
CREATE TABLE booking (
        id INTEGER NOT NULL,
        booked_at DATETIME,
        persons INTEGER,
        booked_by INTEGER NOT NULL,
        created_at DATETIME,
        PRIMARY KEY (id),
        FOREIGN KEY(booked_by) REFERENCES user (id)
);
CREATE TABLE booking_tables (
        table_id INTEGER NOT NULL,
        booking_id INTEGER NOT NULL,
        PRIMARY KEY (table_id, booking_id), 
        FOREIGN KEY(table_id) REFERENCES table (id),
        FOREIGN KEY(booking_id) REFERENCES booking (id)
);
