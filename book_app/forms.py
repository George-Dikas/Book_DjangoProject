from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from book_app.models import Book, Publisher
from django.forms.widgets import NumberInput
from datetime import date


# Common forms
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)

    class Meta:
        widgets = { 
            'password':forms.PasswordInput(),
        }


# Library User forms
class LibraryUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(LibraryUserForm,self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'autofocus': True})
        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs.update({'autocomplete': 'text-input'})
        
        self.fields['last_name'].required = True
        self.fields['last_name'].widget.attrs.update({'autocomplete': 'text-input'})
        
        self.fields['username'].widget.attrs.update({'autocomplete': 'text-input'})

        self.fields['email'].required = True
        self.fields['email'].widget.attrs.update({'autocomplete': 'text-input'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email):
            raise forms.ValidationError('This email is already taken.')
        return email

class LibraryUpdateForm(UserChangeForm):
    password = None
 
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(LibraryUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autocomplete': 'text-input'})
        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs.update({'autocomplete': 'text-input'})
        self.fields['last_name'].required = True
        self.fields['last_name'].widget.attrs.update({'autocomplete': 'text-input'})
        self.fields['email'].required = True
        self.fields['email'].widget.attrs.update({'autocomplete': 'text-input'})
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        self.email = self.initial.get('email')
        
        if User.objects.filter(email=email).exclude(email=self.email):
            raise forms.ValidationError('This email is already taken.')
        return email


# Author forms
class AuthorForm(UserCreationForm):
    age = forms.IntegerField(widget=forms.TextInput(attrs={'autocomplete':'off'}))

    class Meta:
        model = User 
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'autofocus': True})
        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs.update({'autocomplete': 'text-input'})

        self.fields['last_name'].required = True
        self.fields['last_name'].widget.attrs.update({'autocomplete': 'text-input'})

        self.fields['username'].widget.attrs.update({'autocomplete': 'text-input'})

        self.fields['email'].required = True
        self.fields['email'].widget.attrs.update({'autocomplete': 'text-input'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email):
            raise forms.ValidationError('This email is already taken.')
        return email

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age<18:
            raise forms.ValidationError('Age<18')
        return age

class AuthorUpdateForm(UserChangeForm):
    password = None
    age = forms.IntegerField(widget=forms.TextInput(attrs={'autocomplete':'off'}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'age', 'email')

    def __init__(self, *args, **kwargs):
        super(AuthorUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autocomplete': 'text-input'})
        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs.update({'autocomplete': 'text-input'})
        self.fields['last_name'].required = True
        self.fields['last_name'].widget.attrs.update({'autocomplete': 'text-input'})
        self.fields['email'].required = True
        self.fields['email'].widget.attrs.update({'autocomplete': 'text-input'})
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        self.email = self.initial.get('email')
        
        if User.objects.filter(email=email).exclude(email=self.email):
            raise forms.ValidationError('This email is already taken.')
        return email

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age<18:
            raise forms.ValidationError('Age<18')
        return age


# Publisher forms
class PublisherForm(UserCreationForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'text-input'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'text-input'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'text-input'}))

    class Meta:
        model = User 
        fields = ('email', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(PublisherForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'autofocus': True})
        self.fields['username'].widget.attrs.update({'autocomplete': 'text-input'})
        self.fields['email'].required = True
        self.fields['email'].widget.attrs.update({'autocomplete': 'text-input'})

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Publisher.objects.filter(name=name):
            raise forms.ValidationError('There is already a publisher with this name.')
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email):
            raise forms.ValidationError('This email is already taken.')
        return email

class PublisherUpdateForm(UserChangeForm):
    password = None
    name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'text-input'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'text-input'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'text-input'}))
    
    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'address', 'city')
    
    def __init__(self, *args, **kwargs):
        super(PublisherUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autocomplete': 'text-input'})
        self.fields['email'].required = True
        self.fields['email'].widget.attrs.update({'autocomplete': 'text-input'})

    def clean_name(self):
        name = self.cleaned_data.get('name')
        username = self.initial.get('username')
        publisher = Publisher.objects.get(user=User.objects.get(username=username))
        
        if Publisher.objects.filter(name=name).exclude(name=publisher.name):
            raise forms.ValidationError('There is already a publisher with this name.')
        return name
     
    def clean_email(self):
        email = self.cleaned_data.get('email')
        self.email = self.initial.get('email')
        
        if User.objects.filter(email=email).exclude(email=self.email):
            raise forms.ValidationError('This email is already taken.')
        return email


# Book forms
class BookForm(forms.ModelForm):
    pub_date = forms.DateField(widget = NumberInput(attrs={'type': 'date'}), label='Publication date')

    class Meta:
        model = Book
        fields = ('title', 'publisher', 'authors', 'pub_date', 'book')

        widgets = { 
            'authors':forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        super(BookForm,self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'autofocus': True})

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if (Book.objects.filter(title=title)):
            raise forms.ValidationError('There is already a book with this title.')
        return title

    def clean_pub_date(self):
        first_date = date(1990, 1, 1)
        pub_date = self.cleaned_data.get('pub_date')

        if (pub_date<first_date or pub_date>date.today()):
            raise forms.ValidationError('The date must be between 1/1/1990 and today.')
        return pub_date

class BookEditForm(forms.ModelForm):
    pub_date = forms.DateField(widget = NumberInput(attrs={'type': 'date'}), label='Publication date')

    class Meta:
        model = Book
        fields = ('title', 'pub_date')

    def clean_title(self):
        title = self.cleaned_data.get('title')
        self.title = self.initial.get('title')
        
        if Book.objects.filter(title=title).exclude(title=self.title):
            raise forms.ValidationError('There is already a book with this title.')
        return title

    def clean_pub_date(self):
        first_date = date(1990, 1, 1)
        pub_date = self.cleaned_data.get('pub_date')
        
        if (pub_date<first_date or pub_date>date.today()):
            raise forms.ValidationError('The date must be between 1/1/1990 and today.')
        return pub_date
