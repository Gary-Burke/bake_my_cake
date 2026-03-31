from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from checkout.models import OrderLineItem
from .models import UserProfile
from .forms import UserProfileForm
from datetime import date

# Create your views here.


@login_required
def profile(request):
    """
    Get or create instance of :model:`profiles.UserProfile`

    **Context**
    ``userprofile_form``
    An instance of :form:`profiles.UserProfileForm`

    ``current_path``
    Used to determine queryset filter based on dates and
    update the template selected class for the links

    **Template**
    :template:`profiles/profile.html`
    """

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

    if not request.GET.get("path"):
        path = "profile"
    else:
        path = request.GET.get("path")

    template = "profiles/profile.html"

    context = {
        "userprofile_form": userprofile_form,
        "current_path": path,
    }

    return render(request, template, context)


class ItemListView(LoginRequiredMixin, ListView):
    """
    Returns all products in :model:`checkout.OrderLineItem`
    that are related to :model:`profiles.UserProfile`

    **Context**

    ``path / current_path``
    Used to determine queryset filter based on dates and
    update the template selected class for the links

    ``queryset``
    All instances of products in :model:`checkout.OrderLineItem`:
    - related to :model:`profiles.UserProfile`
    - filtered by path

    **Template**
    :template:`profiles/profile.html`
    """

    context_object_name = "order_list"
    template_name = "profiles/profile.html"

    def get_queryset(self):
        queryset = OrderLineItem.objects.filter(
            order__user_profile__user=self.request.user)

        path = self.request.GET.get("path") or "orders_current"
        today = date.today()

        if path == "orders_history":
            queryset = queryset.filter(created_on__lt=today)
        else:
            queryset = queryset.filter(created_on__gte=today)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path = self.request.GET.get("path") or "orders_current"
        context["current_path"] = path
        return context
