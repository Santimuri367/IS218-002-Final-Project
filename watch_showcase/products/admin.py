from django.contrib import admin
from .models import Watch, WatchGroup, Discussion, Comment, WatchReview
# Register the Watch model with custom admin view
@admin.register(Watch)
class WatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'retail_price', 'created_at', 'review_count', 'avg_rating')
    list_filter = ('brand', 'created_at')
    search_fields = ('name', 'brand', 'model_number')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Info', {'fields': ('name', 'brand', 'model_number', 'description', 'history', 'image')}),
        ('Pricing', {'fields': ('price', 'retail_price', 'amazon_price', 'ebay_price', 'chrono24_price') }),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )
    def review_count(self, obj):
        return obj.reviews.count()
    review_count.short_description = 'Reviews'
    def avg_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            total = 0
            for review in reviews:
                total += review.rating
            avg = total / len(reviews)
            return f"{avg:.1f}/5.0"
        return "No ratings"
    avg_rating.short_description = 'Avg Rating'
# Register the WatchGroup model with custom admin view
@admin.register(WatchGroup)
class WatchGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin', 'members_count', 'discussions_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description', 'admin__username')
    readonly_fields = ('created_at',)
    filter_horizontal = ('members',)
    prepopulated_fields = {'slug': ('name',)}
    def members_count(self, obj):
        return obj.members.count()
    members_count.short_description = 'Members'
    # Count number of discussions
    def discussions_count(self, obj):
        return obj.discussions.count()
    discussions_count.short_description = 'Discussions'
# Register the Discussion model with custom admin view
@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'author', 'created_at', 'comments_count')
    list_filter = ('group', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('created_at', 'updated_at')
    # Count number of comments
    def comments_count(self, obj):
        return obj.comments.count()
    comments_count.short_description = 'Comments'
# Register the Comment model with custom admin view
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'discussion', 'content_preview', 'created_at')
    list_filter = ('created_at', 'discussion__group')
    search_fields = ('content', 'author__username')
    readonly_fields = ('created_at',)
    def content_preview(self, obj):
        if len(obj.content) > 50:
            return obj.content[:50] + '...'
        return obj.content
    content_preview.short_description = 'Content'
# Register the WatchReview model with custom admin view
@admin.register(WatchReview)
class WatchReviewAdmin(admin.ModelAdmin):
    list_display = ('watch', 'user', 'rating', 'comment_preview', 'created_at')
    list_filter = ('rating', 'created_at', 'watch__brand')
    search_fields = ('comment', 'user__username', 'watch__name')
    readonly_fields = ('created_at',)
    def comment_preview(self, obj):
        if len(obj.comment) > 50:
            return obj.comment[:50] + '...'
        return obj.comment
    comment_preview.short_description = 'Comment'