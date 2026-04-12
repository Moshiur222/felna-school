from django.db import models
from PIL import Image
from io import BytesIO
from django.utils.text import slugify
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import os
import time

# Define the dimensions for each model
WELCOME_MESSAGE_SIZE = (350, 200)
HEADMASTER_MESSAGE_SIZE = (200, 200)
ASSISTANT_HEADMASTER_MESSAGE_SIZE = (200, 200)


# -------------------------------
# WebP Converter
# -------------------------------
def convert_to_webp(image_field, max_size_kb=100):
    try:
        img = Image.open(image_field)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        quality = 85
        output = BytesIO()

        while quality > 10:
            output.seek(0)
            output.truncate()

            img.save(
                output,
                format="WEBP",
                quality=quality,
                method=6
            )

            size_kb = output.tell() / 1024
            if size_kb <= max_size_kb:
                break

            quality -= 5

        output.seek(0)
        file_name = os.path.splitext(image_field.name)[0] + ".webp"

        return ContentFile(output.read(), name=file_name)

    except Exception:
        return image_field


# -------------------------------
# Upload Paths
# -------------------------------
def album_banner_upload_to(instance, filename):
    if instance.title:
        album_folder = slugify(instance.title)
    else:
        album_folder = "untitled-album"

    filename = f"{instance.slug}.webp"
    return os.path.join("Album", album_folder, filename)


def photo_upload_to(instance, filename):
    if instance.album and instance.album.title:
        album_folder = slugify(instance.album.title)
    else:
        album_folder = "uncategorized"

    filename = f"{instance.slug}.webp"
    return os.path.join("Album", album_folder, filename)


# -------------------------------
# Album Model
# -------------------------------
class Album(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=150, blank=True)
    banner = models.ImageField(upload_to=album_banner_upload_to)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Generate unique slug
        if not self.slug and self.title:
            base_slug = f"felna-high-school-{slugify(self.title)}"
            slug = base_slug
            counter = 1

            while Album.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        # Convert banner to webp
        if self.banner and not self.banner.name.endswith(".webp"):
            self.banner = convert_to_webp(self.banner, max_size_kb=100)

        super().save(*args, **kwargs)


# -------------------------------
# Gallery Model
# -------------------------------
class Gallery(models.Model):
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="photos",
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to=photo_upload_to)
    slug = models.SlugField(max_length=150, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        if self.album:
            return f"{self.album.title} - Photo {self.id}"
        return f"Photo {self.id}"

    def save(self, *args, **kwargs):
        # Generate unique slug
        if not self.slug:
            if self.album:
                base_slug = f"felna-{slugify(self.album.title)}"
            else:
                base_slug = "felna-photo"

            slug = base_slug
            counter = 1

            while Gallery.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        # Convert image to webp
        if self.image and not self.image.name.endswith(".webp"):
            self.image = convert_to_webp(self.image, max_size_kb=150)

        super().save(*args, **kwargs)
    
    
from django.db import models


class Notice(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    file = models.FileField(upload_to='notices/', blank=True, null=True)  # PDF, DOC, etc.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']  # latest notices first

    def __str__(self):
        return self.title
    
    
class OurHistory(models.Model):
    title = models.CharField(max_length=255, default="History Of Felna High School")
    content = models.TextField()  # long text about school history
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Our History"
        verbose_name_plural = "Our History"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
        

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name    
    

class AdmissionResult(models.Model):
    CLASS_CHOICES = [
        ('6', 'Class 6'),
        ('7', 'Class 7'),
        ('8', 'Class 8'),
        ('9', 'Class 9'),
        ('10', 'Class 10'),
    ]

    exam_track_number = models.CharField(max_length=100, unique=True)  # unique track ID
    student_name = models.CharField(max_length=255)  # optional, for display
    class_name = models.CharField(max_length=10, choices=CLASS_CHOICES)
    year = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=[('Passed', 'Passed'), ('Failed', 'Failed'), ('Waiting', 'Waiting')],
        default='Waiting'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Admission Result"
        verbose_name_plural = "Admission Results"
        ordering = ['-year', 'class_name']

    def __str__(self):
        return f"{self.exam_track_number} - {self.student_name} ({self.class_name}, {self.year})"
    
    
    
    
class Slider(models.Model):
    headline = models.CharField(max_length=255)
    caption = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='sliders/')  # stores image in MEDIA_ROOT/sliders/
    order = models.PositiveIntegerField(default=0, help_text="Order of slide in carousel")
    is_active = models.BooleanField(default=True, help_text="Show this slide in carousel")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Slider"
        verbose_name_plural = "Sliders"
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.headline} (Slide {self.order})"
    
    
class MissionVision(models.Model):
    mission = models.TextField()
    vision = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mission & Vision"
        verbose_name_plural = "Mission & Vision"

    def __str__(self):
        return "Our Mission & Vision"
    
class SchoolProfile(models.Model):
    school_name = models.CharField(max_length=255)
    principal_name = models.CharField(max_length=255)
    address = models.TextField()
    contact_number = models.CharField(max_length=50)
    fax_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    web_address = models.URLField(blank=True, null=True)
    class_room_info = models.TextField(blank=True, null=True)
    probable_admission_date = models.CharField(max_length=50, blank=True, null=True)
    established_date = models.DateField(blank=True, null=True)
    eiin = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "School Profile"
        verbose_name_plural = "School Profile"

    def __str__(self):
        return self.school_name
    
    
    
class Founder(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='founders/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Founder"
        verbose_name_plural = "Founders"
        ordering = ['id']

    def __str__(self):
        return self.name
    
class Donor(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='Donor/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Donor"
        verbose_name_plural = "Donor"
        ordering = ['id']

    def __str__(self):
        return self.name
    

class Management(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='Donor/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Management"
        verbose_name_plural = "Management"
        ordering = ['id']

    def __str__(self):
        return self.name
    
    

class WelcomeMessage(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='welcome_messages/')
    message = models.TextField()

    class Meta:
        verbose_name_plural = "Welcome Messages"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # যদি ইমেজ থাকে এবং এটি নতুন আপলোড করা হয়
        if self.image and hasattr(self.image, 'file'):
            try:
                img = Image.open(self.image)
                
                # ইমেজ ফরম্যাট ঠিক রাখা (RGB তে কনভার্ট করা ভালো যদি PNG/RGBA হয়)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                # রিসাইজ করা (Aspect Ratio বজায় রেখে)
                img.thumbnail(WELCOME_MESSAGE_SIZE, Image.Resampling.LANCZOS)

                # মেমোরিতে সেভ করা
                output = BytesIO()
                img.save(output, format='JPEG', quality=90)
                output.seek(0)
                
                # নতুন ফাইল নেম তৈরি
                file_name = f"{self.image.name.split('.')[0]}.jpg"

                # InMemoryUploadedFile এ সঠিক সাইজ দেওয়া (len(output.getvalue()))
                self.image = InMemoryUploadedFile(
                    output,
                    'ImageField',
                    file_name,
                    'image/jpeg',
                    len(output.getvalue()), # এটি sys.getsizeof থেকে অনেক বেশি নির্ভরযোগ্য
                    None
                )
            except Exception as e:
                print(f"Error resizing image: {e}")

        super().save(*args, **kwargs)

class HeadmasterMessage(models.Model):
    """
    Model for the headmaster's message, with a square-format image.
    """
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='headmaster_messages/')
    message = models.TextField()

    class Meta:
        verbose_name_plural = "Headmaster's Message"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Overrides the save method to resize the image to 200x200 pixels.
        """
        if self.image:
            img = Image.open(self.image)
            img.thumbnail(HEADMASTER_MESSAGE_SIZE, Image.Resampling.LANCZOS)
            output = BytesIO()
            img.save(output, format=img.format, quality=90)
            output.seek(0)
            self.image = InMemoryUploadedFile(
                output,
                'ImageField',
                f"{self.image.name.split('.')[0]}.{img.format.lower()}",
                sys.getsizeof(output),
                None,
                None
            )
        super().save(*args, **kwargs)
        
        

class AssistantHeadmasterMessage(models.Model):
    """
    Model for the assistant headmaster's message, with a square-format image.
    """
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='assistant_headmaster_messages/')
    message = models.TextField()

    class Meta:
        verbose_name_plural = "Assistant Headmaster's Message"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Overrides the save method to resize the image to 200x200 pixels.
        """
        if self.image:
            img = Image.open(self.image)
            img.thumbnail(ASSISTANT_HEADMASTER_MESSAGE_SIZE, Image.Resampling.LANCZOS)
            output = BytesIO()
            img.save(output, format=img.format, quality=90)
            output.seek(0)
            self.image = InMemoryUploadedFile(
                output,
                'ImageField',
                f"{self.image.name.split('.')[0]}.{img.format.lower()}",
                sys.getsizeof(output),
                None,
                None
            )
        super().save(*args, **kwargs)
        
        
class Teacher(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    EDUCATION_CHOICES = [ (1, 'SSC'), (2, 'HSC'), (3, 'BSc'), (4, 'MSc'), (5, 'Phd')]

    name = models.CharField(max_length=150, verbose_name="Name")
    designation = models.CharField(max_length=100, verbose_name="Designation")
    subject = models.CharField(max_length=100, verbose_name="Subject", blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name="Phone Number", blank=True, null=True)
    email = models.EmailField(verbose_name="Email", blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Gender", blank=True, null=True)
    photo = models.ImageField(upload_to="teachers/", verbose_name="Photo", blank=True, null=True)
    bio = models.TextField(verbose_name="Biography", blank=True, null=True)
    join_date = models.DateField(verbose_name="Join Date", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Active")
    last_edu = models.IntegerField(choices=EDUCATION_CHOICES, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
        ordering = ["name"]

    def __str__(self):
        return self.name
    

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    CLASS_CHOICES = [
        ('6', 'Class 6'),
        ('7', 'Class 7'),
        ('8', 'Class 8'),
        ('9', 'Class 9'),
        ('10', 'Class 10'),
    ]

    name = models.CharField(max_length=255)
    roll_number = models.CharField(max_length=50)
    class_name = models.CharField(max_length=10, choices=CLASS_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    guardian_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to="students/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ['class_name', 'roll_number']

    def __str__(self):
        return f"{self.name} - Class {self.class_name}"
    
    
class ExamResult(models.Model):
    CLASS_CHOICES = [
        ('6', 'Class 6'),
        ('7', 'Class 7'),
        ('8', 'Class 8'),
        ('9', 'Class 9'),
        ('10', 'Class 10'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="exam_results")
    year = models.PositiveIntegerField()  # passing year
    subject = models.CharField(max_length=100)   # e.g., Math, English
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Exam Result"
        verbose_name_plural = "Exam Results"
        ordering = ['-year', 'student__class_name', 'student__roll_number']

    def __str__(self):
        return f"{self.student.name} - Class {self.student.class_name} ({self.year})"
    


class ClassRoutine(models.Model):
    DAYS_OF_WEEK = [
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]

    CLASS_CHOICES = [
        ('6', 'Class 6'),
        ('7', 'Class 7'),
        ('8', 'Class 8'),
        ('9', 'Class 9'),
        ('10', 'Class 10'),
    ]

    class_name = models.CharField(max_length=10, choices=CLASS_CHOICES)
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK, blank=True, null=True)
    subject = models.CharField(max_length=100, blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(upload_to='class_routines/', blank=True, null=True)  # optional routine image

    class Meta:
        verbose_name = "Class Routine"
        verbose_name_plural = "Class Routines"
        ordering = ['class_name', 'day', 'start_time']

    def __str__(self):
        return f"{self.class_name} - {self.subject or 'No Subject'} ({self.day or 'No Day'})"
    
    
class SchoolAchievement(models.Model):
    title = models.CharField(max_length=255)  # e.g., "Best School Award"
    description = models.TextField(blank=True, null=True)  # Details about the achievement
    awarded_by = models.CharField(max_length=255, blank=True, null=True)  # Organization giving the award
    date_awarded = models.DateField()  # Date of achievement
    year = models.PositiveIntegerField()  # Academic year
    image = models.ImageField(upload_to='achievements/', blank=True, null=True)  # Achievement image

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "School Achievement"
        verbose_name_plural = "School Achievements"
        ordering = ['-year', '-date_awarded']

    def __str__(self):
        return f"{self.title} ({self.year})"
    


from django.db import models

class Syllabus(models.Model):
    CLASS_CHOICES = [
        ('6', 'Class 6'),
        ('7', 'Class 7'),
        ('8', 'Class 8'),
        ('9', 'Class 9'),
        ('10', 'Class 10'),
    ]

    class_name = models.CharField(max_length=10, choices=CLASS_CHOICES)
    image = models.ImageField(upload_to='syllabus_images/')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Syllabus"
        verbose_name_plural = "Syllabuses"

    def __str__(self):
        return f"Syllabus - Class {self.class_name}"


class ExamRoutine(models.Model):
    CLASS_CHOICES = [
        ('6', 'Class 6'),
        ('7', 'Class 7'),
        ('8', 'Class 8'),
        ('9', 'Class 9'),
        ('10', 'Class 10'),
    ]

    class_name = models.CharField(max_length=10, choices=CLASS_CHOICES)
    image = models.ImageField(upload_to='exam_routine_images/')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Exam Routine"
        verbose_name_plural = "Exam Routines"

    def __str__(self):
        return f"Exam Routine - Class {self.class_name}"
    
class AdmissionCircular(models.Model):
    CLASS_CHOICES = [
        ('6', 'Class 6'),
        ('7', 'Class 7'),
        ('8', 'Class 8'),
        ('9', 'Class 9'),
        ('10', 'Class 10'),
    ]

    class_name = models.CharField(max_length=10, choices=CLASS_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='admission_circulars/', blank=True, null=True)
    document = models.FileField(upload_to='admission_documents/', blank=True, null=True)  # Optional PDF/Doc
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Admission Circular"
        verbose_name_plural = "Admission Circulars"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_class_name_display()})"
    

class Prospectus(models.Model):
    CLASS_CHOICES = [
        ('6', 'Class 6'),
        ('7', 'Class 7'),
        ('8', 'Class 8'),
        ('9', 'Class 9'),
        ('10', 'Class 10'),
    ]

    title = models.CharField(max_length=255)
    class_name = models.CharField(max_length=10, choices=CLASS_CHOICES)
    year = models.PositiveIntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='prospectus_images/', blank=True, null=True)
    document = models.FileField(upload_to='prospectus_docs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Prospectus"
        verbose_name_plural = "Prospectuses"
        ordering = ['-year', 'class_name', 'title']

    def __str__(self):
        return f"{self.title} ({self.get_class_name_display()})"
    

class Facility(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='facilities/', blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)  # e.g., Classroom, Lab, Sports
    capacity = models.PositiveIntegerField(blank=True, null=True)  # e.g., number of students it can accommodate
    location = models.CharField(max_length=200, blank=True, null=True)
    status = models.BooleanField(default=True)  # active or inactive
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"
        ordering = ['title']

    def __str__(self):
        return self.title
    

class Visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    visited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.visited_at}"


import datetime
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField

def batch_years():
    current_year = datetime.datetime.now().year
    return [(year, year) for year in range(2000, current_year + 1)]

class Village(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class StudentRegistration(models.Model):
    GENDER_CHOICES = [(1, 'পুরুষ'), (2, 'মহিলা'), (3, 'অন্যান্য')]
    MARITAL_STATUS_CHOICES = [(1, 'অবিবাহিত'), (2, 'বিবাহিত'), (3, 'তালাকপ্রাপ্ত')]
    IS_WHATSAPP_BD_CHOICES = [(1, 'হ্যাঁ'), (2, 'না')]
    IS_WHATSAPP_ABROAD_CHOICES = [(1, 'হ্যাঁ'), (2, 'না')]
    OCCUPATION_CHOICES = [(1, 'কৃষক'), (2, 'চাকরিজীবী'), (3, 'ব্যবসায়ী'), (4, 'ফ্রিল্যান্সার'), (5, 'বেকার'),]
    EDUCATION_CHOICES = [ (1, 'SSC'), (2, 'HSC'), (3, 'BSc'), (4, 'MSc'), (5, 'Phd')]
    NUMBER_HIDE_CHOICES = [(1, 'হ্যাঁ'), (2, 'না')]
    IS_VERIFIED_CHOICES = [ (0, 'Pending'), (1, 'Accepted')]

    student_name = models.CharField(max_length=100)
    facebook_profile = models.CharField(max_length=1000, null=True, blank=True)
    student_bio = models.TextField(max_length=1000, null=True, blank=True)
    student_photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, null=True)
    marrital_status = models.IntegerField(choices=MARITAL_STATUS_CHOICES, null=True)
    batch = models.IntegerField(choices=batch_years(), null=True)
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, null=True)
    current_location = CountryField(blank_label='Select Country')
    job_location = CountryField(blank_label='Select Country')
    bd_no = models.CharField(max_length=15)
    is_whatsapp_bd = models.IntegerField(choices=IS_WHATSAPP_BD_CHOICES, null=True)
    abroad_no = models.CharField(max_length=15, null=True, blank=True)
    is_whatsapp_abroad = models.IntegerField(choices=IS_WHATSAPP_ABROAD_CHOICES, null=True)
    occupation = models.IntegerField(choices=OCCUPATION_CHOICES, null=True)
    last_edu = models.IntegerField(choices=EDUCATION_CHOICES, null=True)
    is_no_hide = models.IntegerField(choices=NUMBER_HIDE_CHOICES, null=True)
    is_verified = models.BooleanField(choices=IS_VERIFIED_CHOICES,)
    job_description = models.TextField(max_length=500, null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True)

    def generate_unique_slug(self):
        """Generate a unique slug with incremental numbering."""
        base_slug = slugify(
            f"felna-high-school-batch-{self.batch}-{self.student_name}"
        )
        slug = base_slug
        counter = 1

        while StudentRegistration.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.student_name