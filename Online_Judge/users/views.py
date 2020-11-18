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
    
    def incorrect():
        done()
        submission.user.userdata.incorrect += 1
        submission.user.userdata.save()
    
    submission = Submission.objects.get(pk=submission_id)
    ques = submission.ques
    testcases = ques.testcases.all()
    lang = submission.lang
    
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
            incorrect()
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
            incorrect()
            return

        elif err_code != 0:
            submission.verdict = f'Runtime Error on Testcase {i + 1}'
            submission.save()
            incorrect()
            return
        
        match = os.system(f'diff -ZB {DIR}/{submission_id}.out {DIR}/{submission_id}.ans')
        
        if match != 0:
            submission.verdict = f'Wrong Answer on Testcase {i + 1}'
            submission.save()
            incorrect()
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
    return render(request,"users/user.html")

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
    return render(request, "users/home_page.html",{
        "page_name":"home_page"
    })

def lab_works(request):
    return render(request, "users/lab_works.html",{
        "page_name":"lab_works"
    })

def tutorial(request):
    return render(request, "users/tutorial.html",{
        "page_name":"tutorial"
    })

def profile(request):
    return render(request, "users/profile.html",{
        "page_name":"profile"
    })

def practice(request):
    return render(request, "users/practice.html" , {"page_name":"practice_problems"})

def problem_statement(request):
    return render(request, "users/problem_statement.html", {"page_name":"problem_statemet"})

def submit(request):
    return render(request, "users/submit.html", {"page_name":"submit problem"})

def contest_page(request):
    return render(request, "users/contest_page.html", {"page_name":"lab #1"})

def developers(request):
    return render(request, "users/developers.html", {"page_name":"Developers"})

def mentors(request):
    return render(request, "users/mentors.html", {"page_name":"Mentors"})
