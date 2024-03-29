from django.shortcuts import render, get_object_or_404
#from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User


#first step when we consider this dummy data is coming from some db
posts=[
    {
        'author':'Harshita',
        'title':'Post1',
        'content':'First post',
        'date':'02-10-2020'
    },
    {
        'author':'Saksham',
        'title':'Post2',
        'content':'Second post',
        'date':'02-10-2020'
    }
]


"""def home(request):
    #return HttpResponse('<h1>Blog Home</h1>')
    #first step when we consider this dummy data is coming from some db
    #context={
    #    'posts':posts
    #}
    #picking vale from db
    context={
        'posts':Post.objects.all()
    }
    return render(request,'blog/home.html',context)"""

class PostListView(ListView):
    model = Post
    # by default template name = modelName_list.html
    template_name = 'blog/home.html'    # <app>/<model>_<viewtype>.html
    # by default template variable name = modelName_list
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 2

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        # this will fetch the username from URL
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        # it will compare fetched username from URL with author of the posts
        return Post.objects.filter(author=user).order_by('-date')


class PostDetailView(DetailView):
    model = Post
    # by default in template we can access as object or modelName
    # by default template name is modelName_detail.html

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # without author we get integrity error
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    #return HttpResponse('<h1>About</h1>')
    return render(request,'blog/about.html',{'title':'About'})
