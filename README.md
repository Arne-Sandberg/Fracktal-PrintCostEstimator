# Fracktal-PrintCostEstimator

This is a small web application which takes an STL file and returns the volume, estimated time for printing and cost of print.
### Requirements
- Python 3
- Django
- numpy + stl python libraries
- Cura Engine ( to use the exact version I used, click here: http://3dpartprice.com/3dpartpricelib/3dpartpricelib-0.1.4.zip. Extract the archive and copy the Cura folder into the Fracktal-PrintCostEstimator folder )
## Running it and more
* To run it on a local server (localhost:8000), navigate to the root folder where manage.py exists and run this command:
  ```
  python manage.py runserver
  ```
  To create an admin account (localhost:8000/admin), run:
  ```
  python manage.py createsuperuser
  ```
  Refer Django documentation (https://docs.djangoproject.com/en/1.10/) on how to deploy it on a production server.
### Acknowledgements
- https://github.com/iashwinprasada/CuraEstimator ( for the gcode analysis )
