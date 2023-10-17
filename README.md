# Description
This back-end provides endpoints for working with e-commerce website, including registration, phone verification and authorisation with JWT-tokens, searching products, adding them to cart, using promocedes and creating orders. Also it provides admin-panel, that allows to create new products or categories, and also verify clients by their Id.

# Technologies
The project was developed with Django Rest Framework, docker conterisation, nginx web-server and Postgresql dbms.

# Usage
create .env-app file with SECRET_KEY, DEBUG, ALLOWED_HOSTS, POSTGRES_HOST, TWILIO_VERIFY_SERVICE_SID, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN.
and .env-db file with POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD.

then use comands:
```
docker build -t ss_web .
docker compose up
```
