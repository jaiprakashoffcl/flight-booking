from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import date
from home.models import S_flight
from home.models import Flight_schedule,places,travel_passenger,payment_details
from datetime import datetime
from django.http import JsonResponse, HttpResponse
import json
from django.core.mail import send_mail


#print(check_password('vdvyas@2307','pbkdf2_sha256$390000$bwUVr9rh4i7MEpPn8m9zgY$0eIwgc7TSJgWsWH4M85m2MCGAK023PtC1kJ8lVWNZwA='))
# Create your views here.
#global Depature,arrive,dept_date,return_date,travel_type,cabin_class

Depature=""
arrive=""
cabin_class=""
dept_date=""
return_date=""
twoway_dept_pnr_no=""
twoway_return_pnr_no=""
oneway_pnr_no=""
Travel_type=""
PNR_no=""
def home(request):
    #return HttpResponse("This is home page")
    return render(request,'base.html')

def service(request):
    return render(request,'services.html')

def booking(request):
    global Depature,cabin_class,arrive,dept_date,return_date,Travel_type
    if request.method=="POST":
       Travel_type=request.POST['checking']
       saverecord=S_flight()
       saverecord.travel_type=request.POST['checking']
       saverecord.depature=request.POST['From']
       Depature = request.POST['From'] 
       saverecord.arrive=request.POST['To']
       arrive=request.POST['To']
       arrive=request.POST['To']
       if Travel_type=="one-way":
           saverecord.return_date=date.today()
       else:
           saverecord.return_date=request.POST['returndate']
           return_date=request.POST['returndate']

       saverecord.depart_date=request.POST['departdate']
       dept_date=request.POST['departdate']
       print(dept_date)
       saverecord.no_of_passenger=request.POST['passenger']
       saverecord.cabin_class=request.POST['cabinclass']
       cabin_class=request.POST['cabinclass']
       saverecord.save()
       #print(travel_type)
       #print(depature)
       #print(arrive)
       if Travel_type=="return":
          print("redirect to return page")
          return redirect('/Return')
       else:
          print("redirect to one-way page")
          return redirect('/oneway')
    return render(request,'booking.html')

def login(request):
     if request.method=="POST":
        number = request.POST['number']
        password = request.POST['password']
        print(number)
        print(password)
        user = authenticate(request, username=number, password=password)
        print(user)
        if user.is_staff:
            auth_login(request, user)
            print("superuser login successfully")
            return redirect('/adminpage')
        if user is not None:
            auth_login(request, user)
            print("login successfully")
            return redirect('/') 

        else:
            print("user is not login")
           # messages.error(request,'Please check password or username')
            return redirect('/login')
     return render(request,'login.html')
     

def register(request):
     if request.method=="POST":
          First_name=request.POST['first_name']
          Last_name=request.POST['last_name']
          Email=request.POST['email']
          Mobile_no=request.POST['mobile_no']
          Password=request.POST['password']
          Confirm_password=request.POST['confirm_password']
          if len(Mobile_no) !=10:
            messages.error(request,'Number should be 10 Digit')
            return redirect('/register')
          elif len(Password) < 8:
             messages.error(request,'password length minimum should be 8 digit')
             return redirect('/register') 
          elif Password!= Confirm_password:
             messages.error(request,'Please check password')
             return redirect('/register') 
          else:
            user=User.objects.create(username=Mobile_no,email=Email,password= make_password(Confirm_password))
            user.first_name= First_name
            user.last_name= Last_name
            user.save()
            print("user register successfully")
            messages.error(request,'your account succefully add')
            return redirect('/')
     return render(request,'register.html')

def handlelogout(request):
    logout(request) 
    return redirect('/')     

def Return(request):
    global Depature,cabin_class,arrive,dept_date,return_date,twoway_dept_pnr_no,twoway_return_pnr_no
    if request.method=="POST":
        twoway_dept_pnr_no = request.POST.get('dpnr')
        twoway_return_pnr_no= request.POST.get('rpnr')
        print("this is return")
        print(twoway_dept_pnr_no)
        print(twoway_return_pnr_no)

        return redirect('/ticketdetails')
    
    
    Flights_one=Flight_schedule.objects.filter(From__icontains=Depature).filter(To__icontains=arrive).filter(everyday__icontains="YES")
    Flights_two=Flight_schedule.objects.filter(From__icontains=arrive).filter(To__icontains=Depature).filter(everyday__icontains="YES")
    return render(request,'return.html', {'flights_one':Flights_one,'flights_two':Flights_two,'Cabin_class': cabin_class.upper() ,'from':Depature,'to': arrive,'Dept_date':dept_date,'Return_date':return_date})

def oneway(request):
     global Depature,cabin_class,arrive,dept_date,oneway_pnr_no
     if request.method=="POST":
        print("redirect to ticketdetails")
        oneway_pnr_no = request.POST.get('dpnr')
        print(oneway_pnr_no)

        return redirect('/ticketdetails')
    
     #depart_day = datetime.strptime(dept_date, "%Y-%m-%d")
     #depart_day=Week.objects.get(number=return_date.weekday())
     Flights=Flight_schedule.objects.filter(From__icontains=Depature).filter(To__icontains=arrive).filter(everyday__icontains="YES")
     return render(request,'oneway.html', {'flights':Flights,'Cabin_class': cabin_class.upper() ,'from':Depature,'to': arrive,'Dept_date':dept_date})

def adminpage(request):
     Flights=Flight_schedule.get_all_product()
     return render(request, 'adminpage.html', {'flights':Flights})

def addflight(request):
    if request.method=="POST":
        saverecord=Flight_schedule()
        saverecord.company_name=request.POST["company_name"]
        saverecord.From=request.POST["from"]
        saverecord.To=request.POST["to"]
        saverecord.pnr_no=request.POST["pnr_no"]
        saverecord.dept_time=request.POST["dept_time"]
        saverecord.rich_time=request.POST["rich_time"]
        saverecord.duration=request.POST["duration"]
        saverecord.economy_seat=request.POST["economy_seat"]
        saverecord.pre_economy_seat=request.POST["pre_economy_seat"]
        saverecord.business_seat=request.POST["business_seat"]
        saverecord.first_class_seat=request.POST["first_class_seat"]
        saverecord.economy_seat_price=request.POST["economy_seat_price"]
        saverecord.pre_economy_seat_price=request.POST["pre_economy_seat_price"]
        saverecord.business_price=request.POST["business_seat_price"]
        saverecord.first_class_seat_price=request.POST["first_class_seat_price"]
        saverecord.date=request.POST["date"]
        saverecord.everyday=request.POST["everyday"]
        print(saverecord.company_name)
        print(saverecord.dept_time)
        saverecord.save()
        return redirect('/addflight')
    return render (request,'addflight.html')

def ticketdetails(request):
    global cabin_class,Travel_type,twoway_dept_pnr_no,twoway_return_pnr_no,oneway_pnr_no
    if Travel_type=="return":
        print(twoway_dept_pnr_no)
        print(twoway_return_pnr_no)
        Flight_ticket_one=Flight_schedule.objects.filter(pnr_no__icontains=twoway_dept_pnr_no)
        Flight_ticket_two=Flight_schedule.objects.filter(pnr_no__icontains=twoway_return_pnr_no)
        zipped_segment= zip(Flight_ticket_one,Flight_ticket_two)
        return render(request,'ticketdetails.html',{'Cabin_class': cabin_class.upper(),'travel_type':Travel_type,'Zipped' : zipped_segment})
    else:
        Flight =Flight_schedule.objects.filter(pnr_no__icontains=oneway_pnr_no)
        print(oneway_pnr_no)
        print(Flight)
        return render(request,'ticketdetails.html',{'Cabin_class': cabin_class.upper(),'flights':Flight,'travel_type':Travel_type})
    
def savepassenger(request):
    if request.method == "POST": 
        #print(request.POST)
         vd =request.POST
         print("this is vd")
         print(vd)
         print(vd["First_name"])
         #print(request.POST[1])
         save_travel_passenger=travel_passenger()
         save_travel_passenger.First_name=vd["First_name"]
         save_travel_passenger.Last_name=vd["Last_name"]
         save_travel_passenger.Gender=vd["Gender"]
         save_travel_passenger.save()
         return JsonResponse({"message" : "request handle.."})
    
def payment(request):
    global Travel_type
    if request.method=="POST":
        saverecord=payment_details()
        saverecord.payment_amount=request.POST['payment-amount']
        saverecord.credit_card_number=request.POST['credit-card-number']
        saverecord.credit_holder_name=request.POST['credit-card-holder-name']
        month=request.POST['expiry-month']
        saverecord.month_year_expiry =datetime.strptime(month,'%Y-%m').date()
        saverecord.cvv_code=request.POST['cvv-code']
        saverecord.save()
        send_mail(
            "Subject here",
            "Here is the message.",
            "flightbooking2307@gmail.com",
            ["vedantvyas2@gmail.com"],
            fail_silently=True,
        ) 
        return HttpResponse("payment is sucessfully and get your boarding pass at airport")
        
    return render(request,'payment.html')