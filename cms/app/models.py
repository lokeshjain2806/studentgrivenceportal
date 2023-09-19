from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator

COURSE_CHOICES=(
    ('B.Tech in Computer Science and Engineering (4 Years)', 'B.Tech in Computer Science and Engineering (4 Years)'),
    ('B.Tech CSE (AI & ML) with academic support of Samatrix & IBM (4 Years)', 'B.Tech CSE (AI & ML) with academic support of Samatrix & IBM (4 Years)'),
    ('B.Tech CSE (Cyber Security) with academic support of EC-Council & IBM (4 Years)', 'B.Tech CSE (Cyber Security) with academic support of EC-Council & IBM (4 Years)'),
    ('B.Tech CSE (Data Science) with academic support of IBM (4 Years)', 'B.Tech CSE (Data Science) with academic support of IBM (4 Years)'),
    ('B.Tech CSE (Full Stack Development) with academic support of Xebia (4 Years)', 'B.Tech CSE (Full Stack Development) with academic support of Xebia (4 Years)'),
    ('B.Tech CSE (UX/UI) with academic support of ImaginXP (4 Years)', 'B.Tech CSE (UX/UI) with academic support of ImaginXP (4 Years)'),
    ('B.Tech. Mechanical Engineering (Automotive Designs & Electric Vehicle) with academic support of Siemens (4 Years)', 'B.Tech. Mechanical Engineering (Automotive Designs & Electric Vehicle) with academic support of Siemens (4 Years)'),
    ('BCA (AI & Data Science) with academic support of Samatrix & IBM (3 Years)', 'BCA (AI & Data Science) with academic support of Samatrix & IBM (3 Years)'),
    ('BCA (Hons. with Research) (AI & Data Science) with academic support of Samatrix & IBM (4 Years)', 'BCA (Hons. with Research) (AI & Data Science) with academic support of Samatrix & IBM (4 Years)'),
    ('B.Tech. (Civil Engineering) with specialization in Sustainable Development & Smart Cities (4 Years)', 'B.Tech. (Civil Engineering) with specialization in Sustainable Development & Smart Cities (4 Years)'),
    ('B.Tech - Computer and Electronics Engineering (CEE) (4 Years)', 'B.Tech - Computer and Electronics Engineering (CEE) (4 Years)'),
    ('B.Sc. (Hons.) Computer Science with academic support of IBM (3 Years)', 'B.Sc. (Hons.) Computer Science with academic support of IBM (3 Years)'),
    ('B.Sc. (Hons.) Data Science (3 Years)', 'B.Sc. (Hons.) Data Science (3 Years)'),
    ('B.Sc. (Hons.) Cyber Security (3 Years)', 'B.Sc. (Hons.) Cyber Security (3 Years)'),
    ('BBA (Logistics & Supply Chain Management) with academic support of Safexpress (3 Years)', 'BBA (Logistics & Supply Chain Management) with academic support of Safexpress (3 Years)'),
    ('BBA (Hons. with Research) (Logistics & Supply Chain Management) with academic support of Safexpress (4 Years)', 'BBA (Hons. with Research) (Logistics & Supply Chain Management) with academic support of Safexpress (4 Years)'),
    ('BBA (International Accounting & Finance) (ACCA - UK) with academic support of Grant Thornton (3 Years)', 'BBA (International Accounting & Finance) (ACCA - UK) with academic support of Grant Thornton (3 Years)'),
    ('BBA (Hons. with Research) (International Accounting & Finance) (ACCA - UK) with academic support of Grant Thornton (4 Years)', 'BBA (Hons. with Research) (International Accounting & Finance) (ACCA - UK) with academic support of Grant Thornton (4 Years)'),
    ('BBA (Entrepreneurship) with academic support of GCEC Global Foundation (3 Years)', 'BBA (Entrepreneurship) with academic support of GCEC Global Foundation (3 Years)'),
    ('BBA (Hons. with Research) (Entrepreneurship) with academic support of GCEC Global Foundation(4 Years)', 'BBA (Hons. with Research) (Entrepreneurship) with academic support of GCEC Global Foundation(4 Years)'),
    ('BBA (Business Intelligence & Analytics) with academic Support of Samatrix (3 Years)', 'BBA (Business Intelligence & Analytics) with academic Support of Samatrix (3 Years)'),
    ('BBA (Hons. with Research) (Business Intelligence & Analytics) with academic Support of Samatrix (4 Years)', 'BBA (Hons. with Research) (Business Intelligence & Analytics) with academic Support of Samatrix (4 Years)'),
    ('BBA (Travel & Tourism) (3 Years)', 'BBA (Travel & Tourism) (3 Years)'),
    ('BBA (Hons. with Research) (Travel & Tourism) (4 Years)', 'BBA (Hons. with Research) (Travel & Tourism) (4 Years)'),
    ('BBA (Human Resource) (3 Years)', 'BBA (Human Resource) (3 Years)'),
    ('BBA (Hons. with Research) (Human Resource) (4 Years)', 'BBA (Hons. with Research) (Human Resource) (4 Years)'),
    ('BBA (Marketing) (3 Years)', 'BBA (Marketing) (3 Years)'),
    ('BBA (Hons. with Research) (Marketing) (4 Years)', 'BBA (Hons. with Research) (Marketing) (4 Years)'),
    ('BBA (Finance) (3 Years)', 'BBA (Finance) (3 Years)'),
    ('BBA (Hons. with Research) (Finance) (4 Years)', 'BBA (Hons. with Research) (Finance) (4 Years)'),
    ('B.Com. (Hons.) (International Accounting & Finance ) (ACCA-UK) with academic support of Grant Thornton (3 Years)', 'B.Com. (Hons.) (International Accounting & Finance ) (ACCA-UK) with academic support of Grant Thornton (3 Years)'),
    ('B.com. (Hons. with Research) (International Accounting & Finance) (ACCA-UK) with academic support of Grant Thornton (4 Years)', 'B.com. (Hons. with Research) (International Accounting & Finance) (ACCA-UK) with academic support of Grant Thornton (4 Years)'),
    ('B.Com. (Hons.) with academic support of NSE Academy (3 Years)', 'B.Com. (Hons.) with academic support of NSE Academy (3 Years)'),
    ('B.Com. (Hons. with Research) with academic support of NSE Academy (4 Years)', 'B.Com. (Hons. with Research) with academic support of NSE Academy (4 Years)'),
    ('B.Com. (Hons.) with academic support of NSE Academy (3 Years)', 'B.Com. (Hons.) with academic support of NSE Academy (3 Years)'),
    ('B.Com. (Hons. with Research) with academic support of NSE Academy (4 Years)', 'B.Com. (Hons. with Research) with academic support of NSE Academy (4 Years)'),
    ('B.Com. Programme with Preparation for Competitive Exam (Banking/ Insurance/ Railways/SSC) for Central and State Govt. Jobs (3 Years)', 'B.Com. Programme with Preparation for Competitive Exam (Banking/ Insurance/ Railways/SSC) for Central and State Govt. Jobs (3 Years)'),
    ('BBA LL.B. (Hons.) with Specialization in Business Laws/Criminal Laws/Constitutional laws/International Laws (5 Years)', 'BBA LL.B. (Hons.) with Specialization in Business Laws/Criminal Laws/Constitutional laws/International Laws (5 Years)'),
    ('B.Com. LL.B. (Hons.) with Specialization in Business Laws/Criminal Laws/Constitutional laws/International Laws (5 Years)', 'B.Com. LL.B. (Hons.) with Specialization in Business Laws/Criminal Laws/Constitutional laws/International Laws (5 Years)'),
    ('B.A. LL.B (Hons.) with Specialization in Business Laws/Criminal Laws/Constitutional laws/International Laws (5 Years)', 'B.A. LL.B (Hons.) with Specialization in Business Laws/Criminal Laws/Constitutional laws/International Laws (5 Years)'),
    ('LL.B. (Hons.) with Specialization in Business Laws/Criminal Laws/Constitutional laws/International Laws (3 Years)', 'LL.B. (Hons.) with Specialization in Business Laws/Criminal Laws/Constitutional laws/International Laws (3 Years)'),
    ('Bachelor of Pharmacy (B.Pharm.) (4 Years)', 'Bachelor of Pharmacy (B.Pharm.) (4 Years)'),
    ('Bachelor of Physiotherapy (BPT) (4 Years)', 'Bachelor of Physiotherapy (BPT) (4 Years)'),
    ('B.Pharm. (Lateral Entry) (3 Years)', 'B.Pharm. (Lateral Entry) (3 Years)'),
)


SCHOOL_CHOICES=(
    ('School of Engineering & Technology', 'School of Engineering & Technology'),
    ('School of Basic & Applied Science', 'School of Basic & Applied Science'),
    ('School of Journalism & Mass Communication', 'School of Journalism & Mass Communication'),
    ('School of Legal Studies', 'School of Legal Studies'),
    ('School of Education', 'School of Education'),
    ('School of Medical & Allied Sciences', 'School of Medical & Allied Sciences'),
    ('School of Management & Commerce', 'School of Management & Commerce'),
    ('School of Humanities', 'School of Humanities'),
    ('School of Agricultural Sciences', 'School of Agricultural Sciences'),
    ('School of Hotel Management & Catering Technology', 'School of Hotel Management & Catering Technology'),
    ('School of Architecture and Design', 'School of Architecture and Design')
)


# Create your models here.

class Student(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255)
    roll_number = models.IntegerField()
    School = models.CharField(choices=SCHOOL_CHOICES, max_length=60)
    Branch = models.CharField(choices=COURSE_CHOICES, max_length=255)
    contact_number = models.IntegerField(validators=[MaxValueValidator(9999999999)])
    email_id = models.EmailField(max_length=255)

    def __str__(self):
        return self.name


STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('In Process', 'In Process'),
    ('Success', 'Success'),
)


class Grievance(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255)
    status = models.CharField(choices=SCHOOL_CHOICES, max_length=100)

    def __str__(self):
        return self.username


class Admin(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.username


COMPLAIN_CATEGORY=(
    ('Course Content', 'Course Content'),
    ('Teaching Quality', 'Teaching Quality'),
    ('Class Scheduling', 'Class Scheduling'),
    ('Registration Problems', 'Registration Problems'),
    ('Financial Aid', 'Financial Aid'),
    ('Administrative Delays', 'Administrative Delays'),
    ('Housing Conditions', 'Housing Conditions'),
    ('Facility Issues', 'Facility Issues'),
    ('Counseling and Health Services', 'Counseling and Health Services'),
    ('Career Services', 'Career Services'),
    ('Library and Resources', 'Library and Resources'),
    ('Student Organizations', 'Student Organizations'),
    ('Campus Safety', 'Campus Safety'),
    ('Discrimination', 'Discrimination'),
    ('Inclusivity', 'Inclusivity'),
    ('Tuition and Fees', 'Tuition and Fees'),
    ('Student Employment', 'Student Employment'),
    ('IT Support', 'IT Support'),
    ('Grading Disputes', 'Grading Disputes'),
    ('Transportation Services', 'Transportation Services'),
)


class Complain(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    complain_type = models.CharField(choices=COMPLAIN_CATEGORY, max_length=80)
    subject = models.CharField(max_length=255)
    decription = models.TextField()

