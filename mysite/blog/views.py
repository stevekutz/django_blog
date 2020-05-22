from django.shortcuts import render, get_object_or_404
from .models import Post

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def post_list(request):
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, 
                             slug = post, 
                             status = 'published', 
                             publish__year = year,
                             publish__month = month,
                             publish__day = day)    

    context = {'post': post}

    return render(request, 'blog/post/detail.html', context)   

def post_lisst(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)   # provide 3 posts per page                          
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:    
        # of page NOT an integer, provide first page
        posts = paginator.page(1)
    except EmptyPage:
        # if Page is out of range, provide last page    
        posts = paginator.page(paginator.num_pages)