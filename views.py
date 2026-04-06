from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import ExpenseForm
from .models import Expense


def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        user.save()

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'expenses/signup.html')

def login_view(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'expenses/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user).order_by("-date")

    context = {
        "expenses": expenses
    }

    return render(request, "expenses/dashboard.html", context)


@login_required
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)

        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()

            return redirect("dashboard")

    else:
        form = ExpenseForm()

    context = {
        "form": form,
        "title": "Add Expense",
        "button_text": "Save Expense"
    }

    return render(request, "expenses/expense_form.html", context)


@login_required
def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
        form = ExpenseForm(instance=expense)

    context = {
        "form": form,
        "title": "Edit Expense",
        "button_text": "Update Expense"
    }

    return render(request, "expenses/expense_form.html", context)


@login_required
def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == "POST":
        expense.delete()
        return redirect("dashboard")

    return render(request, "expenses/delete_expense.html", {"expense": expense})
