CREATE DATABASE medicalapp;
USE medicalapp;
CREATE TABLE records( costumer_id VARCHAR(20), 
age FLOAT, 
gender FLOAT, 
cp FLOAT, 
trtbps FLOAT, 
chol FLOAT, 
FBS FLOAT, 
rest_ecg FLOAT, 
thalach FLOAT, 
exang FLOAT, 
oldpeak FLOAT, 
slp FLOAT, 
ca FLOAT, 
thall FLOAT);
INSERT INTO records( costumer_id, age , gender, cp, trtbps, chol, FBS, rest_ecg, thalach, exang, oldpeak, slp, ca, thall) VALUES( "0", 63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1);
SELECT * FROM records;
SELECT costumer_id FROM records ORDER BY costumer_id DESC LIMIT 1;
DELETE FROM records WHERE costumer_id>'0' LIMIT 10;
CREATE TABLE appointments( costumer_id VARCHAR(20),
costumer_name VARCHAR(20),
costumer_no VARCHAR(15),
costumer_email VARCHAR(30), 
app_slot VARCHAR(6),
app_date DATE,
doc_id VARCHAR(5),
ini_cond VARCHAR(1));
SELECT * FROM appointments;
DELETE FROM appointments WHERE costumer_id>'0' LIMIT 10;
CREATE TABLE doctors( doc_id VARCHAR(5),
doc_name VARCHAR(20),
doc_email VARCHAR(30),
slot_avail VARCHAR(19));
SELECT * FROM doctors;