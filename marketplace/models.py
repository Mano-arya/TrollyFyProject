from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

class User(AbstractUser):
    """
    Custom User model for Trollyfy.
    Extends the default Django AbstractUser to allow for future campus-specific 
    fields while maintaining built-in authentication features.
    """
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        help_text="Contact number for offline transactions."
    )
    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        help_text="User identity image for the marketplace."
    )

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'


class Listing(models.Model):
    """
    Represents an item listed for sale on the marketplace.
    Includes details about the item category, condition, and pricing.
    """
    
    CATEGORY_CHOICES = [
        ('TEXTBOOKS', 'Textbooks'),
        ('ELECTRONICS', 'Electronics'),
        ('FURNITURE', 'Furniture'),
        ('CLOTHING', 'Clothing'),
        ('OTHER', 'Other'),
    ]

    CONDITION_CHOICES = [
        ('NEW', 'Brand New'),
        ('LIKE_NEW', 'Like New'),
        ('GOOD', 'Good'),
        ('FAIR', 'Fair'),
        ('POOR', 'Poor'),
    ]

    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
    ]

    seller = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='listings',
        help_text="The user who posted this listing."
    )
    title = models.CharField(max_length=200, help_text="Headline for the item.")
    description = models.TextField(help_text="Detailed description of the item's features or defects.")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.00)],
        help_text="Price in local currency."
    )
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        default='OTHER'
    )
    condition = models.CharField(
        max_length=20, 
        choices=CONDITION_CHOICES, 
        default='GOOD'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PUBLISHED'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'listings'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - ${self.price}"


class ItemImage(models.Model):
    """
    Stores images associated with a specific listing.
    Allows for multiple images (max 3 will be enforced in the form/view layer).
    """
    listing = models.ForeignKey(
        Listing, 
        on_delete=models.CASCADE, 
        related_name='images',
        help_text="The listing this image belongs to."
    )
    image = models.ImageField(
        upload_to='listings/%Y/%m/%d/',
        help_text="The visual asset for the listing."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'listing_images'

    def __str__(self):
        return f"Image for {self.listing.title}"


class Report(models.Model):
    """
    MODERATION SYSTEM: Allows users to flag suspicious or prohibited listings.
    This model serves as the primary data source for the Admin Moderation Dashboard,
    enabling a safer and more trustworthy campus marketplace environment.
    """
    
    REASON_CHOICES = [
        ('SCAM', 'Prohibited/Scam Content'),
        ('INAPPROPRIATE', 'Inappropriate Language/Media'),
        ('MISCATEGORIZED', 'Incorrect Category'),
        ('DUPLICATE', 'Duplicate Listing'),
        ('SYSTEM_BUG', 'System Flaw/Bug Report'),
        ('OTHER', 'Other Issues'),
    ]

    listing = models.ForeignKey(
        Listing, 
        on_delete=models.CASCADE, 
        related_name='reports',
        help_text="The listing being reported (Optional for system bugs).",
        null=True,
        blank=True
    )
    reporter = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='reports_filed',
        help_text="The user who filed the report."
    )
    reason = models.CharField(
        max_length=20, 
        choices=REASON_CHOICES,
        help_text="The specific violation category."
    )
    description = models.TextField(
        blank=True, 
        null=True, 
        help_text="Additional context provided by the reporter."
    )
    is_resolved = models.BooleanField(
        default=False, 
        help_text="Track whether the admin has reviewed and actioned this report."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'moderation_reports'
        ordering = ['-created_at']

    def __str__(self):
        target = self.listing.title if self.listing else "System Level"
        return f"Report #{self.id} - {self.get_reason_display()} on {target}"


class ChatRoom(models.Model):
    """
    SECURE COMMUNICATION: Creates a private channel between a buyer and a seller.
    Rooms are unique to each user pair to prevent overlapping conversations.
    """
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat_rooms'

    def __str__(self):
        return f"Chat for {self.listing.title}"


class ChatMessage(models.Model):
    """
    REAL-TIME MESSAGING: Stores individual messages within a room.
    Includes read-receipt hooks for future UI expansion.
    """
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'chat_messages'
        ordering = ['timestamp']

    def __str__(self):
        return f"From {self.sender.username} at {self.timestamp}"


class Wishlist(models.Model):
    """
    BOOKMARKING SYSTEM:
    Tracks which listings a student has 'heart'ed to view later.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')
        db_table = 'wishlist'

    def __str__(self):
        return f"{self.user.username} saved {self.listing.title}"
