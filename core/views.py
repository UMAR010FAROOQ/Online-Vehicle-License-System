import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate, login as auth_login
from django.views import View
from .models import LearnerApply,ChangePassword,LearningMaterial,FeeStructure
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import now
import requests
# Create your views here.


def HomePage(request):
        return render(request, 'index.html')


def LearningMaterialPage(request):
    materials = LearningMaterial.objects.all()
    return render(request, 'LearningMaterial.html', {'materials': materials})

@login_required
def FeeStructurePage(request):
        feeStr = FeeStructure.objects.all()
        return render(request, 'feeStructure.html', {'feeStr': feeStr})

@login_required
def SampleTestPage(request):
        return render(request, 'SampleTest.html')

@login_required
def TrackApplicationPage(request):
        return render(request, 'TrackApplication.html')

@login_required
def VerifyLicensePage(request):
        return render(request, 'VerifyLicense.html')

@login_required
def LearnerApplicationPage(request):
    applications = LearnerApply.objects.all()
    context = {'applications': applications}
    return render(request, 'LearnerApplication.html', context)

@login_required
def LearnerApplyPage(request):
        if request.method == 'POST':
                user = request.user
                cnic = request.POST['cnic']
                full_name = request.POST['fullName']
                father_name = request.POST['fatherName']
                dob = request.POST['dob']
                phone_number = request.POST['phoneNumber']
                height = request.POST['height']
                gender = request.POST['gender']
                citizen_type = request.POST['citizenType']
                vehicle_type = request.POST['vehicleType']
                nationality = request.POST['nationality']
                blood_group = request.POST['bloodGroup']
                disability = request.POST['disability']
                category = request.POST['category']
                permanent_province = request.POST['permanentProvince']
                permanent_district = request.POST['permanentDistrict']
                permanent_address = request.POST['permanentAddress']
                current_province = request.POST['currentProvince']
                current_district = request.POST['currentDistrict']
                current_address = request.POST['currentAddress']
                
                user_profile_img = request.FILES['userProfileImg']
                id_front_side = request.FILES['IDfrontSide']
                id_back_side = request.FILES['IDbackSide']

                learner_application_data = LearnerApply(user=user,cnic=cnic,full_name=full_name,father_name=father_name,dob=dob,phone_number=phone_number,height=height,gender=gender,citizen_type=citizen_type,vehicle_type=vehicle_type,nationality=nationality,blood_group=blood_group,
                disability=disability,category=category,permanent_province=permanent_province,permanent_district=permanent_district,permanent_address=permanent_address,current_province=current_province,current_district=current_district,
                current_address=current_address,user_profile_img=user_profile_img,id_front_side=id_front_side,id_back_side=id_back_side)
                learner_application_data.save()
                return redirect('core:success_page')  # Redirect to a success page

        return render(request, 'LearnerApply.html')


@login_required
def SuccessPage(request):
    return render(request, 'success.html')

def user_registration(request):
        if request.method == 'POST':
                user_name = request.POST.get("user_name")
                email = request.POST.get("email")
                password1 = request.POST.get("password1")
                password2 = request.POST.get("password2")

                if password1 == password2:
                        if User.objects.filter(username =user_name).exists():
                                messages.info(request,'Username Taken')
                                return redirect('core:user_registration')
                        elif User.objects.filter(email = email).exists():
                                messages.info(request,'Email Taken')
                                return redirect('core:user_registration')
                        else:
                                user = User.objects.create_user(username = user_name, email=email, password = password1)
                                user.save()
                                print('User Created')
                                print(user_name)
                                return redirect('core:login')

                else:
                        print("password not matching...")
                        messages.info(request,'Password not matching')
                        return redirect('core:user_registration')
        else:
                return render(request, 'signup.html')              


def login(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        return redirect("/")
    
    if request.method == 'POST':
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")
        remember_me = request.POST.get('remember_me')  # Get the 'Remember Me' value
        recaptcha_response = request.POST.get('g-recaptcha-response')

        # Verify reCAPTCHA
        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if result['success']:
            user = authenticate(username=user_name, password=password)
            if user is not None:
                auth_login(request, user)

                if remember_me:
                    # Set session expiry to 7 days
                    request.session.set_expiry(604800)  # 7 days in seconds
                else:
                    # Set session expiry to browser close
                    request.session.set_expiry(0)

                return redirect("/")
            else:
                messages.info(request, 'Invalid credentials')
        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')

        return redirect('core:login')
    else:
        return render(request, 'login.html', {'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY})


def logout(request):
        auth.logout(request)
        return redirect('core:login') 


def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        associated_users = User.objects.filter(email=email)
        if associated_users.exists():
            for user in associated_users:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = request.build_absolute_uri(
                    reverse('core:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                )
                subject = 'Password Reset Requested'
                html_content = render_to_string('password_reset_email.html', {
                    'user': user,
                    'reset_link': reset_link,
                })
                text_content = strip_tags(html_content)
                
                email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
                email.attach_alternative(html_content, "text/html")
                email.send()
            messages.success(request, 'An email has been sent with instructions to reset your password.')
        else:
            messages.error(request, 'No user is associated with this email address.')
        return redirect('core:password_reset')
    return render(request, 'password_reset.html')

def password_reset_confirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been set. You may go ahead and log in now.')
                return redirect('core:login')
        else:
            form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'The password reset link was invalid, possibly because it has already been used.')
        return redirect('core:password_reset')
        

def password_reset_complete(request):
    return render(request, 'password_reset_complete.html')



@login_required
def change_password(request):
    user = request.user
    last_change = ChangePassword.objects.filter(user=user).order_by('-timestamp').first()

    if last_change:
        time_since_last_change = now() - last_change.timestamp
        remaining_time = timedelta(hours=24) - time_since_last_change
    else:
        remaining_time = timedelta()

    if remaining_time > timedelta():
        remaining_seconds = int(remaining_time.total_seconds())
        google_extra_data = user.social_auth.get(provider='google-oauth2').extra_data if user.social_auth.filter(provider='google-oauth2').exists() else None
        context = {
            'remaining_seconds': remaining_seconds,
            'google_extra_data': google_extra_data,
        }
        return render(request, 'change_password.html', context)

    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            ChangePassword.objects.create(user=user)  # Save the timestamp of the password change
            update_session_auth_hash(request, user)  # Important to maintain the user's session
            messages.success(request, 'Your password was successfully updated!')
            return redirect('core:change_password')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:
        form = PasswordChangeForm(user)

    google_extra_data = user.social_auth.get(provider='google-oauth2').extra_data if user.social_auth.filter(provider='google-oauth2').exists() else None
    # print(google_extra_data)
    return render(request, 'change_password.html', {'form': form, 'google_extra_data': google_extra_data})

# @login_required
# def change_password(request):
#     user = request.user
#     last_change = ChangePassword.objects.filter(user=user).order_by('-timestamp').first()

#     if last_change:
#         time_since_last_change = now() - last_change.timestamp
#         remaining_time = timedelta(hours=24) - time_since_last_change
#     else:
#         remaining_time = timedelta()

#     if remaining_time > timedelta():
#         remaining_seconds = int(remaining_time.total_seconds())
#         context = {'remaining_seconds': remaining_seconds}
#         return render(request, 'change_password.html', context)
    
#     if request.method == 'POST':
#         form = PasswordChangeForm(user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             ChangePassword.objects.create(user=user)  # Save the timestamp of the password change
#             update_session_auth_hash(request, user)  # Important to maintain the user's session
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('core:change_password')
#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f'{field.capitalize()}: {error}')
#     else:
#         form = PasswordChangeForm(user)
    
#     return render(request, 'change_password.html', {'form': form})