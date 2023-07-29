DROP TABLE IF EXISTS lawn_owners;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS lawns;
DROP TABLE IF EXISTS employees;


CREATE TABLE employees (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    address VARCHAR(100),
    email VARCHAR(100),
    dob DATE,
    phone VARCHAR(15),
    start_date DATE,
    title VARCHAR(50)
) ENGINE=INNODB;


CREATE TABLE customers (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    address VARCHAR(100),
    email VARCHAR(100),
    dob DATE,
    phone VARCHAR(15)
)ENGINE=INNODB;

CREATE TABLE lawns (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(100),
    size INT,
    date_added DATE,
    lawn_type VARCHAR(100),
    notes VARCHAR(200)
)ENGINE=INNODB;

CREATE TABLE lawn_owners (
    customer_id INT NOT NULL,
    lawn_id INT NOT NULL,
    PRIMARY KEY (customer_id, lawn_id),
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (lawn_id) REFERENCES lawns(id)
)ENGINE=INNODB;


INSERT INTO employees (first_name, last_name, address, email, dob, phone, start_date, title) VALUES
('James', 'Dill', '123 John St', 'jamesdill@example.com', '1990-01-01', '123-456-7890', '2020-01-01', 'Manager'),
('Jane', 'Smith', '784 Oak Ave', 'jane.smith@example.com', '1985-05-10', '987-654-3210', '2018-05-01', 'Assistant'),
('Gary', 'Davies', '981 Elm Rd', 'gary.davies@example.com', '1993-09-15', '555-888-7777', '2019-11-20', 'Supervisor'),
('Emily', 'Johnson', '456 Pine St', 'emily.johnson@example.com', '1998-12-05', '444-999-3333', '2022-03-10', 'Technician'),
('Michael', 'Brown', '876 Oak Ave', 'michael.brown@example.com', '1996-07-30', '777-222-1111', '2021-06-15', 'Analyst');


INSERT INTO customers (first_name, last_name, address, email, dob, phone) VALUES
('Alice', 'Johnson', '789 Elm Rd', 'alice.johnson@example.com', '1988-11-20', '555-123-4567'),
('Bob', 'Williams', '101 Pine St', 'bob.williams@example.com', '1995-07-15', '555-987-6543'),
('David', 'Smith', '888 Oak Ave', 'david.smith@example.com', '1992-03-25', '555-444-3333'),
('Jennifer', 'Johnson', '456 Elm Rd', 'jennifer.johnson@example.com', '1997-09-18', '555-789-4561'),
('Robert', 'Davis', '321 Pine St', 'robert.davis@example.com', '1984-12-10', '555-321-7894');


INSERT INTO lawns (address, size, date_added, lawn_type, notes) VALUES
('100 N College Ave Bloomington, IN', 12500, '2023-04-22', 'Commerical', 'Downtown lot without much parking. No mowing during the week!'),
('50 Elm St Bloomington, IN', 8000, '2023-05-10', 'Residential', 'Front yard only.'),
('789 Oak Ave Bloomington, IN', 6000, '2023-06-15', 'Residential', 'Backyard with a garden.'),
('654 Pine St Bloomington, IN', 10000, '2023-07-01', 'Residential', 'Large front and side lawn.'),
('222 Elm Rd Bloomington, IN', 3500, '2023-08-05', 'Commercial', 'Small corner lot with minimal maintenance needed.');

INSERT INTO lawn_owners (customer_id, lawn_id) VALUES
(1, 1),
(2, 2), 
(3, 3), 
(4, 4),
(5, 5); 