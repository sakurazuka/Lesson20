DROP TABLE if exists users;
CREATE TABLE IF NOT EXISTS users (
     account_name TEXT NOT NULL,
     user_photo TEXT NOT NULL,
     UNIQUE(account_name,user_photo));

INSERT INTO users (account_name, user_photo) VALUES ('麹町太郎' , './upload/taro.png');
INSERT INTO users (account_name, user_photo) VALUES ('麹町花子' , './upload/hanako.png');

DROP TABLE if exists bmi_data;
CREATE TABLE IF NOT EXISTS bmi_data (
     account_name TEXT NOT NULL,
     bmi REAL NOT NULL,
     date TEXT NOT NULL, 
     UNIQUE(account_name,date));

INSERT INTO bmi_data (account_name, bmi,date) VALUES ('麹町太郎' ,21.4,'2013-07-01');
INSERT INTO bmi_data (account_name, bmi,date) VALUES ('麹町太郎' ,22.4,'2013-08-01');
INSERT INTO bmi_data (account_name, bmi,date) VALUES ('麹町太郎' ,22.7,'2013-09-01');
INSERT INTO bmi_data (account_name, bmi,date) VALUES ('麹町太郎' ,23.1,'2013-10-01');
INSERT INTO bmi_data (account_name, bmi,date) VALUES ('麹町花子' ,23.4,'2013-07-01');
INSERT INTO bmi_data (account_name, bmi,date) VALUES ('麹町花子' ,22.4,'2013-08-01');
INSERT INTO bmi_data (account_name, bmi,date) VALUES ('麹町花子' ,24.7,'2013-09-01');
INSERT INTO bmi_data (account_name, bmi,date) VALUES ('麹町花子' ,25.1,'2013-10-01');

