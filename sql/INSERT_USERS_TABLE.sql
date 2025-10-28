--INSERT USERS TABLE TEST
INSERT INTO users (username, name, email)
VALUES
 
 ('admin', 'admin', 'admin@app.com'),
 ('alex','alex', 'alex@app.com' ); 








Select
    *
from
    users;

update users
set status_id = 1
where users.name = 'admin' ;