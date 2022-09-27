from symbol import pass_stmt
from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        bio = request.POST.get('bio', None)
        
        if password != password2:
            return render(request, 'user/signup.html')
        else:
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'user/signup.html')
            else:
                UserModel.objects.create_user(username=username, password=password, bio=bio)
            return redirect('/sign-in')


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        
        me = auth.authenticate(request, username=username, password=password)
        if me is not None:
            auth.login(request, me)
            return redirect('/')
        else:
            return redirect('/sign-in')
    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')


# user/views.py 

@login_required
def user_view(request):  
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)  # 지금 로그인 한 유저이름(내 이름)을 제외한 모든 사용자 리스트를 가져오겠다.
        return render(request, 'user/user_list.html', {'user_list': user_list})  # html을 user_list랑 같이 보여줄거다 


@login_required
def user_follow(request, id):
    me = request.user  #나를 설정
    click_user = UserModel.objects.get(id=id)  #내가 방금 누른 사람
    if me in click_user.followee.all():  # 내가 누른 사람을 팔로우하는 모든 사람들 중에 내가 들어가 있다면 그 팔로우 리스트에서 나를 뺀다.
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)  #없다면 나는 내가 방금 누른 사람들 팔로우 하겠다.
    return redirect('/user')