from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.utils.decorators import method_decorator
from django.views import View

from .forms import CustomUserCreationForm, loginForm
from .models import Blog

def home(request):
    return redirect('/login')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the new user with the extra fields
            messages.success(request, "Signup successful! You can now log in.")
            return redirect('/login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field} : {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/index')
        else:
            messages.error(request, "Incorrect username or password")
            return redirect('/login')
    else:
        form = loginForm()
    return render(request, 'login.html', {'form': form})

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class IndexView(View):
    def get(self, request):
        blogs = Blog.objects.filter(blogger=request.user)
        return render(request, 'index.html', {'blogs': blogs})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CreateBlogView(View):
    def get(self, request):
        # Render the empty form when the user visits the page
        return render(request, 'create_blog.html')

    def post(self, request):
        title = request.POST['title']
        content = request.POST['content']
        user = request.user
        Blog.objects.create(title=title, content=content, blogger=user)
        return redirect('/index')


class BlogDetailView(View):
    def get(self, request, id):
        # Retrieve the blog object by ID or return a 404 error if not found
        blog = get_object_or_404(Blog, id=id)
        return render(request, 'blog_detail.html', {'blog': blog})
