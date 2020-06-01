# JWT Authentication Server
Token Authentication Server that utilizes JWT with a simple frontend.

### Setup
> Note: Domain is set to 127.0.0.1 for both FE/BE since SameSite: Lax
1. Server: ```python auth.py```
2. Frontend: ``` python -m http.server```

### Variables
> Set All variables in config.py
1. MySQL Database - including credentials
2. Access token / Refresh token **secret** key

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