from django.shortcuts import render, get_object_or_404, redirect, reverse
from . import models
from . import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from accounts import models as accounts_models


# The following is the search function which i used to handle the search part in the blog.html page
@login_required(login_url='user-login')
def search(request):
    queryset = models.Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains = query)|
            Q(overview__icontains = query)
        ).distinct()    # the distinct() function used here because title and overview 
                        # which i search by may have the same search word
    
    context = {
        'queryset' : queryset,
    }

    return render(request, 'posts/search_results.html', context)



def get_category_count():
    # The following is a queryset that return the category title and the number of each category 
    # that already exists in the database
    queryset = models.Post.objects.values('categories__title').annotate(Count('categories'))
    return queryset


def index (request):
    featured = models.Post.objects.filter(featured=True)
    latest = models.Post.objects.order_by('-timestamp')[0:3]
    categories = models.Category.objects.all()

    
    context = {
        'object_list' : featured,
        'latest' : latest,
        'categories' : categories,
    }
    
    return render(request, 'posts/index.html', context)




def blog(request):
    category_count = get_category_count() # Function which i defined above to get the category item and categories count
    most_recent = models.Post.objects.order_by('-timestamp')[0:3]
    categories = models.Category.objects.all()


    category = request.GET.get('category')

    if category:    
        queryset = models.Post.objects.filter(categories__title = category)
    else:
        queryset  = models.Post.objects.all()


    paginator = Paginator(queryset, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)



    context = {
        'queryset' : queryset, 
        'page_request_var' : page_request_var,
        'most_recent' : most_recent,
        'category_count' : category_count,
        'categories' : categories,

    }

    return render(request, 'posts/blog.html', context)



def post(request, id):
    post = get_object_or_404(models.Post, id=id)
    comment = models.Comment.objects.all().filter(user=request.user, post=post)

    category_count = get_category_count() # Function which i defined above to get 
                                          # the category item and categories count

    most_recent = models.Post.objects.order_by('-timestamp')[0:3]

    categories = models.Category.objects.all()

    if request.user.is_authenticated:
        models.PostView.objects.get_or_create(user=request.user, post=post)

    # To get the previous post if found
    try:
        previous_post = models.Post.objects.get(id=str( int(id) - 1 ))
    except:
        previous_post = None


    # To get the next post if found
    try:
        next_post = models.Post.objects.get(id=str( int(id) + 1 ))
    except:
        next_post = None

    form = forms.CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect('post_detail', post.id)
 
 
    context = {
        'post' : post,
        'previous_post' : previous_post,
        'next_post' : next_post,
        'form' : form,

        'most_recent' : most_recent,
        'category_count' : category_count,

        'categories' : categories,
        'comment' : comment,

    }


    return render(request, 'posts/post.html', context)



# To get the author...
def get_author(user):
    queryset = accounts_models.User.objects.filter(user=user)
    if queryset.exists():
        return queryset[0]

    return None


@login_required(login_url='user-login')
def post_create(request):
    categories = models.Category.objects.all()
    form = forms.PostForm(request.POST or None, request.FILES or None)
    author = request.user
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect('post_detail', form.instance.id)
        
    context = {
        'form' : form,
        'categories' : categories,
    }  

    return render(request, "posts/post_create.html", context)


@login_required(login_url='user-login')
def post_update(request, id):
    categories = models.Category.objects.all()
    post = get_object_or_404(models.Post, id=id)
    form = forms.PostForm(request.POST or None, request.FILES or None, instance=post)
    author = request.user

    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect('post_detail', form.instance.id)

    context = {
        'form' : form,
        'categories' : categories,
    }  

    return render(request, "posts/post_update.html", context)

@login_required(login_url='user-login')
def post_delete(request, id):
    categories = models.Category.objects.all()
    post = get_object_or_404(models.Post, id=id)
    if request.method == "POST":
        post.delete()
        return redirect(reverse("post_list"))

    context = {
        'post' : post,
        'categories' : categories,
    }

    return render(request, 'posts/post_delete.html', context)


@login_required(login_url='user-login')
def comment_update(request, id):
    comment = models.Comment.objects.get(id=id) # Get the comment user
    comment_post = comment.post.id  # Get the post that refered to that comment
    form = forms.CommentForm(instance=comment)
    comment_author = comment.user
    
    if request.method == "POST":
        form = forms.CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save(commit=False)
            form.instance.author = comment_author
            form.save()
            return redirect('post_detail', comment_post)
        
    context = {
        'form' : form,
        'comment_post' : comment_post,
    } 


    return render(request, "posts/comment_update.html", context)



@login_required(login_url='user-login')
def comment_delete(request, id):
    comment = models.Comment.objects.get(id=id)     # Get the comment user
    comment_post = comment.post.id  # Get the post that refered to that comment
    
    if request.method == "POST":
        comment.delete()
        return redirect('post_detail', comment_post)

    context = {
        'post' : post,
    }

    return render(request, 'posts/comment_delete.html', context)



@login_required(login_url='user-login')
def about(request):
    categories = models.Category.objects.all()

    context = {
        'categories' : categories,
    }

    return render(request, 'posts/about.html', context)