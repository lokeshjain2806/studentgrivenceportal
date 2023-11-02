from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator
from django.utils import timezone


# Create your models here.
class Student(models.Model):
    COURSE_CHOICES = (
        ('Select Your Course', 'Select Your Course'),
        (

            'B.Tech in Computer Science and Engineering (4 Years)',
            'B.Tech in Computer Science and Engineering (4 Years)'),
        ('B.Tech CSE (AI & ML) with academic support of Samatrix & IBM (4 Years)',
         'B.Tech CSE (AI & ML) with academic support of Samatrix & IBM (4 Years)'),
        ('B.Tech CSE (Cyber Security) with academic support of EC-Council & IBM (4 Years)',
         'B.Tech CSE (Cyber Security) with academic support of EC-Council & IBM (4 Years)'),
        ('B.Tech CSE (Data Science) with academic support of IBM (4 Years)',
         'B.Tech CSE (Data Science) with academic support of IBM (4 Years)'),
        ('B.Tech CSE (Full Stack Development) with academic support of Xebia (4 Years)',
         'B.Tech CSE (Full Stack Development) with academic support of Xebia (4 Years)'),
        ('B.Tech CSE (UX/UI) with academic support of ImaginXP (4 Years)',
         'B.Tech CSE (UX/UI) with academic support of ImaginXP (4 Years)'),
        (
            'B.Tech. Mechanical Engineering (Automotive Designs & Electric Vehicle) with academic support of Siemens '
            '(4 Years)',
            'B.Tech. Mechanical Engineering (Automotive Designs & Electric Vehicle) with academic support of Siemens '
            '(4 Years)'),
        ('BCA (AI & Data Science) with academic support of Samatrix & IBM (3 Years)',
         'BCA (AI & Data Science) with academic support of Samatrix & IBM (3 Years)'),
        ('BCA (Hons. with Research) (AI & Data Science) with academic support of Samatrix & IBM (4 Years)',
         'BCA (Hons. with Research) (AI & Data Science) with academic support of Samatrix & IBM (4 Years)'),
        ('B.Tech. (Civil Engineering) with specialization in Sustainable Development & Smart Cities (4 Years)',
         'B.Tech. (Civil Engineering) with specialization in Sustainable Development & Smart Cities (4 Years)'),
        ('B.Tech - Computer and Electronics Engineering (CEE) (4 Years)',
         'B.Tech - Computer and Electronics Engineering (CEE) (4 Years)'),
        ('B.Sc. (Hons.) Computer Science with academic support of IBM (3 Years)',
         'B.Sc. (Hons.) Computer Science with academic support of IBM (3 Years)'),
        ('B.Sc. (Hons.) Data Science (3 Years)', 'B.Sc. (Hons.) Data Science (3 Years)'),
        ('B.Sc. (Hons.) Cyber Security (3 Years)', 'B.Sc. (Hons.) Cyber Security (3 Years)'),
        ('BBA (Logistics & Supply Chain Management) with academic support of Safexpress (3 Years)',
         'BBA (Logistics & Supply Chain Management) with academic support of Safexpress (3 Years)'),
        (
            'BBA (Hons. with Research) (Logistics & Supply Chain Management) with academic support of Safexpress (4 '
            'Years)',
            'BBA (Hons. with Research) (Logistics & Supply Chain Management) with academic support of Safexpress (4 '
            'Years)'),
        ('BBA (International Accounting & Finance) (ACCA - UK) with academic support of Grant Thornton (3 Years)',
         'BBA (International Accounting & Finance) (ACCA - UK) with academic support of Grant Thornton (3 Years)'),
        (
            'BBA (Hons. with Research) (International Accounting & Finance) (ACCA - UK) with academic support of '
            'Grant Thornton (4 Years)',
            'BBA (Hons. with Research) (International Accounting & Finance) (ACCA - UK) with academic support of'
            'Grant Thornton (4 Years)'),
        ('BBA (Entrepreneurship) with academic support of GCEC Global Foundation (3 Years)',
         'BBA (Entrepreneurship) with academic support of GCEC Global Foundation (3 Years)'),
        ('BBA (Hons. with Research) (Entrepreneurship) with academic support of GCEC Global Foundation(4 Years)',
         'BBA (Hons. with Research) (Entrepreneurship) with academic support of GCEC Global Foundation(4 Years)'),
        ('BBA (Business Intelligence & Analytics) with academic Support of Samatrix (3 Years)',
         'BBA (Business Intelligence & Analytics) with academic Support of Samatrix (3 Years)'),
        ('BBA (Hons. with Research) (Business Intelligence & Analytics) with academic Support of Samatrix (4 Years)',
         'BBA (Hons. with Research) (Business Intelligence & Analytics) with academic Support of Samatrix (4 Years)'),
        ('BBA (Travel & Tourism) (3 Years)', 'BBA (Travel & Tourism) (3 Years)'),
        ('BBA (Hons. with Research) (Travel & Tourism) (4 Years)',
         'BBA (Hons. with Research) (Travel & Tourism) (4 Years)'),
        ('BBA (Human Resource) (3 Years)', 'BBA (Human Resource) (3 Years)'),
        (
            'BBA (Hons. with Research) (Human Resource) (4 Years)',
            'BBA (Hons. with Research) (Human Resource) (4 Years)'),
        ('BBA (Marketing) (3 Years)', 'BBA (Marketing) (3 Years)'),
        ('BBA (Hons. with Research) (Marketing) (4 Years)', 'BBA (Hons. with Research) (Marketing) (4 Years)'),
        ('BBA (Finance) (3 Years)', 'BBA (Finance) (3 Years)'),
        ('BBA (Hons. with Research) (Finance) (4 Years)', 'BBA (Hons. with Research) (Finance) (4 Years)'),
        (
            'B.Com. (Hons.) (International Accounting & Finance ) (ACCA-UK) with academic support of Grant Thornton ('
            '3 Years)',
            'B.Com. (Hons.) (International Accounting & Finance ) (ACCA-UK) with academic support of Grant Thornton ('
            '3 Years)'),
        (
            'B.com. (Hons. with Research) (International Accounting & Finance) (ACCA-UK) with academic support of '
            'Grant Thornton (4 Years)',
            'B.com. (Hons. with Research) (International Accounting & Finance) (ACCA-UK) with academic support of'
            'Grant Thornton (4 Years)'),
        ('B.Com. (Hons.) with academic support of NSE Academy (3 Years)',
         'B.Com. (Hons.) with academic support of NSE Academy (3 Years)'),
        ('B.Com. (Hons. with Research) with academic support of NSE Academy (4 Years)',
         'B.Com. (Hons. with Research) with academic support of NSE Academy (4 Years)'),
        ('B.Com. (Hons.) with academic support of NSE Academy (3 Years)',
         'B.Com. (Hons.) with academic support of NSE Academy (3 Years)'),
        ('B.Com. (Hons. with Research) with academic support of NSE Academy (4 Years)',
         'B.Com. (Hons. with Research) with academic support of NSE Academy (4 Years)'),
        (
            'B.Com. Programme with Preparation for Competitive Exam (Banking/ Insurance/ Railways/SSC) for Central '
            'and State Govt. Jobs (3 Years)',
            'B.Com. Programme with Preparation for Competitive Exam (Banking/ Insurance/ Railways/SSC) for Central '
            'and State Govt. Jobs (3 Years)'),
        (
            'BBA LL.B. (Hons.) with Specialization in Business Laws/Criminal Laws/Constitutional laws/International '
            'Laws (5 Years)',
            'BBA LL.B. (Hons.) with Specialization in Business Laws/Criminal Laws/Constitutional laws/International '
            'Laws (5 Years)'),
        (
            'B.Com. LL.B. (Hons.) with Specialization in Business Laws/Criminal Laws/Constitutional '
            'laws/International Laws (5 Years)',
            'B.Com. LL.B. (Hons.) with Specialization in Business Laws/Criminal Laws/Constitutional '
            'laws/International Laws (5 Years)'),
        (
            'B.A. LL.B (Hons.) with Specialization in Business Laws/Criminal Laws/Constitutional laws/International '
            'Laws (5 Years)',
            'B.A. LL.B (Hons.) with Specialization in Business Laws/Criminal Laws/Constitutional laws/International '
            'Laws (5 Years)'),
        (
            'LL.B. (Hons.) with SpecializatioSchooln in Business Laws/Criminal Laws/Constitutional laws/International '
            'Laws (3 Years)',
            'LL.B. (Hons.) with Specialization in Business Laws/Criminal Laws/Constitutional laws/International Laws '
            '(3 Years)'),
        ('Bachelor of Pharmacy (B.Pharm.) (4 Years)', 'Bachelor of Pharmacy (B.Pharm.) (4 Years)'),
        ('Bachelor of Physiotherapy (BPT) (4 Years)', 'Bachelor of Physiotherapy (BPT) (4 Years)'),
        ('B.Pharm. (Lateral Entry) (3 Years)', 'B.Pharm. (Lateral Entry) (3 Years)'),
        (
            'B.A. (Hons.) English with Preparation for Competitive Exam (Banking/ Insurance/ Railways/SSC) for '
            'Central and State Govt Jobs (3 Years)',
            'B.A. (Hons.) English with Preparation for Competitive Exam (Banking/ Insurance/ Railways/SSC) for '
            'Central and State Govt Jobs (3 Years)'),
        (
            'B.A. (Hons. with Research) English with Preparation for Competitive Exam (Banking/ Insurance/ '
            'Railways/SSC) for Central and State Govt Jobs (4 Years)',
            'B.A. (Hons. with Research) English with Preparation for Competitive Exam (Banking/ Insurance/ '
            'Railways/SSC) for Central and State Govt Jobs (4 Years)'),
        (
            'B.A. (Hons.) Economics with Preparation for Competitive Exam (Banking/ Insurance/ Railways/SSC) for '
            'Central and State Govt Jobs (3 Years)',
            'B.A. (Hons.) Economics with Preparation for Competitive Exam (Banking/ Insurance/ Railways/SSC) for '
            'Central and State Govt Jobs (3 Years)'),
        (
            'B.A. (Hons. with Research) Economics with Preparation for Competitive Exam (Banking/ Insurance/ '
            'Railways/SSC) for Central and State Govt Jobs (4 Years)',
            'B.A. (Hons. with Research) Economics with Preparation for Competitive Exam (Banking/ Insurance/ '
            'Railways/SSC) for Central and State Govt Jobs (4 Years)'),
        (
            'B.A. (Hons.) Psychology with Preparation for Competitive Exam (Banking/ Insurance/ Railways/SSC) for '
            'Central and State Govt Jobs (3 Years)',
            'B.A. (Hons.) Psychology with Preparation for Competitive Exam (Banking/ Insurance/ Railways/SSC) for '
            'Central and State Govt Jobs (3 Years)'),
        (
            'B.A. (Hons. with Research) Psychology with Preparation for Competitive Exam (Banking/ Insurance/ '
            'Railways/SSC) for Central and State Govt Jobs (4 Years)',
            'B.A. (Hons. with Research) Psychology with Preparation for Competitive Exam (Banking/ Insurance/ '
            'Railways/SSC) for Central and State Govt Jobs (4 Years)'),
        (
            'B.A. (Hons.) Chinese with Preparation for Competitive Exam (Banking/ Insurance/ Railways/SSC) for '
            'Central and State Govt Jobs (3 Years)',
            'B.A. (Hons.) Chinese with Preparation for Competitive Exam (Banking/ Insurance/ Railways/SSC) for '
            'Central and State Govt Jobs (3 Years)'),
        (
            'B.A. (Hons. with Research) Chinese with Preparation for Competitive Exam (Banking/ Insurance/ '
            'Railways/SSC) for Central and State Govt Jobs (4 Years)',
            'B.A. (Hons. with Research) Chinese with Preparation for Competitive Exam (Banking/ Insurance/ '
            'Railways/SSC) for Central and State Govt Jobs (4 Years)'),
        (
            'B.A. (Hons.) Political Science with Preparation for Competitive Exam (Banking/ Insurance/ Railways/SSC) '
            'for Central and State Govt Jobs (3 Years)',
            'B.A. (Hons.) Political Science with Preparation for Competitive Exam (Banking/ Insurance/ Railways/SSC) '
            'for Central and State Govt Jobs (3 Years)'),
        (
            'B.A. (Hons. with Research) Political Science with Preparation for Competitive Exam (Banking/ Insurance/ '
            'Railways/SSC) for Central and State Govt Jobs (4 Years)',
            'B.A. (Hons. with Research) Political Science with Preparation for Competitive Exam (Banking/ Insurance/ '
            'Railways/SSC) for Central and State Govt Jobs (4 Years)'),
        (
            'B.A. Programme with Preparation for Competitive Exam (Banking/ Insurance/ Railways/SSC) for Central and '
            'State Govt Jobs (3 Years)',
            'B.A. Programme with Preparation for Competitive Exam (Banking/ Insurance/ Railways/SSC) for Central and '
            'State Govt Jobs (3 Years)'),
        ('Bachelor of Architecture (B.Arch) (5 Years)', 'Bachelor of Architecture (B.Arch) (5 Years)'),
        ('Bachelor of Fine Arts (BFA) (4 Years)', 'Bachelor of Fine Arts (BFA) (4 Years)'),
        ('Bachelor of Design (B.Des.) (4 Years)', 'Bachelor of Design (B.Des.) (4 Years)'),
        ('Bachelor of Interior Design (BID) (4 Years)', 'Bachelor of Interior Design (BID) (4 Years)'),
        ('B.Sc. (Hons.) Interior Design (3 Years)', 'B.Sc. (Hons.) Interior Design (3 Years)'),
        ('B.A. Fashion Design (3 Years)', 'B.A. Fashion Design (3 Years)'),
        ('B.Des. (Game Design & Animation) with academic support of ImaginXP (4 Years)',
         'B.Des. (Game Design & Animation) with academic support of ImaginXP (4 Years)'),
        ('B.A. (Journalism And Mass Communication) (3 Years)', 'B.A. (Journalism And Mass Communication) (3 Years)'),
        ('B.A. (Hons. with Research) (Journalism And Mass Communication) (4 Years)',
         'B.A. (Hons. with Research) (Journalism And Mass Communication) (4 Years)'),
        (
            'B.Sc. (Hons.) Physics with Preparation for Competitive Exam (Banking/ Insurance/ Railways/SSC) for '
            'Central and State Govt. Jobs (3 Years)',
            'B.Sc. (Hons.) Physics with Preparation for Competitive Exam (Banking/ Insurance/ Railways/SSC) for '
            'Central and State Govt. Jobs (3 Years)'),
        (
            'B.Sc. (Hons. with Research ) Physics with preparation for Competitive Exam (Banking/ Insurance/ '
            'Railways/SSC) for Central and State Govt. Jobs (4 Years)',
            'B.Sc. (Hons. with Research ) Physics with preparation for Competitive Exam (Banking/ Insurance/ '
            'Railways/SSC) for Central and State Govt. Jobs (4 Years)'),
        (
            'B.Sc. (Hons.) Chemistry with Preparation for Competitive Exam (Banking/ Insurance/ Railways/SSC) for '
            'Central and State Govt. Jobs (3 Years)',
            'B.Sc. (Hons.) Chemistry with Preparation for Competitive Exam (Banking/ Insurance/ Railways/SSC) for '
            'Central and State Govt. Jobs (3 Years)'),
        (
            'B.Sc. (Hons. with Research) Chemistry with preparation for Competitive Exam (Banking/ Insurance/'
            'Railways/SSC) for Central and State Govt. Jobs (4 Years)',
            'B.Sc. (Hons. with Research) Chemistry with preparation for Competitive Exam (Banking/ Insurance/ '
            'Railways/SSC) for Central and State Govt. Jobs (4 Years)'),
        (
            'B.Sc. (Hons.) Maths with Preparation for Competitive Exam (Banking/ Insurance/ Railways/SSC) for Central '
            'and State Govt. Jobs (3 Years)',
            'B.Sc. (Hons.) Maths with Preparation for Competitive Exam (Banking/ Insurance/ Railways/SSC) for Central '
            'and State Govt. Jobs (3 Years)'),
        (
            'B.Sc. (Hons. with Research.) Maths with preparation for Competitive Exam (Banking/ Insurance/ '
            'Railways/SSC) for Central and State Govt. Jobs (4 Years)',
            'B.Sc. (Hons. with Research.) Maths with preparation for Competitive Exam (Banking/ Insurance/ '
            'Railways/SSC) for Central and State Govt. Jobs (4 Years)'),
        ('B.Sc. (Hons.) Forensic Science (3 Years)', 'B.Sc. (Hons.) Forensic Science (3 Years)'),
        ('B.Sc. (Hons. with Research) Forensic Science (4 Years)',
         'B.Sc. (Hons. with Research) Forensic Science (4 Years)'),
        ('Bachelor of Hotel Management and Catering Technology (B.HMCT) (4 Years)',
         'Bachelor of Hotel Management and Catering Technology (B.HMCT) (4 Years)'),
        ('Bachelor of Elementary Education (B.El.Ed.) (4 Years)',
         'Bachelor of Elementary Education (B.El.Ed.) (4 Years)'),
        ('Bachelor of Education (B.Ed.) (2 Years)', 'Bachelor of Education (B.Ed.) (2 Years)'),
        ('B.Sc. (Hons.) Agriculture (4 Years)', 'B.Sc. (Hons.) Agriculture (4 Years)'),
        ('M.Tech. Computer Science and Engineering (2 Years)', 'M.Tech. Computer Science and Engineering (2 Years)'),
        ('M.Tech in VLSI (2 Years)', 'M.Tech in VLSI (2 Years)'),
        ('M.Tech in Power, Electronics and Drive (2 Years)', 'M.Tech in Power, Electronics and Drive (2 Years)'),
        ('M.Tech in Automobile Engineering (2 Years)', 'M.Tech in Automobile Engineering (2 Years)'),
        ('Master of Computer Application (MCA) (2 Years)', 'Master of Computer Application (MCA) (2 Years)'),
        ('Integrated BBA + MBA with academic support of IBM (5 Years)',
         'Integrated BBA + MBA with academic support of IBM (5 Years)'),
        ('MBA with Academic Support of IBM with Various Specializations (2 Years)',
         'MBA with Academic Support of IBM with Various Specializations (2 Years)'),
        ('MBA (Digital Marketing) with academic support of Imarticus Learning (2 Years)',
         'MBA (Digital Marketing) with academic support of Imarticus Learning (2 Years)'),
        ('Master of Commerce (M.Com) (2 Years)', 'Master of Commerce (M.Com) (2 Years)'),
        (
            'LL.M. with Specialization in Corporate Law/Cyber Law/Human Rights/Criminal Law/Intellectual Property '
            'Rights(1 Years)',
            'LL.M. with Specialization in Corporate Law/Cyber Law/Human Rights/Criminal Law/Intellectual Property '
            'Rights(1 Years)'),
        ('Master of Pharmacy (M.Pharm.) - Pharmaceutics (2 Years)',
         'Master of Pharmacy (M.Pharm.) - Pharmaceutics (2 Years)'),
        ('Master of Pharmacy (M.Pharm.) - Pharmacology (2 Years)',
         'Master of Pharmacy (M.Pharm.) - Pharmacology (2 Years)'),
        ('M.A. English (2 Years)', 'M.A. English (2 Years)'),
        ('M.A. Economics (2 Years)', 'M.A. Economics (2 Years)'),
        ('M.A. Applied Psychology (2 Years)', 'M.A. Applied Psychology (2 Years)'),
        ('M.Sc. (Hons.) Part Time (2 Years)', 'M.Sc. (Hons.) Part Time (2 Years)'),
        ('M.A. (Journalism And Mass Communication) (2 Years)', 'M.A. (Journalism And Mass Communication) (2 Years)'),
        ('M.A. in Education (2 Years)', 'M.A. in Education (2 Years)'),
        ('Ph.D. in Computer Science and Engineering', 'Ph.D. in Computer Science and Engineering'),
        ('Ph.D. in Electrical and Electronics Engineering', 'Ph.D. in Electrical and Electronics Engineering'),
        ('Ph.D. in Mechanical Engineering', 'Ph.D. in Mechanical Engineering'),
        ('Ph.D. in Management', 'Ph.D. in Management'),
        ('Ph.D. in Commerce', 'Ph.D. in Commerce'),
        ('Ph.D. in Law', 'Ph.D. in Law'),
        ('Ph.D. in Pharmaceutical Sciences', 'Ph.D. in Pharmaceutical Sciences'),
        ('Ph.D. in English', 'Ph.D. in English'),
        ('Ph.D. in Economics', 'Ph.D. in Economics'),
        ('Ph.D. in Physics', 'Ph.D. in Physics'),
        ('Ph.D. in Chemistry', 'Ph.D. in Chemistry'),
        ('Ph.D. in Mathematics', 'Ph.D. in Mathematics'),
        ('Ph.D. in Journalism and Mass Communication', 'Ph.D. in Journalism and Mass Communication'),
        ('Ph.D. in Education', 'Ph.D. in Education'),
        ('D.Pharm.', 'D.Pharm.'),
    )

    SCHOOL_CHOICES = (
        ('Select Your School', 'Select Your School'),
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
    username = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255)
    roll_number = models.IntegerField(null=True, blank=True)
    School = models.CharField(choices=SCHOOL_CHOICES, max_length=60, null=True, blank=True)
    Branch = models.CharField(choices=COURSE_CHOICES, max_length=255, null=True, blank=True)
    contact_number = models.BigIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(limit_value=9999999999, message='Contact number is too large.')]
    )
    email_id = models.EmailField(max_length=255, null=True, blank=True)
    USERNAME_FIELD = 'username'

    class Meta:
        permissions = [
            ("can_view_superuser", "Can View SuperUser"),
            ("can_view_staff", "Can View Staff"),
        ]

    def __str__(self):
        return self.name


class Complain(models.Model):
    COMPLAIN_CATEGORY = (
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
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Process', 'In Process'),
        ('Resolved', 'Resolved'),
    )
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    complain_type = models.CharField(choices=COMPLAIN_CATEGORY, max_length=80)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    complain_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=100, default='Pending')
    remarks = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updatestatustime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.complain_type

    def save(self, *args, **kwargs):
        if self.pk:
            original_status = Complain.objects.get(pk=self.pk).status
            if self.status != original_status:
                self.updatestatustime = timezone.now()
        super().save(*args, **kwargs)
