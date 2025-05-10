from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Avg, Count, Q
from django.urls import reverse
from .models import Watch, WatchGroup, Discussion, Comment, WatchReview
from .forms import WatchGroupForm, DiscussionForm, CommentForm, WatchReviewForm, UserRegisterForm
# Home page view
def home(request):
    recent_watches = Watch.objects.all()[:8]
    popular_groups = WatchGroup.objects.all()[:4]
    
    return render(request, 'products/home.html', {
        'watches': recent_watches,
        'groups': popular_groups,
    })
# Watch listing with search option
class WatchListView(ListView):
    model = Watch
    template_name = 'products/watch_list.html'
    context_object_name = 'watches'
    paginate_by = 8
    ordering = ['name']
    def get_queryset(self):
        watches = super().get_queryset()
        search_query = self.request.GET.get('q')
        # Filter by search query if provided
        if search_query:
            watches = watches.filter(
                Q(name__icontains=search_query) | 
                Q(brand__icontains=search_query)
            )
        return watches
# Single watch detail view
class WatchDetailView(DetailView):
    model = Watch
    template_name = 'products/watch_detail.html'
    context_object_name = 'watch'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add reviews to context the watch
        context['reviews'] = self.object.reviews.all().order_by('-created_at')
        # Add review form for logged users only
        if self.request.user.is_authenticated:
            context['review_form'] = WatchReviewForm()
        return context
    # Handle review submissions
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please log in to submit a review.")
            return redirect('login')
        watch = self.get_object()
        form = WatchReviewForm(request.POST)
        if form.is_valid():
            existing_review = WatchReview.objects.filter(
                watch=watch, 
                user=request.user
            ).first()
            if existing_review:
                # Update the existing review
                existing_review.rating = form.cleaned_data['rating']
                existing_review.comment = form.cleaned_data['comment']
                existing_review.save()
                messages.success(request, "Your review has been updated.")
            else:
                # Create a new review
                new_review = form.save(commit=False)
                new_review.watch = watch
                new_review.user = request.user
                new_review.save()
                messages.success(request, "Your review has been submitted.")
                
            return redirect('watch_detail', pk=watch.pk)
        messages.error(request, "There was an error with your review. Please try again.")
        context = self.get_context_data(object=watch)
        context['review_form'] = form
        return render(request, self.template_name, context)
# Group listing view
class WatchGroupListView(ListView):
    model = WatchGroup
    template_name = 'products/group_list.html'
    context_object_name = 'groups'
    paginate_by = 10
# Single group detail view
class WatchGroupDetailView(DetailView):
    model = WatchGroup
    template_name = 'products/group_detail.html'
    context_object_name = 'group'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['discussions'] = self.object.discussions.all().order_by('-created_at')
        return context
    # Handle group actions (join, leave, etc)
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please log in first.")
            return redirect('login')
        group = self.get_object()
        action = request.POST.get('action')
        if action == 'join':
            group.members.add(request.user)
            messages.success(request, f"You have joined {group.name}.")
        elif action == 'leave':
            if request.user == group.admin:
                messages.error(request, "As the admin, you cannot leave your own group.")
            else:
                group.members.remove(request.user)
                messages.success(request, f"You have left {group.name}.")
        elif action == 'delete':
            # Only admin can delete group
            if request.user != group.admin:
                messages.error(request, "Only the group admin can delete this group.")
            else:
                group_name = group.name
                group.delete()
                messages.success(request, f"Group '{group_name}' has been deleted.")
                return redirect('group_list')        
        elif action == 'new_discussion':
            # Only members can create discussions
            if request.user not in group.members.all():
                messages.error(request, "You must be a member to start a discussion.")
            else:
                title = request.POST.get('title')
                content = request.POST.get('content')
                if title and content:
                    Discussion.objects.create(
                        group=group,
                        title=title,
                        content=content,
                        author=request.user
                    )
                    messages.success(request, "Discussion created successfully.")
                else:
                    messages.error(request, "Please provide both title and content.")
        return redirect('group_detail', slug=group.slug)
# Create a new group
@login_required
def create_group(request):
    if request.method == 'POST':
        form = WatchGroupForm(request.POST)
        if form.is_valid():
            # Create the group
            group = form.save(commit=False)
            group.admin = request.user
            group.save()
            # Add creator as first member
            group.members.add(request.user)
            messages.success(request, f"Group '{group.name}' has been created.")
            return redirect('group_detail', slug=group.slug)
    else:
        form = WatchGroupForm()
    return render(request, 'products/group_form.html', {'form': form})
@login_required
def discussion_detail(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    comments = discussion.comments.all().order_by('created_at')
    related_discussions = Discussion.objects.filter(
        group=discussion.group
    ).exclude(
        pk=pk
    ).order_by('-created_at')[:5]
    
    return render(request, 'products/discussion_detail.html', {
        'discussion': discussion,
        'comments': comments,
        'related_discussions': related_discussions,
    })
# Create a new discussion
@login_required
def create_discussion(request, group_slug):
    group = get_object_or_404(WatchGroup, slug=group_slug)
    # Check if user is a member
    if request.user not in group.members.all():
        messages.error(request, "You must be a member to start a discussion.")
        return redirect('group_detail', slug=group_slug)
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.group = group
            discussion.author = request.user
            discussion.save()
            
            messages.success(request, "Discussion created.")
            return redirect('discussion_detail', pk=discussion.pk)
    else:
        form = DiscussionForm()
    
    return render(request, 'products/discussion_form.html', {
        'form': form, 
        'group': group
    })
# Edit an existing discussion
@login_required
def edit_discussion(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    # Check permissions
    if request.user != discussion.author and request.user != discussion.group.admin:
        messages.error(request, "You can't edit this discussion.")
        return redirect('discussion_detail', pk=pk)
    
    if request.method == 'POST':
        form = DiscussionForm(request.POST, instance=discussion)
        if form.is_valid():
            form.save()
            messages.success(request, "Discussion updated.")
            return redirect('discussion_detail', pk=discussion.pk)
    else:
        form = DiscussionForm(instance=discussion)
    
    return render(request, 'products/discussion_form.html', {
        'form': form, 
        'discussion': discussion
    })
# Delete a discussion
@login_required
def delete_discussion(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    group_slug = discussion.group.slug
    # Check permissions
    if request.user != discussion.author and request.user != discussion.group.admin:
        messages.error(request, "You can't delete this discussion.")
        return redirect('discussion_detail', pk=pk)
    if request.method == 'POST':
        discussion.delete()
        messages.success(request, "Discussion deleted.")
        return redirect('group_detail', slug=group_slug)
    return redirect('discussion_detail', pk=pk)
# Add a comment to a discussion
@login_required
def add_comment(request, discussion_id):
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    # Check if user is a member
    if request.user not in discussion.group.members.all():
        messages.error(request, "You must be a member to comment.")
        return redirect('discussion_detail', pk=discussion_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                discussion=discussion,
                author=request.user,
                content=content
            )
            messages.success(request, "Comment added.")
        else:
            messages.error(request, "Comment can't be empty.")
    return redirect('discussion_detail', pk=discussion_id)
# Delete a comment
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    discussion_id = comment.discussion.id
    # Check permissions
    if request.user != comment.author and request.user != comment.discussion.group.admin:
        messages.error(request, "You can't delete this comment.")
        return redirect('discussion_detail', pk=discussion_id)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Comment deleted.")
    return redirect('discussion_detail', pk=discussion_id)
# Join a group
@login_required
def join_group(request, slug):
    group = get_object_or_404(WatchGroup, slug=slug)  
    # Add user to group if not already a member
    if request.user not in group.members.all():
        group.members.add(request.user)
        messages.success(request, f"You joined {group.name}.")
    return redirect('group_detail', slug=slug)
# Leave a group
@login_required
def leave_group(request, slug):
    group = get_object_or_404(WatchGroup, slug=slug)  
    if request.user in group.members.all():
        # Admin can't leave their own group
        if request.user == group.admin:
            messages.error(request, "As the admin, you can't leave your own group.")
        else:
            group.members.remove(request.user)
            messages.success(request, f"You left {group.name}.")
    return redirect('group_detail', slug=slug)
# Show brand-specific groups
def brand_groups(request):
    brands = WatchGroup.objects.annotate(
        discussion_count=Count('discussions')
    ).order_by('name')
    return render(request, 'products/brand_groups.html', {'brands': brands})
# Show specialized interest groups
def specialized_groups(request):
    # The template has the hardcoded groups
    return render(request, 'products/specialized_groups.html')
# Admin feedback report
@login_required
@user_passes_test(lambda user: user.is_staff or user.is_superuser)
def feedback_report(request):
    # Get all reviews, newest first
    reviews = WatchReview.objects.all().order_by('-created_at')   
    watches = Watch.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-avg_rating')
    return render(request, 'products/feedback_report.html', {
        'reviews': reviews,
        'watches': watches,
    })
# User registration
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
# Search watches
def search_watches(request):
    query = request.GET.get('q', '')
    watches = []
    if query:
        watches = Watch.objects.filter(
            Q(name__icontains=query) | 
            Q(brand__icontains=query) |
            Q(description__icontains=query)
        )
    return render(request, 'products/search_results.html', {
        'watches': watches,
        'query': query
    })