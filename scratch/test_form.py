import os
import django
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trollyfy_core.settings')
django.setup()

from marketplace.forms import ListingForm

# Test form with multiple files
data = {
    'title': 'Test Item',
    'description': 'A test item',
    'price': '10.00',
    'category': 'OTHER',
    'condition': 'GOOD'
}

file_data = {
    'images': SimpleUploadedFile('test.jpg', b'test content', content_type='image/jpeg')
}

form = ListingForm(data=data, files=file_data)
print(f"Form Valid: {form.is_valid()}")
if not form.is_valid():
    print(f"Errors: {form.errors}")

# Test form without files (should be balance since required=False)
form_no_files = ListingForm(data=data)
print(f"Form (No Files) Valid: {form_no_files.is_valid()}")
if not form_no_files.is_valid():
    print(f"Errors: {form_no_files.errors}")
