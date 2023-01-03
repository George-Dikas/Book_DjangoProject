from django.urls import path
from . import views

urlpatterns = [
    # Common paths
    path('login/', views.loginView, name='loginView'),
    path('logout/', views.logoutView, name='logoutView'),
    path('home/<str:user_type>/<str:username>/', views.homeView, name='homeView'),
    path('personal_info/', views.infoView, name='infoView'),
    path('delete_profile/', views.delProfView, name='delProfView'),
    
    # Common paths for Authors and Publishers
    path('new_book/', views.addBookView, name='addBookView'),
    path('edit_book/<int:book_id>', views.editBookView, name='editBookView'),
    path('delete_book/<int:book_id>', views.deleteBookView, name='deleteBookView'),
    
    # Library User paths
    path('registration/library_user/', views.regLibUserView, name='regLibUserView'),
    path('add_favourite/<int:book_id>', views.addFavouriteView, name='addFavouriteView'),
    path('remove_favourite/<int:book_id>', views.removeFavouriteView, name='removeFavouriteView'),
    path('rate/<int:book_id>', views.rateView, name='rateView'),
    path('favourites/', views.favouritesView, name='favouritesView'),
    
    # Author paths
    path('registration/author/', views.regAuthorView, name='regAuthorView'),
    
    # Publisher paths
    path('registration/publisher/', views.regPublisherView, name='regPublisherView'),
    path('authors/', views.authorsView, name='authorsView'),
]
