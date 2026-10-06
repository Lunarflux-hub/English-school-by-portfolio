from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=66,
                             widget=forms.EmailInput(
                                 attrs={"class": 'input-register form-control', 'placeholder': 'Your email'}))
    first_name = forms.CharField(required=True, max_length=20,
                                 widget=forms.TextInput(  # ИСПРАВЛЕНО: TextInput
                                     attrs={"class": 'input-register form-control', 'placeholder': 'Your first name'}))
    last_name = forms.CharField(required=True, max_length=20,
                                widget=forms.TextInput(  # ИСПРАВЛЕНО: TextInput
                                    attrs={"class": 'input-register form-control', 'placeholder': 'Your last name'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(  # ИСПРАВЛЕНО: PasswordInput
        attrs={"class": 'input-register form-control', 'placeholder': 'Your password'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(  # ИСПРАВЛЕНО: PasswordInput
        attrs={"class": 'input-register form-control', 'placeholder': 'Confirm your password'}))

    marketing_consent = forms.BooleanField(required=False,
                                           label='i agree to receive commercial, promotion and marketing communications.',
                                           widget=forms.CheckboxInput(attrs={'class': 'checkbox-input-register'}))
    personaldata_consent = forms.BooleanField(required=True,
                                              label='i agree to provide my personal data.',
                                              widget=forms.CheckboxInput(attrs={'class': 'checkbox-input-register'}))

    class Meta:  # ИСПРАВЛЕНО: отступ
        model = User
        # ИСПРАВЛЕНО: убрано дублирование marketing_consent
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'marketing_consent',
                  'personaldata_consent')

    def clean_email(self):  # ИСПРАВЛЕНО: метод внутри формы
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use')
        return email

    def save(self, commit=True):  # ИСПРАВЛЕНО: метод внутри формы
        user = super().save(commit=False)
        # user.username = None # Этого делать не нужно, так как username = None уже задан в модели
        user.marketing_consent = self.cleaned_data['marketing_consent']
        user.personaldata_consent = self.cleaned_data['personaldata_consent']
        if commit:
            user.save()
        return user


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email',
                               widget=forms.TextInput(attrs={'autofocus': True, 'class': 'input-register form-control',
                                                             'placeholder': 'Your email'}))

    password = forms.CharField(label="Password", widget=forms.PasswordInput(  # ИСПРАВЛЕНО: PasswordInput
        attrs={'autofocus': True, 'class': 'input-register form-control', 'placeholder': 'Your password'}))

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            # ИСПРАВЛЕНО: Django ModelBackend ожидает username, а не email
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Invalid email or password')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('This account is inactive')
        return self.cleaned_data


class CustomUserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=True, max_length=50, widget=forms.TextInput(
        attrs={'class': 'input-register form-control', 'placeholder': 'Your first name'}))
    last_name = forms.CharField(required=True, max_length=50, widget=forms.TextInput(
        attrs={'class': 'input-register form-control', 'placeholder': 'Your last name'}))
    email = forms.EmailField(required=False, widget=forms.TextInput(
        attrs={'class': 'input-register form-control', 'placeholder': 'Your email'}))

    class Meta:  # ИСПРАВЛЕНО: отступ
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'input-register form-control', 'placeholder': 'Your email'}),
            'first_name': forms.TextInput(
                attrs={'class': 'input-register form-control', 'placeholder': 'Your first name'}),
            'last_name': forms.TextInput(
                attrs={'class': 'input-register form-control', 'placeholder': 'Your last name'}),
        }

    def clean_email(self):  # ИСПРАВЛЕНО: метод внутри формы
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('This email already in use.')
        return email

    def clean(self):  # ИСПРАВЛЕНО: метод внутри формы
        cleaned_data = super().clean()
        if not cleaned_data.get('email'):
            cleaned_data['email'] = self.instance.email
        return cleaned_data