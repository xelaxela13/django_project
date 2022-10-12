from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from feedbacks.model_forms import FeedbackModelForm
from feedbacks.models import Feedback


@login_required
def feedbacks(request, *args, **kwargs):
    user = request.user
    if request.method == 'POST':
        form = FeedbackModelForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('main'))
    else:
        form = FeedbackModelForm(user=user)
    context = {
        'feedbacks': Feedback.objects.all(),
        'form': form
    }
    return render(request, 'feedbacks/index.html', context)
