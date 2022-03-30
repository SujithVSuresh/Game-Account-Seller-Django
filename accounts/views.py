from xml.dom import VALIDATION_ERR
from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.views import View
from django.http import HttpResponse
from .forms import UserSignupForm, UserLoginForm
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.utils.http import urlsafe_base64_decode


class UserSignupView(CreateView):
    model = User
    template_name = 'accounts/signup.html'
    #permission_required = 'employee.can_add_employee'
    form_class = UserSignupForm
    #success_message = 'Blog post created successfully..'
    success_url = reverse_lazy('accounts:login')  

def acc_activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    #if user is not None and account_activation_token.check_token(user, token):
    if user is not None:
        user.is_active = True
        user.save()
        login(request, user)
        #return redirect('home')
        return redirect('core:home')
    else:
        return HttpResponse('Activation link is invalid!')    
                    

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'  

class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:login')  


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "accounts/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("accounts:password_reset_done")                         
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="accounts/password_reset.html", context={"password_reset_form":password_reset_form})                      
