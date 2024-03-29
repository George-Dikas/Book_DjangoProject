# Book_DjangoProject
## Description
With Book_DjangoProject a user can:
* create an account as a Library User, or as an Author, or as a Publisher
* as a Library User a user can: 
  - see all the published books
  - add a book to favourite or remove it
  - see all his/her favourite books
  - rate a book
  - see his/her personal info
  - change his/her personal info or password
  - delete his/her profile
* as an Author a user can: 
  - see all his/her books
  - update or delete a book
  - add a new book
  - see his/her personal info
  - change his/her personal info or password
  - delete his/her profile
* as a Publisher a user can: 
  - see all his/her published books 
  - update or delete a book
  - add a new book with one or more authors
  - see all collaborative authors
  - see his/her personal info
  - change his/her personal info or password
  - delete his/her profile
## Technologies
* Django 4.1.3
* Django-crispy-forms 1.14.0
* Bootstrap 5.1.3
* Fontawesome 5.11.2
## Use Project Locally:
* Project Folder and Virtual Environment:		
  - Open Visual Studio Code
  - Launch Profile/Command Prompt																										
  - Go to this path: C:\Users\User\Desktop																					
  - Create a folder for the project: C:\Users\User\Desktop>mkdir Book_DjangoProject								
  - Get inside the folder: C:\Users\User\Desktop>cd Book_DjangoProject																								
  - Create a Virtual Environment with name myenv: C:\Users\User\Desktop\Book_DjangoProject>python -m venv myenv					
  - Activate Virtual Environment: C:\Users\User\Desktop\Book_DjangoProject>myenv\Scripts\activate										
* Clone Project OR:                                                                                                                     									
  - (myenv) C:\Users\User\Desktop\Book_DjangoProject>git clone https://github.com/George-Dikas/Book_DjangoProject.git	
  - Change folder's name Book_DjangoProject inside the Project Folder into book_project			
  - (myenv) C:\Users\User\Desktop\Book_DjangoProject>cd book_project		
* Download Project:
  - Code/Download Zip
  - Extract folder and put it into Book_DjangoProject folder
  - Change folder's name Book_DjangoProject-master into book_project
  - (myenv) C:\Users\User\Desktop\Book_DjangoProject>cd book_project
* Run Project: 
  - Install all requirments for the project: 
    (myenv) C:\Users\User\Desktop\Book_DjangoProject\book_project>pip install -r requirements.txt
  - Begin your local server: 
    (myenv) C:\Users\User\Desktop\Book_DjangoProject\book_project>python manage.py runserver
  - Type into your browser: http://127.0.0.1:8000/library/login/
