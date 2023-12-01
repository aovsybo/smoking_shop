# Description
This back-end provides endpoints for working with e-commerce website, including registration, phone verification and authorisation with JWT-tokens, searching products, adding them to cart, using promocedes and creating orders. Also it provides admin-panel, that allows to create new products or categories, and also verify clients by their Id.
App has next roles:
- any
- authorised
- admin

what has been developed:
- JWT-aythentication
- user verification by phone and passport/id
- CRUD for categories and products (Non-admin users can only read)
- Searching filters and sting search
- Creating promocode (for admin)
- Cart CRUD and promocode applying (for authenticated)
- Order creating
- Notifications for admin

# Technologies
Back-end part was developed with Django Rest Framework <br>
Postgresql was used as dbms <br>
For copying catalog was used beautifulsoup for websccrapping and aiohttp for requests <br>
Docker and docker compose were used for containerisation <br>
Nginx was used as a web server <br>

# Starting
create .env-app file with 
```
SECRET_KEY
DEBUG
ALLOWED_HOSTS
POSTGRES_HOST
TWILIO_VERIFY_SERVICE_SID
TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN
```
and .env-db file with 
```
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
```
then use comands:
```
pip install -r requirements.txt
docker build -t ss_web .
docker compose up
```

# Usage
## Account
### register
![image](https://github.com/aovsybo/smoking_shop/assets/66824112/9cd4d294-4195-42c0-94d8-f0b49b739105)

### phone verify
![image](https://github.com/aovsybo/smoking_shop/assets/66824112/a7a808de-d7eb-4dc3-8f6b-8d19124b9c86)

### get token
![image](https://github.com/aovsybo/smoking_shop/assets/66824112/7d6b95bb-0179-4e49-b067-b96a809e5bac)

## Products
### create (by user)
![image](https://github.com/aovsybo/smoking_shop/assets/66824112/3fb44dd8-3971-43e4-96c9-e2303fb0058b)

### create (by admin)
![image](https://github.com/aovsybo/smoking_shop/assets/66824112/ee20c2f1-1115-48b2-8f9e-a675bc95eb74)

### get one
![image](https://github.com/aovsybo/smoking_shop/assets/66824112/e9e6326c-9d91-4799-8643-08ab3fbeab3b)

### get all
![image](https://github.com/aovsybo/smoking_shop/assets/66824112/87ba2600-92ec-4266-828d-80a70ad9a47e)

### get by text request 
![image](https://github.com/aovsybo/smoking_shop/assets/66824112/d64ae2db-2f5a-4566-a8d4-75455880381d)

## Categories
### create (by user)
![image](https://github.com/aovsybo/smoking_shop/assets/66824112/2971523b-9d8e-4ffe-891d-5bfdd112c9f1)

### create (by admin)
![image](https://github.com/aovsybo/smoking_shop/assets/66824112/074e7f32-2704-40a1-b1cf-4d94ea6cb2e7)

### get one
![image](https://github.com/aovsybo/smoking_shop/assets/66824112/132324e2-ec7e-4480-95f2-92a46b7f1d6e)

### get all
![image](https://github.com/aovsybo/smoking_shop/assets/66824112/a73be0d3-e85b-4256-8b29-9e5de64983cc)

## Cart
### add item
![image](https://github.com/aovsybo/smoking_shop/assets/66824112/6aaefaaf-f287-4b15-b5e3-c2e652fc8128)
![image](https://github.com/aovsybo/smoking_shop/assets/66824112/1500b69f-e406-4b36-a6b1-8300e5252d74)

### remove
![image](https://github.com/aovsybo/smoking_shop/assets/66824112/8a3c37cc-f9d4-4078-b0a5-65e5377edb0a)
![image](https://github.com/aovsybo/smoking_shop/assets/66824112/1a762317-1514-43b0-a3a4-c2763327d0e1)

### create promocode (by admin)
![image](https://github.com/aovsybo/smoking_shop/assets/66824112/b3b64798-5b35-4b58-b68d-5b0dd2c07289)

### use promocode (by user)
![image](https://github.com/aovsybo/smoking_shop/assets/66824112/c1bf1dde-dee9-4453-9c77-23aadbbd15b3)
![image](https://github.com/aovsybo/smoking_shop/assets/66824112/daa5eabe-ee93-4777-a614-5eabe2c78298)
