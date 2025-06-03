from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post, Category
from .forms import PostForm
from .forms import CommentForm

class PostListView(ListView):
    model = Post
    template_name = 'content/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(is_published=True)
        
        # Filter by category
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        # Filter by tag
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__icontains=tag)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['featured_posts'] = Post.objects.filter(is_featured=True)[:3]
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'content/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_posts'] = Post.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        return context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.filter(parent=None)
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'content/post_form.html'
    success_url = reverse_lazy('post_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'content/post_form.html'
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'slug': self.object.slug})
    


from django.views.generic import CreateView
from .models import Comment

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(slug=self.kwargs['slug'])
        
        # Check for parent comment
        parent_id = self.request.POST.get('parent_id')
        if parent_id:
            form.instance.parent = Comment.objects.get(id=parent_id)
            
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'slug': self.kwargs['slug']}) + '#comments'