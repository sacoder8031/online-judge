from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from .models import *
from background_task import background
import os


# Create your views here.

compile_lang = ['c', 'cpp',]


@background(schedule=0)
def compile_run(submission_id):

    def done():
        os.system(f'rm -fr /home/guest/{submission_id}')
    

    submission = Submission.objects.get(pk=submission_id)
    ques = submission.ques
    testcases = ques.testcases.all()
    lang = submission.lang
    data = submission.user.userdata
    
    os.system(f'mkdir /home/guest/{submission_id}')
    DIR = f'/home/guest/{submission_id}'

    # executes this command using ubuntu user
    with open(f'{DIR}/{submission_id}.{lang}', 'w') as f:
        f.write(submission.code)

    # compile code in case of c and c++
    if lang in compile_lang:
        compile = 0

        if lang == 'c':
            compile = os.system(f'gcc {DIR}/{submission_id}.{lang} -o {DIR}/{submission_id}')
            
        if lang == 'cpp':
            compile = os.system(f'g++ {DIR}/{submission_id}.{lang} -o {DIR}/{submission_id}')

        if compile != 0:
            submission.verdict = 'Compilation Error'
            submission.save()
            done()
            return

        else:
            submission.verdict = 'Compiled'
            submission.save()



    # command for executing code (language specific)
    cmd = ''
    if lang in ['c', 'cpp']:
        cmd = f'{DIR}/{submission_id}'
    elif lang == 'py':
        cmd = f'python3 {DIR}/{submission_id}.{lang}'
    


    # Testing begins...
    for i, testcase in enumerate(testcases):
        submission.verdict = f'Running on Testcase {i + 1}'
        submission.save()

        with open(f'{DIR}/{submission_id}.tc', 'w') as f:
            f.write(testcase.testcase) 
        with open(f'{DIR}/{submission_id}.ans', 'w') as f:
            f.write(testcase.answer)
        
        err_code = os.system(f'sudo su - guest -c "schroot -c compile-run -- timeout {ques.timelimit} {cmd} < {DIR}/{submission_id}.tc" > {DIR}/{submission_id}.out')
        
        # err_code = os.system(f'timeout {ques.timelimit} {cmd} < {DIR}/{submission_id}.tc > {DIR}/{submission_id}.out')
        
        if err_code == 31744:
            submission.verdict = f'Time Limit Exceeded on Testcase {i + 1}'
            submission.save()
            done()
            data.timelimit += 1
            data.save()
            return

        elif err_code != 0:
            submission.verdict = f'Runtime Error on Testcase {i + 1}'
            submission.save()
            done()
            data.runtime += 1
            data.save()
            return
        
        match = os.system(f'diff -ZB {DIR}/{submission_id}.out {DIR}/{submission_id}.ans')
        
        if match != 0:
            submission.verdict = f'Wrong Answer on Testcase {i + 1}'
            submission.save()
            done()
            data.incorrect += 1
            data.save()
            return
    
    data = submission.user.userdata

    submission.verdict = f'Correct Answer!!'
    data.correct += 1
    data.save()
    submission.save()
    done()

    for tag in ques.tags.all():
        if tag.name not in data.tags:
            data.tags[tag.name] = 1
        else:
            data.tags[tag.name] = data.tags[tag.name] + 1
    
    data.save()

    return

        


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    recent_blog = Blog.objects.all().last()
    user = User.objects.get(username=request.user)
    mydata = user.userdata
    context = {"blog": recent_blog, "notifications": mydata.notifications, "recent_subs": user.submissions.all().order_by('-id')[:5], "page_name": "home_page"}
    return render(request,"users/home_page.html", context=context)


def home_page_blog(request, blog_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    user = User.objects.get(username=request.user)
    blog = Blog.objects.get(pk=blog_id)
    mydata = user.userdata
    context = {"blog": blog, "notifications": mydata.notifications, "recent_subs": user.submissions.all().order_by('-id')[:5], "page_name": "home_page"}
    return render(request,"users/home_page.html", context=context)
    

def login_view(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"users/login.html")
    return render(request,"users/login.html")

def logout_view(request):
    logout(request)
    return render(request,"users/login.html")

def home_page(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    recent_blog = Blog.objects.all().last()
    user = User.objects.get(username=request.user)
    mydata = user.userdata
    context = {"blog": recent_blog, "notifications": mydata.notifications, "recent_subs": user.submissions.all().order_by('-id')[:5], "page_name": "home_page"}
    return render(request,"users/home_page.html", context=context)

contests=Contest.objects.all()
cur_date=datetime.datetime.now()

def lab_works(request):
    return render(request, "users/lab_works.html",{
        "page_name":"lab_works","contests":contests , "cur_date":cur_date
    })


#For enlisting Tutorials of each Contest
blogs=Blog.objects.all()

def tutorial(request):
    return render(request, "users/tutorial.html",{
        "page_name":"tutorial","blogs":blogs
    })

def profile(request):
    user = User.objects.get(username=request.user)
    mydata = user.userdata
    tag_names = []
    tag_values = []
    if not mydata.tags["isnull"]:
        for i in mydata.tags:
            if i != "isnull":
                tag_names.append(i)
                tag_values.append(mydata.tags[i])

    return render(request, "users/profile.html",{
        "page_name":"profile",
        "user": user,
        "data": mydata,
        "tot_sub": mydata.correct + mydata.incorrect + mydata.timelimit + mydata.runtime,
        "tag_names": tag_names,
        "tag_values": tag_values,
        "submissions": user.submissions.all().order_by('-id')[:5]
    })



def practice(request):
    user = User.objects.get(username=request.user)
    questions=Question.objects.all()
    submissions=Submission.objects.filter(user=user)
    return render(request, "users/practice.html" , {"page_name":"practice_problems","questions":questions , "submissions":submissions , "user":user})

def problem_statement(request,question_id):
    question = Question.objects.get(pk=question_id)
    tags=question.tags.all()
    return render(request, "users/problem_statement.html", {"page_name":"Problem_Statement#"+str(question_id),"question_id":question_id,"questions":question,"tags":tags})

def submit(request, ques_id):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        ques = Question.objects.get(pk=ques_id)
        code = request.POST["code"]
        lang = request.POST["lang"]
        submission = Submission.objects.create(user=user, ques=ques, code=code, lang=lang)
        submission.save()
        compile_run(submission.id)

    ques = Question.objects.get(pk=ques_id)
    tags = ques.tags.all()
    blog_id = ques.contest.blog.id
    return render(request, "users/submit.html", {"page_name":"submit problem", "ques_id": ques_id, "tags": tags, "name": ques.name, "blog_id": blog_id})

#Retreiving Problems of a contest

def contest_page(request,contest_id):
    contest=Contest.objects.get(pk=contest_id)
    question = contest.questions.all()
    return render(request, "users/contest_page.html", {"page_name":"lab#"+str(contest_id),"question":question,"contest_id":contest_id})

def developers(request):
    return render(request, "users/developers.html", {"page_name":"Developers"})

def mentors(request):
    return render(request, "users/mentors.html", {"page_name":"Mentors"})
