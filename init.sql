
CREATE USER 'user'@'%' IDENTIFIED BY 'rootpassword';

GRANT ALL PRIVILEGES ON autohaus_db.* TO 'user'@'%';

FLUSH PRIVILEGES;
