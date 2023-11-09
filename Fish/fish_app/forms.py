from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Video,Order,Profile,Customer



class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = ('price', 'quantity', 'place','fish_species','date')
		price = forms.IntegerField(
	   		label="價錢",
	    	widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width:50%;'})
		)
		quantity = forms.IntegerField(
	        label="數量",
	        widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width:50%;'})
		)
		place = forms.CharField(
	        label="交易市場",
	        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%;'})
		)
		fish_species = forms.CharField(
	        label="魚種",
	        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%;'})
		)
		date = forms.DateField(
	        label="交易日期",
	        widget=forms.DateInput(attrs={'class': 'form-control', 'style': 'width:50%;',}),
		)



class CustomerForm(forms.ModelForm):
    class Meta:
        model =Customer
        fields = ('name', 'mobile', 'location')

        first_name = forms.CharField(
			label="姓名",
			widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%;'})
		)

        last_name = forms.CharField(
	        label="電話",
	        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%;'})
        )

        email = forms.EmailField(
	        label="地址",
	        widget=forms.EmailInput(attrs={'class': 'form-control', 'style': 'width:50%;'}),
        )



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

        first_name = forms.CharField(
			label="姓氏",
			widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%;'})
		)

        last_name = forms.CharField(
	        label="姓名",
	        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%;'})
        )

        email = forms.EmailField(
	        label="電子郵件",
	        widget=forms.EmailInput(attrs={'class': 'form-control', 'style': 'width:50%;'}),
        )




class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('mobile', 'location', 'birth_date')

        mobile = forms.CharField(
	        label="電話號碼",
	        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%;'})
        )

        location = forms.CharField(
	        label="地址",
	        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%;'})
        )

        birth_date = forms.DateField(
	        label="生日",
	        widget=forms.DateInput(attrs={'class': 'form-control', 'style': 'width:50%;'}),
        )


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(
            attrs={'class': 'login-input', 'placeholder': 'username'})
    )
    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(
            attrs={'class': 'login-input', 'placeholder': 'Email adress'})
    )
    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(
            attrs={'class': 'login-input', 'placeholder': 'password'})
    )
    password2 = forms.CharField(
        label="密碼確認",
        widget=forms.PasswordInput(
            attrs={'class': 'login-input', 'placeholder': 'password'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(
            attrs={'class': 'login-input', 'placeholder': 'username'})
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(
            attrs={'class': 'login-input', 'placeholder': 'password'})
    )
