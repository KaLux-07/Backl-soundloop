-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS soundloop;

-- Seleccionar la base de datos
USE soundloop;

-- Crear la tabla "users"
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    surname VARCHAR(255),
    email VARCHAR(255),
    username VARCHAR(255),
    password_hash VARCHAR(255)
);

-- Crear la tabla "loops"
CREATE TABLE IF NOT EXISTS loops (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Crear la tabla "sounds"
CREATE TABLE IF NOT EXISTS sounds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sound_data BLOB,
    loop_id INT,
    user_id INT,
    FOREIGN KEY (loop_id) REFERENCES loops(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);