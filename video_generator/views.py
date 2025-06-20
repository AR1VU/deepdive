import os
import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse, FileResponse
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
import subprocess
import requests
import openai
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordChangeForm
from .models import CustomUser

# Render the form for user input
def input_form(request):
    return render(request, 'video_generator/form.html')

# Generate video and display it
def generate_video(request):
    # Check if the user has enough credits
    if request.user.is_authenticated:
        if request.user.credits <= 0:
            return render(request, 'video_generator/form.html', {"error": "You do not have enough credits to generate a video.", "user": request.user})
        request.user.credits -= 1
        request.user.save()

    # Get user input from the request
    user_input = request.GET.get("input", "Default math explanation")

    # Check if the user input matches a predefined video
    predefined_videos = {
        "Simple Harmonic Motion": "SimpleHarmonicMotion.mp4",
        "Simple Harmonic Motion using Reference Circle": "SimpleHarmonicMotionUsingReferenceCircle.mp4",
        "Superposition": "SuperpositionExplanation.mp4",
        "Torque on a Dipole": "TorqueonaDipole.mp4",
        "Magnetic Field due to Electric Current":"MagneticFieldduetoElectricCurrent.mp4",
        "Explain Chain Rule": "ChainRule.mp4",
    }

    if user_input in predefined_videos:
        video_filename = predefined_videos[user_input]
        video_url = os.path.join(settings.MEDIA_URL, "videos", video_filename)
        return render(request, 'video_generator/form.html', {"video_url": video_url})

    # Show loading screen while generating video
    if request.GET.get("loading") != "1":
        # Redirect to same page with loading=1 to trigger loading screen
        params = request.GET.copy()
        params["loading"] = "1"
        return render(request, 'video_generator/form.html', {"loading": True, "input": user_input})

    # Initialize OpenAI ChatGPT client
    openai.api_key = os.getenv("OPENAI_API_KEY")  # Load from environment variable

    # Call OpenAI ChatGPT API to generate Manim code
    try:
        prompt_path = os.path.join(settings.BASE_DIR, "prompt.txt")
        if not os.path.exists(prompt_path):
            return render(request, 'video_generator/form.html', {"error": "Prompt file not found."})
        with open(prompt_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()
        response = openai.ChatCompletion.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        manim_code = response['choices'][0]['message']['content']
    except Exception as e:
        return render(request, 'video_generator/form.html', {"error": "Failed to generate Manim code", "details": str(e)})

    if not manim_code:
        return render(request, 'video_generator/form.html', {"error": "No Manim code generated"})

    # Save the script to a temporary file
    script_path = os.path.join(settings.BASE_DIR, "temp_manim_script.py")
    with open(script_path, "w", encoding="utf-8") as script_file:
        script_file.write(manim_code)

    # Output video path
    output_dir = os.path.join(settings.MEDIA_ROOT, "videos")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "example_scene.mp4")

    # Run Manim to generate the video
    try:
        subprocess.run([
            "manim", script_path, "ExampleScene", "-o", output_path, "--format=mp4"
        ], check=True)
    except subprocess.CalledProcessError as e:
        return render(request, 'video_generator/form.html', {"error": "Failed to generate video", "details": str(e)})

    # Return the form with the video embedded
    video_url = os.path.join(settings.MEDIA_URL, "videos", "example_scene.mp4")
    return render(request, 'video_generator/form.html', {"video_url": video_url})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('input_form')  # Redirect to the input form after signup
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'login.html'

@login_required
def account_view(request):
    user = request.user
    password_form = CustomPasswordChangeForm(user)
    password_changed = False
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        old_password = request.POST.get('old_password')
        # Update name/email if changed
        if name:
            user.name = name  # Save to the correct field
        if email:
            user.email = email
        user.save()
        # Only process password change if new password fields are filled
        if new_password1 or new_password2 or old_password:
            password_form = CustomPasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                password_changed = True
            else:
                messages.error(request, 'Please correct the error below.')
        if not password_changed:
            messages.success(request, 'Profile updated successfully!')
    return render(request, 'account.html', {
        'user': user,
        'password_form': password_form
    })

@login_required
def buy_credits(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        try:
            credits_to_add = int(request.POST.get('credits', 0))
            if credits_to_add > 0:
                # Create payment intent with Ziina
                amount = credits_to_add  # 1 credit = 1 AED
                headers = {
                    'Authorization': f'Bearer {os.getenv("ZIINA_API_KEY")}',
                    'Content-Type': 'application/json'
                }
                payload = {
                    'amount': amount*100,
                    'currency_code': 'AED',
                    'message': f'Buy {credits_to_add} credits',
                    'success_url': request.build_absolute_uri('/buy-credits/success/?credits=' + str(credits_to_add)),
                    'cancel_url': request.build_absolute_uri('/buy-credits/cancel/'),
                    'failure_url': request.build_absolute_uri('/buy-credits/failure/'),
                    'test': True,  # Set to False in production
                    'transaction_source': 'directApi'
                }
                response = requests.post('https://api-v2.ziina.com/api/payment_intent', headers=headers, json=payload)
                print('Ziina API status:', response.status_code)
                print('Ziina API response:', response.text)
                data = response.json()
                payment_url = data.get('redirect_url')  
                if payment_url:
                    return redirect(payment_url)
                else:
                    messages.error(request, 'Failed to initiate payment. Please try again.')
            else:
                messages.error(request, 'Please enter a positive number of credits.')
        except Exception as e:
            messages.error(request, f'Invalid input or payment error: {e}')
        return redirect('buy_credits')
    return render(request, 'video_generator/buy_credits.html', {'user': request.user})

@login_required
def buy_credits_success(request):
    credits = int(request.GET.get('credits', 0))
    if credits > 0:
        request.user.credits += credits
        request.user.save()
        messages.success(request, f'Successfully added {credits} credits!')
    else:
        messages.error(request, 'No credits were added.')
    return redirect('buy_credits')

@login_required
def buy_credits_cancel(request):
    messages.info(request, 'Payment was cancelled.')
    return redirect('buy_credits')

@login_required
def buy_credits_failure(request):
    messages.error(request, 'Payment failed. Please try again.')
    return redirect('buy_credits')
