from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User, Listing, ItemImage, Report, ChatRoom, ChatMessage

# --- HOLMES BRANDING CONFIGURATION ---
admin.site.site_header = "Trollyfy.com Admin Console"
admin.site.site_title = "Trollyfy Moderator Portal"
admin.site.index_title = "Platform Moderation & Management"


# --- USER MODERATION & DATA INTEGRITY ---
class CustomUserAdmin(UserAdmin):
    """
    DATA INTEGRITY & AUDIT:
    Enforces that 'email' and 'phone_number' are present.
    Makes critical identity and audit fields READ-ONLY during editing.
    """
    list_display = ('username', 'email', 'phone_number', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('-date_joined',)

    # Fields shown when editing a user
    fieldsets = UserAdmin.fieldsets + (
        ('Marketplace Identity', {'fields': ('phone_number', 'profile_picture')}),
    )

    # Fields shown when ADDING a user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Required for Marketplace', {
            'classes': ('wide',),
            'fields': ('email', 'phone_number'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        """
        Locks the username and date fields after creation to preserve 
        the immutable student ID audit trail.
        """
        if obj: # editing an existing object
            return self.readonly_fields + ('username', 'date_joined', 'last_login')
        return self.readonly_fields

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

# Unregister and re-register
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass
admin.site.register(User, CustomUserAdmin)

# --- LISTING MODERATION ---
class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1
    max_num = 3

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    """
    SYSTEM INTEGRITY:
    Seller and Timestamps are immutable for moderators to ensure
    ownership accuracy and audit transparency.
    """
    list_display = ('title', 'seller', 'category', 'price', 'condition', 'created_at')
    list_filter = ('category', 'condition', 'created_at')
    search_fields = ('title', 'description', 'seller__username')
    readonly_fields = ('seller', 'created_at', 'updated_at')
    inlines = [ItemImageInline]
    
    fieldsets = (
        ('Immutable Audit Data', {'fields': ('seller', 'created_at', 'updated_at')}),
        ('Core Information', {'fields': ('title', 'category', 'condition')}),
        ('Pricing & Description', {'fields': ('price', 'description')}),
    )

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


# --- REPORTING & SYSTEM INTEGRITY ---
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """
    MODERATION REVIEWS:
    Filters allow admins to quickly separate 'Listing Reports' from 
    'System Feedback'.
    
    DATA INTEGRITY: Critical metadata (Reporter, Listing, Reason) is 
    READ-ONLY to prevent staff from altering historical complaint records.
    """
    list_display = ('id', 'listing_link', 'reporter', 'reason', 'is_resolved', 'created_at')
    list_filter = ('reason', 'is_resolved', 'created_at')
    search_fields = ('listing__title', 'reporter__username', 'description')
    actions = ['mark_as_resolved']
    
    # Preventing manipulation of original complaint data
    readonly_fields = ('reporter', 'listing', 'reason', 'description', 'created_at')

    fieldsets = (
        ('Resolution Status', {
            'fields': ('is_resolved',)
        }),
        ('Original Complaint Data', {
            'fields': ('reporter', 'listing', 'reason', 'description', 'created_at'),
            'description': "This data is immutable to preserve the audit trail of user feedback."
        }),
    )

    def listing_link(self, obj):
        from django.utils.safestring import mark_safe
        if obj.listing:
            return format_html('<a href="/admin/marketplace/listing/{}/change/">{}</a>', 
                               obj.listing.id, obj.listing.title)
        return mark_safe('<span style="color: #666;">System Flaw</span>')
    listing_link.short_description = 'Listing'

    def mark_as_resolved(self, request, queryset):
        queryset.update(is_resolved=True)
    mark_as_resolved.short_description = "Mark selected as resolved"

    def has_delete_permission(self, request, obj=None):
        """Only senior superusers can prune old moderated data."""
        return request.user.is_superuser


# --- CHAT & COMMUNICATION AUDIT ---
class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('sender', 'content', 'timestamp')
    can_delete = False

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'created_at')
    inlines = [ChatMessageInline]
    readonly_fields = ('participants', 'listing', 'created_at')

    def has_add_permission(self, request):
        return False # Chats should only be created via the marketplace
