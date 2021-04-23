PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE posts(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, text TEXT NOT NULL, timestamp TEXT NOT NULL);
INSERT INTO posts VALUES(1,'Brandon','hello world','03-07-2021');
INSERT INTO posts VALUES(2,'Brandon','My first post!','2021-03-07 15:31:17');
INSERT INTO posts VALUES(3,'Brandon','My 2nd ever post!','2021-03-08 00:14:16');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('posts',3);
COMMIT;
