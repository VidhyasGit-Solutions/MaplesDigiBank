# MaplesDigiBank
BankingApplication - academic project (BigData Solution Architecture-2023)


Steps to run:

1. Install the python package
 ```bash
 pip install -r requirements.txt
 ```

2. Create the Mysql database
```bash
mysql -u root -p -e "CREATE DATABASE maple_digi_bank"
```

3. ADD MYSQL credentails in `maples_digi_app/__init__.py`.
```bash
DATABASE_NAME = "maple_digi_bank"
MYSQL_USERNAME = "root"
MYSQL_HOST = "localhost"
MYSQL_PASSWORD = "password"
```

3. Run the python file
```bash
python run.py
```