CREATE DATABASE gym;

USE gym;

CREATE TABLE members (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    plan VARCHAR(50),
    status VARCHAR(50)
);
