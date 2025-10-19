DROP DATABASE IF EXISTS tienda_online;
CREATE DATABASE tienda_online;
USE tienda_online;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT DEFAULT 0,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE carritos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    producto_id INT,
    cantidad INT DEFAULT 1,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

ALTER TABLE productos
ADD COLUMN usuario_id INT,
ADD FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE;

CREATE TABLE imagenes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT NOT NULL,
    nombre_archivo VARCHAR(255),
    datos LONGBLOB NOT NULL,
    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
);

