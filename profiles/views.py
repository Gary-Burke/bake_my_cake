from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserProfileForm

# Create your views here.


@login_required
def profile(request):

    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        userprofile_form = UserProfileForm(request.POST, instance=profile)
        if userprofile_form.is_valid():
            userprofile_form.save()
            messages.add_message(
                request, messages.SUCCESS,
                "Your profile has been successfully updated!"
            )
        else:
            messages.add_message(
                request, messages.ERROR,
                "Unable to update your profile. Please fill out the form again"
            )
    else:
        userprofile_form = UserProfileForm(instance=profile)

    template = "profiles/profile.html"
    context = {
        "userprofile_form": userprofile_form,
        "path": "profile"
    }

    return render(request, template, context)
