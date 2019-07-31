# Example Catalog API with DRF

We use as an example a "shoes" CRUD. It was used for API:
-  Django
-	Django Rest Framework
-	Pytest
-  Docker
-  MySQL
- Swagger

## Installation

For installation will be used as reference Ubuntu 18.04 64bits

**Ubuntu requirements:**
```
sudo apt install curl git make libmysqlclient-dev python3-dev python3-venv docker docker-compose
```
**Fork the repository on GitHub:**
```
git clone git@github.com:eduleones/catalog-backend-example.git
cd catalog-backend-example/
```

**Create and activate virtualenv**
```
python3 -m venv venv
source venv/bin/activate
```
**Python dependency:**
```
make requirements-pip
```

**Started MySQL with Docker Compose:**
```
sudo docker-compose up -d
```
**Create and configure .env  / django superuser:**
```
make install-linux
```
Create API token:
```
make create_token user=joao
```
"user" the superuser created in the previous command.

## Run tests

```
make test
```
## Run webserver

```
make runserver
```

## API Documentation
Enter your browser with the following address:
```
 http://127.0.0.1:8000/docs/
```

## Import csv file

You can bulk upload "shoe" data. For this, get the template sheet here: CSV

Then send CSV file to API:

```
curl -X POST \
  http://localhost:8000/shoes/csv_import/ \
  -H 'Authorization: Token {token}' \
  -H 'Content-disposition: attachment;filename=upload_file.csv' \
  -H 'Postman-Token: 432bed2c-820b-405b-b451-78bc606b29f9' \
  -H 'cache-control: no-cache' \
  -F file=@upload_file.csv
```
{token} Token created with previous command 