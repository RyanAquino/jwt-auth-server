# JWT/OAuth Authentication Server
Token Authentication Server that utilizes JWT and Google OAuth with a simple frontend.

### Setup
1. Set **MySQL database info** and **JWT token secrets** on `config.py`
2. run Server: ```python auth.py```
3. run Frontend: ``` python -m http.server```

### Tech Stack
* Python Flask
* HTML
* CSS
* JavaScript

### Libraries Used
* JWT
* Argon2 
* flask CORS
* MySQL Connector

### Database Querying
```
print(query_all('SELECT * FROM users')) # Query All
print(query_one('SELECT id FROM users where username = "test"')) # Query One
# data = {
#     'username': 'test',
#     'password': '$argon2id$v=19$m=102400,t=2,p=8$L+l4tHExPwcCxO+cRK/Viw$DjKX7ZCh34i4PcUVklijYw'
# }
print(insert('INSERT INTO users (username, password) VALUES (%(username)s, %(password)s)', data)) # Insert Data
```


