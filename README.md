# `company name` test task

REST API server using django-rest-framework with pagination, sorting and filtering for two models:

Transaction (id, wallet_id (fk), txid, amount);

Wallet (id, label, balance);

Where txid is required unique string field, amount is a number with 18-digits precision, label is a string field, balance is a summary of all transactions’s amounts.

## Setup
Create `.env` file with the following variables (values are provided just for example):
```
MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=b2bbroker
DB_USER=root
DB_PASSWORD=root
DB_HOST=db
```
## Run
The project is containerized. So just run
```
docker-compose up
```
When the project is launched first time, apply Django migrations:
```
docker-compose exec app python manage.py migrate
```
The project is accessible at http://localhost:8000 

### Tests
```
docker-compose exec app python manage.py test
```

### Endpoints
- wallets - list of all wallets. Can be filtered by a label name, query string argument `label`
- wallets/:id - wallet details
- wallets/:id/transactions - list of wallet transactions. Can be filtered by the argument `amount` or an amount range specified by `amount_min` and / or `amount_max`
- wallets/:id/transactions/:id - transaction details

The list endpoints accept `limit` and `offset` pagination parameters.

## Potential improvements
- Add authorization
- Implement non-integer wallet identifiers
