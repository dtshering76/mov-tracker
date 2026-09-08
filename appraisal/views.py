from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Standard, MOV, AppraisalPeriod, Submission


@login_required
def dashboard(request):
    period = AppraisalPeriod.objects.filter(is_active=True).first()

    # Instead of just IDs, store a dict: {mov_id: status}
    submissions_by_mov = {}
    if period:
        subs = Submission.objects.filter(teacher=request.user, period=period)
        submissions_by_mov = {s.mov_id: s.status for s in subs}

    standards = Standard.objects.prefetch_related('focus_areas__movs')

    context = {
        'standards': standards,
        'period': period,
        'submissions_by_mov': submissions_by_mov,
    }
    return render(request, 'dashboard.html', context)

@login_required
def submit_mov(request, mov_id):
    """Lets a teacher upload a file as evidence for one specific MOV."""

    mov = get_object_or_404(MOV, id=mov_id)
    period = AppraisalPeriod.objects.filter(is_active=True).first()

    if not period:
        messages.error(request, "No active appraisal period right now.")
        return redirect('dashboard')

    # Check if a submission already exists (so we can let them replace it)
    existing = Submission.objects.filter(teacher=request.user, mov=mov, period=period).first()

    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        remarks = request.POST.get('remarks', '')

        if not uploaded_file:
            messages.error(request, "Please choose a file to upload.")
        else:
            if existing:
                existing.file = uploaded_file
                existing.remarks = remarks
                existing.status = 'pending'  # reset to pending since it changed
                existing.save()
                messages.success(request, "Your submission was updated.")
            else:
                Submission.objects.create(
                    teacher=request.user,
                    mov=mov,
                    period=period,
                    file=uploaded_file,
                    remarks=remarks,
                )
                messages.success(request, "Your evidence was submitted.")
            return redirect('dashboard')

    context = {'mov': mov, 'existing': existing, 'period': period}
    return render(request, 'submit_mov.html', context)