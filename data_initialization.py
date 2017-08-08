#For Fresh Project
python3 manage.py br_delete_migrations
python3 manage.py br_init_migrations
python3 manage.py br_init
python3 manage.py makemigrations
python3 manage.py migrate

#After DB activities
python3 manage.py init_utilities
python3 manage.py upload_warehouse
python3 manage.py upload_author
python3 manage.py upload_publisher
python3 manage.py upload_category
python3 manage.py upload_currency_list
python3 manage.py upload_books
python3 manage.py upload_inventory
python3 manage.py upload_sale_price
python3 manage.py upload_rent_price