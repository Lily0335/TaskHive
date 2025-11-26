from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import StudySession
from .forms import StudySessionForm

@login_required
def study_list(request):
    sessions = StudySession.objects.filter(user=request.user)
    return render(request, "studytracker/study_list.html", {"sessions": sessions})

@login_required
def study_create(request):
    if request.method == "POST":
        form = StudySessionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect("studytracker:list")
    else:
        form = StudySessionForm()

    return render(request, "studytracker/study_form.html", {"form": form})

@login_required
def study_update(request, pk):
    session = get_object_or_404(StudySession, pk=pk, user=request.user)
    if request.method == "POST":
        form = StudySessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect("studytracker:list")
    else:
        form = StudySessionForm(instance=session)

    return render(request, "studytracker/study_form.html", {"form": form})

@login_required
def study_delete(request, pk):
    session = get_object_or_404(StudySession, pk=pk, user=request.user)
    if request.method == "POST":
        session.delete()
        return redirect("studytracker:list")

    return render(request, "studytracker/study_delete.html", {"session": session})
