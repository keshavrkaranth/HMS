from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
import calendar
import datetime
from django.core.exceptions import ObjectDoesNotExist


def homepage(request):
    return render(request, 'index.html')


def user_registration(request):
    form = registrationForm()
    if request.method == 'POST':
        form = registrationForm(data=request.POST)
        if form.is_valid():
            x = form.cleaned_data
            y = User.objects.create(username=x['Username'].upper(
            ), email=x['Email'], password=x['password'])
            y.set_password(y.password)
            y.save()
            stu = Student.objects.create(user=y, student_name=x['Name'], student_mbl_no=x['Phone_no'], adress=x['Adress'], father_name=x[
                                         'Father_name'], father_mbl_no=x['Father_mbl_no'], USN=x['USN'].upper(), Branch=x['Branch'], dob=x['DOB'], gender=x['Gender'])
            stu.save()
            auth = authenticate(
                request, username=x['Username'].upper(), password=x['password'])
            if auth is not None:
                if auth.is_active:
                    login(request, auth)
                    return redirect('hostelapp:get_room')
    return render(request, 'signup.html', {'form': form})

@login_required
def get_room(request):
    rooms = ''
    try:
        gen = request.user.student.gender
        obj = Hostel.objects.get(gender=gen)
        rooms = Room.objects.filter(hostel=obj.id)
    except:
        pass
    return render(request, 'room.html', {'room': rooms})

@login_required
def select_room(request, pk):
    try:
        room = Room.objects.get(pk=pk)
        if room.room_type == 'S':
            stu = Student.objects.get(pk=request.user.student.id)
            stu.room = room
            stu.room_allotted = True
            room.current_no_of_persons +=1
            room.vacant = False
            room.save()
            stu.save()
            return redirect('hostelapp:leave')
        else:
            stu = Student.objects.get(pk=request.user.student.id)
            stu.room = room
            stu.room_allotted = True
            room.current_no_of_persons +=1
            room.save()
            if room.current_no_of_persons == room.max_no_of_persons:
                room.vacant = False
                room.save()
            stu.save()
            return redirect('hostelapp:leave')
    except:
        pass
    return render(request,'Student_profile.html')


def user_login(request):
    context = ''
    if request.method == 'POST':
        username = request.POST.get('Username').upper()
        password = request.POST.get('Password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_warden:
                if user.is_active:
                    login(request, user)
                    return redirect('hostelapp:warden_home')

            else:
                if user.is_active:
                    login(request, user)
                    return redirect("hostelapp:leave")

        else:
            context = 'Disabled acc contact Your warden or Admin'

    return render(request, 'Login.html', {'message': context})


@login_required
def warden_homepage(request):
    user = request.user
    if user is not None:
        if user.is_warden:
            warden = request.user.warden.hostel
            stud = Student.objects.filter(room__hostel=warden)
        else:
            return HttpResponse("You are Not warden")

    return render(request, 'wardenindex.html',{'student':stud})


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'index.html')


@login_required
def student_profile(request):
    stu = Student.objects.get(pk=request.user.student.id)
    return render(request,'Student_profile.html',{'student':stu})



@login_required
def user_leave(request):
    form = LeaveForm()
    if request.method == "POST":
        form = LeaveForm(data=request.POST)

        if form.is_valid() and request.user.student.room_allotted:
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            delta = end-start
            if delta.days >= 0 and (start-datetime.date.today()).days >= 0:
                usr_contr = Leave.objects.filter(
                    student=request.user.student, start_date__lte=end, end_date__gte=start
                )
                count = usr_contr.count()
                count = int(count)
                if count == 0:
                    leave_form = form.save(commit=False)
                    student = request.user.student
                    leave_form.student = student
                    leave_form.save()
                    leaves = Leave.objects.filter(student=request.user.student)

                    return render(request, 'Student_profile.html', {'student': student, 'leaves': leaves})
                else:
                    return HttpResponse('<h3>Already have a Leave in this period Try another</h3>  <br> '
                                        '<a href = \'\' style = "text-align: center; color: Red ;"> Apply Leave </a> ')
            else:
                return HttpResponse('<h2> Invalid Date </h2> <br>  <a href = \'\' '
                                    'style = "text-align: center; color: Red ;"> Apply Leave </a> ')
        elif not request.user.student.room_allotted:
            return HttpResponse('<h3>First Select a Room </h3> <br> <a href = \'select\''
                                ' style = "text-align: center; color: Red ;"> SELECT ROOM </a> ')
        else:
            form = LeaveForm()
            return render(request, 'leave_form.html', {'form': form})
    else:
        form = LeaveForm()
    user = request.user.student
    leave = Leave.objects.filter(student= user)

    return render(request, 'leave.html', {'form': form,'leav':leave})

@login_required
def maintainence(request):
    context = ''
    form = RepairForm()
    if request.method == 'POST':
        form = RepairForm(data=request.POST)
        if form.is_valid() and request.user.student.room_allotted:
            repair = form.cleaned_data['repair']
            room = request.user.student.room
            room.repair = repair
            room.save()
            context = 'Complient Registered'
            return redirect('hostelapp:student_profile')
        elif not request.user.student.room_allotted:
            return HttpResponse("Plz Select Room Before Registering Complient")

    else:
        form = RepairForm()
    return render(request, 'repair.html', {'form': form, 'context': context})

@login_required
def Warden_add_room(request):
    form = RoomForm()
    msg = ''
    if request.method == 'POST':
        gender = request.user.warden.hostel.gender
        hos = Hostel.objects.get(gender=gender)
        form = RoomForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['Room_Type'] == 'S':
                room = Room.objects.get_or_create(no=data['Room_No'],room_type='S',max_no_of_persons=1,current_no_of_persons=0,
                                                  vacant=True,hostel=hos)
                msg = 'Room added Sucessfully'
            else:
                room = Room.objects.get_or_create(no=data['Room_No'], room_type='D', max_no_of_persons=2,
                                                  current_no_of_persons=0,
                                                  vacant=True, hostel=hos)
                msg = 'Room added Sucessfully'
    return render(request,'addroom.html',{'form':form,'message':msg})


def leave_applications(request):
    warden_hostel = request.user.warden.hostel
    stud = Student.objects.filter(room__hostel=warden_hostel)
    leave = Leave.objects.filter(student__in=stud).filter(accept=False, reject=False)
    today = datetime.datetime.now().date()
    yesterday = today - datetime.timedelta(15)
    accepted_leaves = Leave.objects.filter(student__in=stud, accept=True,
                                         ). \
        order_by('-confirm_time')

    return render(request,'leaveapplication.html',{'leav':leave,'accepted_leave':accepted_leaves})


def accept_leave(request,pk):
    leave = Leave.objects.get(pk=pk)
    try:
        leave.accept = True
        leave.save()
    except:
        pass
    return redirect('hostelapp:leaveapplications')


def reject_leave(request,pk):
    leave = Leave.objects.get(pk=pk)
    try:
        leave.reject = True
        leave.save()
    except:
        pass
    return redirect('hostelapp:leaveapplications')



def wardenroom_grivelences(request):
    user = request.user
    if user is not None:
        if user.is_warden:
            warden = request.user.warden.hostel
            stud = Student.objects.filter(room__hostel=warden)

        else:
            return HttpResponse("You are Not warden")

    return render(request,'wardengrivelences.html',{'room':stud})



def warden_resolve(request,pk):
    room = Room.objects.get(pk=pk)
    room.repair = ""
    room.save()
    return redirect('hostelapp:roomgrivelences')


def feedback(request):
    form = LoginForm()
    context = ''
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data

            user = authenticate(request, username=data['username'], password=data['password'])
            if user:
                if user is not None:
                    if user.is_warden:
                        context = 'warden are not allowed to give feedback'
                    else:
                        if user.is_active:
                            login(request, user)
                            return redirect("hostelapp:feedback_home")
            else:
                context = 'Invalid credentials'

    else:

        print('eoor')
    feed = Feedback.objects.order_by('rating')

    return render(request,'feedback.html',{'form':form,'feedback':feed,'msg':context})


def feedback_home(request):
    form = FeedbackForm()
    if request.method == 'POST':
        usr = request.user.student.id
        stu = Student.objects.get(id=usr)

        form = FeedbackForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            feed = Feedback.objects.create(student = stu,review=data['Review'],rating=data['rating'])
            feed.save()
            return redirect('hostelapp:feedback')
    return render(request,'feedback_home.html',{'form':form})


def profile(request):
    usr = request.user.student.student_name
    student = Student.objects.get(student_name=usr)

    return render(request,'profile.html',{'stu':student})


def update_profile(request,pk):
    form = updateprofile()
    if request.method=='POST':
        stu = Student.objects.get(id=pk)
        form = updateprofile(request.POST,instance=stu)
        if form.is_valid():
            form.save()
    return render(request,'update_profile.html',{'form':form})