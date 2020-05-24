from django.shortcuts import render, get_object_or_404
from .models import Post

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from .forms import EmailPostForm
from django.core.mail import send_mail

# Create your views here.
def post_list(request):
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
    
    
    context = {'page': page, 'posts': posts, }
    
    return render(request, 'blog/post/list.html', context)


class PostListView(ListView):
    model = Post
    # queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, 
                             slug = post, 
                             status = 'published', 
                             publish__year = year,
                             publish__month = month,
                             publish__day = day)    

    context = {'post': post}

    return render(request, 'blog/post/detail.html', context)   

def post_share(request, post_id):
    # Retrieve post by ID
    post = get_object_or_404(Post, id = post_id, status = "published")
    sent = False

    if request.method == 'POST':
        # form was submitted with data
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data 
            # ... send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = f"Read {post.title} at {post_url} \n\n" f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'sktestdjango@gmail.com', [cd['to']])
            sent = True

    else:  # show blank form
        form = EmailPostForm()        

    context = {'post': post, 'form': form, 'sent': sent}

    return render(request, 'blog/post/share.html', context)    