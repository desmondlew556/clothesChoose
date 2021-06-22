## Setup

Setup instructions will always start from the root folder of this repo.

### Django Environment
Create a virtual environment to download the required modules for the Django Server. Please name it ``venv`` because the ``.gitignore`` only ignores the folder venv.
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Node Packages
Change directory into the react front-end folder and install the node modules.
```sh
cd react-api-search
npm i
```

## Running the Servers
Once again, assuming that you're running from the root directory of this repo.

### Django Backend
Need to activate virtualenv if you have not already done so.
```sh
source venv/bin/activate
cd api_server
python manage.py migrate
python manage.py runserver
```

### React Client
```sh
cd react-frontend
npm start
```
# clothesChoose
