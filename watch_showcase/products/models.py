from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
# Model for watches
class Watch(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    history = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    #Price fields for comparison of companies
    amazon_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ebay_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    chrono24_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='watches/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.brand} - {self.name}"
    # Find the lowest price from all available prices
    def get_best_price(self):
        prices = []
        if self.price:
            prices.append(self.price)
        if self.amazon_price:
            prices.append(self.amazon_price)
        if self.ebay_price:
            prices.append(self.ebay_price)
        if self.chrono24_price:
            prices.append(self.chrono24_price)
        return min(prices) if prices else None
# Model for watch discussion groups
class WatchGroup(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    members = models.ManyToManyField(User, related_name='watch_groups')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='administered_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name
# Model for discussions within groups
class Discussion(models.Model):
    group = models.ForeignKey(WatchGroup, on_delete=models.CASCADE, related_name='discussions')
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
# Model for comments on discussions
class Comment(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Comment by {self.author.username}"
# Model for watch reviews
class WatchReview(models.Model):
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ['watch', 'user']
    def __str__(self):
        return f"Review by {self.user.username} for {self.watch.name}"