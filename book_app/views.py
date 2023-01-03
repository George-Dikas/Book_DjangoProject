from django.shortcuts import render, redirect
from book_app.forms import *
from book_app.models import *
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import HiddenInput


# Common views and functions: userType, loginView, logoutView, homeView, infoView, delProfView

def userType(user):
    if (LibraryUser.objects.filter(user=user)):
        user_type = 'LibraryUser'
    
    elif (Author.objects.filter(user=user)):
        user_type = 'Author'

    else: 
        user_type = 'Publisher'
    
    return user_type

def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                 login(request, user)
                 user_type = userType(user)
                 messages.success(request, 'You are logged in!')
                 return redirect('homeView', user_type, username)

            else: 
                messages.error(request, 'Username and password do not match.')
        
    form = LoginForm()
    return render(request, 'book_app/Common/login.html', {'form':form})

def logoutView(request):
    logout(request)
    messages.warning(request, 'You have been successfully logged out.')
    return render (request, 'book_app/Common/logout.html')

@login_required(login_url='/library/login/')
def homeView(request, user_type, username):
    data={}

    if user_type == 'LibraryUser':
        books = Book.objects.all()
        
        if books: 
            data['books'] = books
            lib_user = LibraryUser.objects.get(user=request.user)
            favourites = Favourite.objects.filter(lib_user=lib_user)

            if favourites:
                favourite_books = []
                for obj in favourites:
                    favourite_books.append(obj.book)
                data['favourite_books'] = favourite_books
                
            else:
                data['favourite_books'] = Favourite.objects.none

        else:
            data['message'] = 'Sorry, there are no books at the moment.'

    elif user_type == 'Author':
        author = Author.objects.get(user=request.user)
        books = Book.objects.filter(authors__pk=author.pk)

        if books:
            data['books'] = books
            data['form'] = BookEditForm()

        else:
            data['message'] = 'You have not written any book yet. '

    else:
        publisher = Publisher.objects.get(user=request.user)
        books = Book.objects.filter(publisher=publisher)

        if books:
            data['books'] = books
            data['form'] = BookEditForm()

        else:
            data['message'] = 'You have not published any book yet. '
        
    data['user_type'] = user_type
    data['username'] = username
    return render(request, 'book_app/Common/home.html', data)

@login_required(login_url='/library/login/')
def infoView(request):
    user = request.user
    user_type = userType(user)
    formPwd = PasswordChangeForm(user)
    
    if user_type == 'LibraryUser':
        context = contextLibraryUser(user)
        formUpdate = LibraryUpdateForm(initial=context)
    
    elif user_type == 'Author':
        context = contextAuthor(user)
        formUpdate = AuthorUpdateForm(initial=context)

    else:
        context = contextPublisher(user)
        formUpdate = PublisherUpdateForm(initial=context)
    
    if request.method == 'POST':
        if 'subProf' in request.POST:
            if user_type == 'LibraryUser':
                formUpdate = LibraryUpdateForm(request.POST, instance=user)
                
                if formUpdate.is_valid():
                    formUpdate.save()
                    messages.success(request, 'Your profile was updated succesfully!')
                    return redirect('infoView')

            elif user_type == 'Author':
                formUpdate = AuthorUpdateForm(request.POST, instance=user)
                
                if formUpdate.is_valid():
                    age = request.POST['age']
                    Author.objects.filter(user=user).update(age=age)
                    formUpdate.save()
                    messages.success(request, 'Your profile was updated succesfully!')
                    return redirect('infoView')

            else: 
                formUpdate = PublisherUpdateForm(request.POST, instance=user)
                
                if formUpdate.is_valid():
                    name = request.POST['name']
                    address = request.POST['address']
                    city = request.POST['city']
                    Publisher.objects.filter(user=user).update(name=name)
                    Publisher.objects.filter(user=user).update(address=address)
                    Publisher.objects.filter(user=user).update(city=city)
                    formUpdate.save()
                    messages.success(request, 'Your profile was updated succesfully!')
                    return redirect('infoView')

            #When formUpdate is invalid
            messages.error(request, "Something went wrong. Your profile wasn't updated.")
            
        elif 'subPwd' in request.POST:
            formPwd = PasswordChangeForm(request.user, request.POST)
            if formPwd.is_valid():
                formPwd.save()
                update_session_auth_hash(request, formPwd.user)
                messages.success(request, 'Your password was changed succesfully!')
                return redirect('infoView')

            else: 
                messages.error(request, "Something went wrong. Password wasn't changed.")
    
    data = {'context':context, 'formUpdate':formUpdate, 'formPwd':formPwd, 'user_type':user_type, 'username':user.username}
    return render(request, 'book_app/common/info.html', data)

@login_required(login_url='/library/login/')
def delProfView(request):
    request.user.delete()
    messages.warning(request, 'Your account was deleted succesfully.')
    return redirect('logoutView')


# Common views and functions for Authors and Publishers: addBookView, editBookView, deleteBookView

@login_required(login_url='/library/login/')
def addBookView(request):
    user = request.user
    user_type =userType(user)

    if request.method == 'POST': 
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST['title']
            form.save()
            messages.success(request, f'The book with title "{title}" was saved succesfully!')
            return redirect('addBookView')

        else: 
            messages.error(request, "Something went wrong. Book wasn't added.")
            
            if user_type == 'Publisher':
                form.fields['publisher'].widget = HiddenInput()
            
            else:
                form.fields['authors'].widget = HiddenInput()

            data = {'form':form, 'username':user.username, 'user_type':user_type}
            return render(request, 'book_app/common/newbook.html', data)

    if user_type == 'Publisher':
        form = BookForm(initial={'publisher': user.publisher})
        form.fields['publisher'].widget = HiddenInput()

    else:
        form = BookForm(initial={'authors': user.author})
        form.fields['authors'].widget = HiddenInput()

    data = {'form':form, 'username':user.username, 'user_type':user_type}
    return render(request, 'book_app/common/newbook.html', data)

@login_required(login_url='/library/login/')
def editBookView(request, book_id):
    username = request.user.username
    user_type = userType(request.user)
    data = {}
    book = Book.objects.get(id=book_id)
    
    if request.method == 'POST':
        form = BookEditForm(request.POST, instance=book)
        
        if form.is_valid():
            messages.success(request, 'You have succesfully updated the book!')
            form.save()
            return redirect('homeView', user_type, username)
        
        else:
            messages.error(request, "Something went wrong. Book wasn't updated.") 
            data['form'] = form
            data['book_id'] = book_id

            if user_type == 'Author':
                author = Author.objects.get(user=request.user)
                data['books'] = Book.objects.filter(authors__pk=author.pk)

            else:
                publisher = Publisher.objects.get(user=request.user)
                data['books'] = Book.objects.filter(publisher=publisher)
        
        data['user_type'] = user_type
        data['username'] = username
        
        return render(request, 'book_app/Common/home.html', data)
            
@login_required(login_url='/library/login/')
def deleteBookView(request, book_id):
    username = request.user.username
    user_type = userType(request.user)

    book = Book.objects.get(id=book_id)
    book.delete()
    messages.warning(request, f'The book with title "{book.title}" was deleted succesfully.')
    return redirect('homeView', user_type, username)


#Library Users views and functions: regLibUserView, contextLibraryUser, addFavouriteView, removeFavouriteView, favouritesView, rateView

def regLibUserView(request):
    if request.method == 'POST':
        form = LibraryUserForm(request.POST)
        if form.is_valid():
            user = form.save() 
            lib_user = LibraryUser(user=user)
            lib_user.save()

            user_type = userType(user)
            username = user.username

            messages.success(request, f'A Library User with username "{username}" was created!')
            messages.success(request, 'You are logged in!')
            login(request, user)
            return redirect('homeView', user_type, username)
        
        else: 
            return render(request, 'book_app/LibraryUser/registration.html', {'form':form})

    form = LibraryUserForm()
    return render(request, 'book_app/LibraryUser/registration.html', {'form':form})

def contextLibraryUser(user):
    context={
        'username':user.username,
        'user_type':userType(user),
        'first_name':user.first_name,
        'last_name':user.last_name,
        'email':user.email
    }

    return context

@login_required(login_url='/library/login/')
def addFavouriteView(request, book_id):
    user = request.user
    username = user.username
    user_type = userType(user)

    lib_user = LibraryUser.objects.get(user=user)
    book = Book.objects.get(id=book_id)
    favourite_book = Favourite(lib_user=lib_user, book=book)
    favourite_book.save()
    
    messages.success(request, f'{book.title} was added to your favourites!')
    return redirect('homeView', user_type, username)

@login_required(login_url='/library/login/')
def removeFavouriteView(request, book_id):
    user = request.user
    username = user.username
    user_type = userType(user)
    
    lib_user = LibraryUser.objects.get(user=user)
    book = Book.objects.get(id=book_id)
    favourite_book = Favourite.objects.get(lib_user=lib_user, book=book)
    favourite_book.delete()
    
    url_path = request.META.get('HTTP_REFERER')
    messages.warning(request, f'{book.title} was removed from your favourites.')

    if url_path == 'http://127.0.0.1:8000/library/favourites/':
        return redirect('favouritesView')
    
    else:
        return redirect('homeView', user_type, username)

@login_required(login_url='/library/login/')
def favouritesView(request): 
    user_type =userType(request.user)
    lib_user = LibraryUser.objects.get(user=request.user)
    favourites = Favourite.objects.filter(lib_user=lib_user)
    data = {}

    if favourites:
        favourite_books = []
        for obj in favourites:
            favourite_books.append(obj.book)
        data['favourite_books'] = favourite_books

    else:
        data['message'] = 'You have no favourite books at the moment.'

    data['user_type'] = user_type 
    data['username'] = request.user.username
    return render(request, 'book_app/LibraryUser/favourites.html', data)

@login_required(login_url='/library/login/')
def rateView(request, book_id): 
    user_type = userType(request.user)
    username = request.user.username
    
    if request.method == 'POST':
        if request.POST.get('stars') is not None:
            rating = int(request.POST['stars'])
            book = Book.objects.get(id=book_id)
            num_rates = book.num_rates
            num_stars = book.num_stars

            new_rating = (num_rates*num_stars + rating)/(num_rates + 1)
            num_rates = num_rates + 1

            Book.objects.filter(id=book_id).update(num_stars=new_rating)
            Book.objects.filter(id=book_id).update(num_rates=num_rates)

            messages.success(request, 'You have succesfully rated the book!')
            return redirect('homeView', user_type, username)
        
        else:
            messages.warning(request, 'You did not select a rating for the book.')
            return redirect('homeView', user_type, username)


# Author views and functions: regAuthorView, contextAuthor 

def regAuthorView(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            age = request.POST['age']
            user = form.save()
            Author_User = Author(user=user, age=age)
            Author_User.save()

            user_type = userType(user)
            username = user.username

            messages.success(request, f'A Author with username "{username}" was created!')
            messages.success(request, 'You are logged in!')
            login(request, user)
            return redirect('homeView', user_type, username)

        else: 
            return render(request, 'book_app/Author/registration.html', {'form':form})

    form = AuthorForm()
    return render(request, 'book_app/Author/registration.html', {'form':form})

def contextAuthor(user):
    context={
        'username':user.username,
        'user_type':userType(user),
        'first_name':user.first_name,
        'last_name':user.last_name,
        'age':user.author.age,
        'email':user.email
    }

    return context


# Publisher views and functions: regPublisherView, contextPublisher, authorsView

def regPublisherView(request):
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            name = request.POST['name']
            address = request.POST['address']
            city = request.POST['city']
            user = form.save()
            Publisher_User = Publisher(user=user, name=name, address=address, city=city)
            Publisher_User.save()

            user_type = userType(user)
            username = user.username

            messages.success(request, f'A Publisher with username "{username}" was created!')
            messages.success(request, 'You are logged in!')
            login(request, user)
            return redirect('homeView', user_type, username)

        else:
            return render(request, 'book_app/Publisher/registration.html', {'form':form})
                
    form = PublisherForm()
    return render(request, 'book_app/Publisher/registration.html', {'form':form})

def contextPublisher(user):
    context={
        'username':user.username,
        'user_type':userType(user),
        'name':user.publisher.name,
        'email':user.email,
        'address':user.publisher.address,
        'city':user.publisher.city
    }

    return context

@login_required(login_url='/library/login/')
def authorsView(request):
    username = request.user.username
    user_type = userType(request.user)
    data = {}
    authors = []

    publisher = Publisher.objects.get(user=request.user)
    books = Book.objects.filter(publisher=publisher)
    for book in books:
        for author in book.authors.all():
            if author not in authors:
                authors.append(author)
    
    data['authors'] = authors
    data['user_type'] = user_type 
    data['username'] = request.user.username

    return render(request, 'book_app/Publisher/authors.html', data)  
