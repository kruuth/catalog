# Catalog Project - Udacity Full Stack Project 3

## Application information

* First start the catalog application from the command line by typing "python catalog.py" to start the application.  
* The catalog application can be accessed from a web browser by accesing url `http://localhost:5000`, once the server is running.  
* Users need a google account to do anything beyond viewing categories.  
* The application provides the user with a login page using their Google account information.  
* The application forbids the editing or deletion catagories created by users other than the one signed in.  
* The application prohibits users adding, editing or deleting items in a category created by another user.  
* JSON endpoints are provided as described in the below JSON Endpoints section of this readme file.  
* You will posibly need your own client_secrets.json file for your own enpoints if this is needed.  

## Environment information

The applications were used during the development of this project:  
* sqlite
* FireFox Quantum 64.0
* Python 2.7
* DB Browser for SQLite
* Google Chrome Version 73.0.3683.86 (Official Build) (64-bit)
* VirtualBox Version 5.2.26 r128414 (Qt5.6.2)
* Vagrant Version 2.2.2
* Postman [Get Postman](https://www.getpostman.com/downloads/) for testing JSON
* Files required to operate the server and application are located in the catalog.zip file.
If you already have a running vagrant instance on your computer, then decompress the contents of the zip file inside the  
vagrant directory of your choosing.  If you do not have an existing instance of Vagrant then continue to the next section.  

Creating a functional Vagrant instance:  

1. Download the Udacity Full Stack Wed Developer VM from Github here:  [https://github.com/udacity/fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) and follow the directions there to get your instance running.  
2. Load the files and directories supplied in the catalog.zip file into the directory `/fullstack/vagrant/catalog` note that the root of the directory is where you put your vagrant instance mentioned above.  
3. You must run the database_setup.py and loaddatabasecontent.py to use the database.  
4. Open a command line(Start Menu->cmd) and type the following commands:  
	1. `cd /fullstack/vagrant/ `  
	2. `vagrant up`  
	3. `vagrant ssh`  
	4. `cd /vagrant`  
	5. `cd catalog`  
 

## Database Setup

* A sample database is supplied with sample data and is named vgcatalog.db  
* Optionally a new blank database can be created by running `python database_setup.py`  
* Optionally the new blank database can be loaded with data by running `python loaddatabasecontent.py`  

## Running the Server

1. Use python to run the server application from the catalog directory: `python catalog.py`  
2. Once the server is up the catalog application can be accessed via a web browser at this url/address `http://localhost:5000`  

## JSON Endpoints

The follwing JSON endpoints are available.<br/>
The examples are intended to work with the author supplied populated database.  
1. Get all categories: `http://localhost:5000/category/JSON`  
     -ex:  `http://localhost:5000/category/JSON`  
2. Get all categories owned by a single user: `http://localhost:5000/user/<int:user_id>/categories/JSON`  
     -ex:  `http://localhost:5000/user/1/categories/JSON`  
3. Get all items in single category: `http:localhost:5000/category/<int:category_id>/item/JSON`  
     -ex: `http://localhost:5000/category/1/item/JSON`  
4. Get a single item in a category: `http://localhost:5000/category/<int:category_id>/item/<int:item_id>/JSON`  
     -ex: `http://localhost:5000/category/1/item/1/JSON`  
5. Get all users: `http://localhost:5000/users/JSON`  
     -ex:  `http://localhost:5000/users/JSON`  


## Acknowledgements

- Udacity Full Stack Web Development - Catalog Project.  
- python validation - [PEP8 online tool](http://pep8online.com/)  
- Google OAuth2 documentation(https://developers.google.com/identity/protocols/OAuth2)  
