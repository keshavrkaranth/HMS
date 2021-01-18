from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_warden = models.BooleanField(default=False)

# trigger


class Student(models.Model):
    BRANCHES = [('CS', 'Computer Science'), ('IS', 'Information Science'), ('EC', 'Electronics And Communication'),
                ('EEE', 'Electrical And Electronics'), ('ME', 'Mecanical')]
    user = models.OneToOneField(
        User,
        default=None,
        null=True,
        on_delete=models.CASCADE)
    gender_choices = [('M', 'Male'), ('F', 'Female')]
    student_name = models.CharField(max_length=200, null=True)
    student_mbl_no = models.BigIntegerField(default=None, null=True)
    adress = models.CharField(max_length=256, default=None, null=True)
    father_name = models.CharField(max_length=200, null=True)
    father_mbl_no = models.BigIntegerField(default=None, null=True)
    USN = models.CharField(max_length=10, unique=True, null=True)
    Branch = models.CharField(max_length=4, choices=BRANCHES)
    dob = models.DateField(
        max_length=10,
        help_text="format : YYYY-MM-DD",
        null=True)
    gender = models.CharField(
        choices=gender_choices,
        max_length=1,
        default='N', null=True)
    room = models.ForeignKey(
        'Room',
        blank=True,
        on_delete=models.SET_NULL,
        null=True)
    room_allotted = models.BooleanField(default=False)
    no_dues = models.BooleanField(default=True)


    def __str__(self):
        return str(self.student_name)

    def delete(self, *args, **kwargs):
        room_del = Room.objects.filter(student__room=self.room)
        for s in room_del:
            s.vacant = True
            s.save()
        super(Student, self).delete(*args, **kwargs)


class Room(models.Model):
    room_choice = [('S', 'Single Occupancy'), ('D', 'Double Occupancy') ]
    no = models.CharField(max_length=20)
    room_type = models.CharField(
        choices=room_choice, max_length=1, default=None)
    max_no_of_persons = models.PositiveIntegerField(default=2)
    current_no_of_persons = models.PositiveIntegerField(default=0,blank=True,null=True)
    vacant = models.BooleanField(default=False)
    hostel = models.ForeignKey('Hostel', on_delete=models.CASCADE)
    repair = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return '%s %s' % (self.no, self.hostel)

    def delete(self, *args, **kwargs):
        stud = Student.objects.filter(room=self)
        for s in stud:
            s.room_allotted = False
            s.save()
        super(Room, self).delete(*args, **kwargs)



class Hostel(models.Model):
    name = models.CharField(max_length=50)
    gender_choices = [('M', 'Male'), ('F', 'Female')]
    gender = models.CharField(
        choices=gender_choices,
        max_length=1,
        default=None,
        null=True)
    caretaker = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Warden(models.Model):
    user = models.OneToOneField(
        User,
        default=None,
        null=True,
        on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phoneno = models.CharField(max_length=12, default=None,blank=True,null=True)
    hostel = models.ForeignKey('Hostel', default=None, null=True,
                               on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.user.is_warden is False:  # Set default reference
            self.user.is_warden = True
            self.user.save()
        super(Warden, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.user.is_warden = False
        self.user.save()

        super(Warden, self).delete(*args, **kwargs)

# stored procedure


class Leave(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=100, blank=False)
    accept = models.BooleanField(default=False)
    reject = models.BooleanField(default=False)
    confirm_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.USN} '


class created_date(models.Model):
    user = models.CharField(max_length=20)
    created_date = models.DateField()
