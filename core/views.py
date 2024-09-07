from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Count

from core.models import FeedBack, SubmittedWork, Supervisor, CustomUser
from .forms import FeedBackForm, SubmittedWorkForm


# Create your views here.
def redirect_to_login(request):
    return redirect("login")


def login_user(request):
    user_id = request.POST.get("identifier")
    password = request.POST.get("password")
    role = request.POST.get("role")
    email = request.POST.get("email")

    if request.method == "POST":
        if role:

            user = authenticate(
                request, email=email, password=password, user_id=user_id
            )

            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(f"{role}_dashboard")
            messages.error(request, "Invalid credentials provided")
            return redirect("login")
        messages.error(request, "All fields are required")
        return redirect("login")
    return render(request, "core/login.html")


@login_required(login_url="login")
def student_dashboard(request):
    auth_user = request.user

    if auth_user.user_type == "student":
        if request.method == "POST":

            user_assignment_form = SubmittedWorkForm(
                data=request.POST, files=request.FILES
            )
            try:
                work = SubmittedWork.objects.get(student=auth_user)
            except SubmittedWork.DoesNotExist:
                #  no work submitted
                if user_assignment_form.is_valid():
                    submiited_work = user_assignment_form.save(commit=False)

                    submiited_work.student = auth_user

                    # save work to the database
                    submiited_work.save()
                    messages.success(request, "Work submitted successfully")
                    return redirect("student_dashboard")

            # updating work
            update_form = SubmittedWorkForm(
                data=request.POST, files=request.FILES, instance=work
            )
            if update_form.is_valid():
                update_form.save()
                messages.success(request, "Work submitted updated")
                return redirect("student_dashboard")

        # get supervisor info of user
        supervisor_info = Supervisor.objects.filter(student=auth_user)
        form = SubmittedWorkForm()

        feedbacks = FeedBack.objects.filter(student=request.user)
        context = {
            "supervisor_info": supervisor_info,
            "form": form,
            "feedbacks": feedbacks,
        }
        return render(request, "core/student_dashboard.html", context)
    return HttpResponseForbidden("You are not allowed to view this resources")


@login_required(login_url="login")
def coordinator_dashboard(request):

    if request.user.user_type == "coordinator":

        if request.method == "POST":
            student_id = request.POST.get("student")
            supervior_id = request.POST.get("supervisor")

            try:
                # get student
                curr_student = get_user_model().objects.get(id=student_id)
                curr_supervisor = get_user_model().objects.get(id=supervior_id)

                Supervisor.objects.create(
                    supervisor=curr_supervisor, student=curr_student
                )

            except Exception as e:
                print(str(e))
                messages.error(request, str(e))
                return redirect("coordinator_dashboard")

        students = get_user_model().objects.filter(
            user_type=CustomUser.UserType.STUDENT, is_active=True
        )
        supervisors = get_user_model().objects.filter(
            user_type=CustomUser.UserType.SUPERVISOR, is_active=True
        )

        statistics = (
            FeedBack.objects.values("grade")
            .annotate(total=Count("grade"))
            .order_by("-total")
        )

        context = {
            "students": students,
            "supervisors": supervisors,
            "statistics": statistics,
        }
        print(statistics, "this is the stat")
        return render(request, "core/coordinator_dashboard.html", context)

    return HttpResponseForbidden("You are not allowed to view this resources")


@login_required(login_url="login")
def supervisor_dashboard(request):

    supervisor = request.user

    if supervisor.user_type == "supervisor":

        if request.method == "POST":

            form = FeedBackForm(data=request.POST)

            if form.is_valid():
                form.save()

                messages.success(request, "Feedback sent successfully!")
                return redirect("supervisor_dashboard")

            messages.error(request, "couldn't send feedback. Try again")
            return redirect("supervisor_dashboard")

        supervisor_students = Supervisor.objects.filter(supervisor=supervisor)
        students = [student.student for student in supervisor_students]
        works = SubmittedWork.objects.filter(student__in=students)

        form = FeedBackForm()

        context = {"students": supervisor_students, "form": form, "works": works}

        return render(request, "core/supervisor_dashboard.html", context)
    return HttpResponseForbidden(
        "You do not have the permission to access this resources"
    )


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/login/")
