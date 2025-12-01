from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import StickyNote

@login_required
def sticky_wall(request):
    notes = StickyNote.objects.filter(owner=request.user).order_by("-pinned", "-id")
    return render(request, "sticky/wall.html", {"notes": notes})

@login_required
def create_note(request):
    if request.method == "POST":
        StickyNote.objects.create(
            owner=request.user,
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            color=request.POST.get("color"),
        )
        return redirect("sticky:wall")

    return redirect("sticky:wall")

@login_required
def edit_note(request, pk):
    note = get_object_or_404(StickyNote, id=pk, owner=request.user)

    if request.method == "POST":
        note.title = request.POST.get("title")
        note.description = request.POST.get("description")
        note.color = request.POST.get("color")
        note.save()
        return redirect("sticky:wall")

    return render(request, "sticky/edit.html", {"note": note})

@login_required
def delete_note(request, pk):
    note = get_object_or_404(StickyNote, id=pk, owner=request.user)
    note.delete()
    return redirect("sticky:wall")

@login_required
def pin_note(request, pk):
    note = get_object_or_404(StickyNote, id=pk, owner=request.user)
    note.pinned = not note.pinned
    note.save()
    return redirect("sticky:wall")
