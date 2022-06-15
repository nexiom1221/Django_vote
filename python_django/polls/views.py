from genericpath import exists
from secrets import choice
from time import time
from django.template import RequestContext
from django.views import generic
from django.db.models import Q
from xmlrpc.client import DateTime
from wsgiref.simple_server import sys_version
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime,date,timedelta
from django.core.paginator import Paginator
from .models import Question, Choice
from .checkMethod import *
from .errorMessage import *
from django.utils.functional import cached_property

def index(request):
    search = request.GET.get("search", "")
    searchDateFrom = request.GET.get("searchDateFrom","")
    searchDateTo = request.GET.get("searchDateTo","")
    From = validate_date_form_check_from(searchDateFrom)
    To = validate_date_form_check_to(searchDateTo)
    date_today = datetime.now() + timedelta(days=1)
    date_today_from = datetime.now() - timedelta(days=1)
    pages = 0
   
    # 検索条件(質問、日付)
    if search != '':
        all_questions = Question.objects.filter(question_text__contains=search)
    elif searchDateTo != '' and searchDateFrom != '':
        all_questions = Question.objects.filter(pub_date__range=[From, To ])
    elif searchDateFrom != '':
        if len(searchDateFrom) == 10 or From == str:
            searchDateFrom = str(searchDateFrom)
        all_questions = Question.objects.filter(pub_date__range=[From, date.today()+timedelta(days=1) ])
    elif searchDateTo != '':
        all_questions = Question.objects.filter(pub_date__range=[date.today() - timedelta(days=10000), To ])
    elif search == "":
        all_questions = Question.objects.all().order_by('-pub_date')  
    if search != '' and searchDateTo != '' and searchDateFrom != '':
        all_questions = Question.objects.filter(question_text__contains=search, pub_date__range=[From, To ])
    elif search != '' and searchDateFrom != '':
        all_questions = Question.objects.filter(question_text__contains=search, pub_date__range=[From, date.today()])
    elif search != '' and searchDateTo != '':
        all_questions = Question.objects.filter(question_text__contains=search, pub_date__range=[date.today() - timedelta(days=10000), To])
    if len(searchDateTo) == 10 and searchDateTo == str:            
        all_questions = Question.objects.all().order_by('pub_date')
    else:
        pass
    if len(search) > 10:
        all_questions = Question.objects.all().order_by('pub_date')
    else:
        pass

    page = int(request.GET.get('page', 1)) # URLからpageの値を取得するときに使用、page値なしで呼び出された場合にはデフォルトで 1 という値を設定する
    paginator = Paginator(all_questions, 7) # all_questions:質問全体、7:ページごとに表示する質問の数
    questions = paginator.get_page(page) # 要求されたページに対応するページングオブジェクトを生成
    for question in questions:
        question.pub_date = question.pub_date.strftime("%Y-%m-%d")
    # これにより、Django内部では、データ全体を照会するのではなく、そのページのデータのみを照会するようにクエリが変更される
    
    # 前のページに戻る
    for i in questions.paginator.page_range:
        if i == questions.number:
            pages = i
            request.session['pages'] = i

    request.session['search'] = request.GET.get("search", "")
    request.session['searchDateFrom'] = request.GET.get("searchDateFrom","")
    request.session['searchDateTo'] = request.GET.get("searchDateTo","")

    context = {
        'questions':questions,
        'search':search,
        'searchDateFrom':searchDateFrom,
        'searchDateTo':searchDateTo,
        'To':To,
        'From':From,
        'error_massage':"正しい日付範囲をセットしてください。",
        'error_massage2':"日付Toは最大本日の日付にセットしてください。",
        'error_massage3':"日付Fromは本日より大きな日付は入力出来ません。",
        'error_massage4':"日付FromとToは本日より大きな日付は入力出来ません。",        
        'error_massage5':"正しい日付フォーマットで入力してください。",
        'error_massage6':"質問がありません。",        
        'date_today': date_today,
        'date_today_from': date_today_from,
        'pages':pages,
        'search':request.session['search'],
        'searchDateFrom':request.session['searchDateFrom'],
        'searchDateTo':request.session['searchDateTo'],
    }

    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    all_choice = question.choice_set.all()
    all_choice_votes = []
    view_select = {}

    for i in all_choice:
        all_choice_votes.append(i.votes)
    if all_choice_votes.count(0) != len(all_choice_votes):
        view_select['nomodify'] = 0

    return render(request, 'polls/detail.html', {'question':question, 'view_select':view_select, 'pages':request.session['pages'],'search':request.session['search'],
        'searchDateFrom':request.session['searchDateFrom'],'searchDateTo':request.session['searchDateTo'], })

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question':question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    all_choice = question.choice_set.all()
    all_choice_votes = []
    view_select = {}
    for i in all_choice:
        all_choice_votes.append(i.votes)

    if all_choice_votes.count(0) != len(all_choice_votes):
        view_select['nomodify'] = 0

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "選択肢を選んでください。",
            'view_select': view_select,
            'pages':request.session['pages'],
            'search':request.session['search'],
            'searchDateFrom':request.session['searchDateFrom'],
            'searchDateTo':request.session['searchDateTo'],
        })

    else:
        selected_choice.votes +=1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def create(request):
    if request.method == 'POST':
        # 入力された質問と選択肢を取得する
        select_all = {}
        for select in request.POST:
            value = request.POST.get(select, None)
            select_all["{}".format(select)] = value
        question = select_all.pop('question')
        select_all.pop('csrfmiddlewaretoken')
        
        # errorメッセージ
        error_messages = [] 
        
        # 質問必須チェック
        if not required_check(question):
            error_messages.append(error_message.question_required())
        
        # 質問スペースのみチェック
        if only_space_check(question):
            error_messages.append(error_message.only_space())

        # 質問桁数チェック
        if length_check(question):
            error_messages.append(error_message.length("質問"))
        
        # 質問重複チェック
        if question_double_check(question):
            error_messages.append(error_message.question_double())
        
        # 選択肢数（必須）チェック
        if not select_count_check(select_all.values()): 
            error_messages.append(error_message.select_count())

        # 選択肢重複チェック
        if select_double_check(select_all.values()):
            error_messages.append(error_message.select_double())
        
        # 選択肢桁数チェック
        if select_length_check(select_all.values()):
            error_messages.append(error_message.length("選択肢"))

        if not len(error_messages):
            pub_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            question = Question.objects.create(question_text=question.strip(), pub_date=pub_date)
            for select in select_all.values():
                if not only_space_check(select) and required_check(select):
                    Choice.objects.create(choice_text=select.strip(), question_id=question.id)
            return redirect('/polls')
        return render(request, 'polls/create.html', {'error_messages':error_messages, 'select_all':select_all, 'question':question})
    else:
        return render(request, 'polls/create.html')

def delete(request, question_id):
    if request.method == "GET":
        question = get_object_or_404(Question, pk=question_id)
        return render(request, 'polls/delete.html', {'question':question, 'pages':request.session['pages'], 'search':request.session['search'],
            'searchDateFrom':request.session['searchDateFrom'],
            'searchDateTo':request.session['searchDateTo'],})

    elif request.method == "POST":
        question = get_object_or_404(Question, pk=question_id)
        question.delete()
        return redirect('/polls/')

def modify(request, question_id):
    if request.method == 'POST':
        # 入力された質問と選択肢を取得する
        old_question = Question.objects.get(pk=question_id)
        old_choice = old_question.choice_set.all()
        select_all = {}
        for select in request.POST:
            value = request.POST.get(select, None)
            select_all["{}".format(select)] = value
        new_question = select_all.pop('question')
        select_all.pop('csrfmiddlewaretoken')

        # errorメッセージ
        error_messages = [] 
        # 質問必須チェック
        if not required_check(new_question):
            error_messages.append(error_message.question_required())
        # 質問スペースのみチェック
        if only_space_check(new_question):
            error_messages.append(error_message.only_space())
        # 質問桁数チェック
        if length_check(new_question):
            error_messages.append(error_message.length("質問"))
        # 選択肢数（必須）チェック
        if not select_count_check(select_all.values()): 
            error_messages.append(error_message.select_count())
        # 選択肢重複チェック
        if select_double_check(select_all.values()):
            error_messages.append(error_message.select_double())
        # 選択肢桁数チェック
        if select_length_check(select_all.values()):
            error_messages.append(error_message.length("選択肢"))
        # MODIFY質問重複チェック 
        if question_double_check_modify(old_question, new_question):
            error_messages.append(error_message.question_double())

        if not len(error_messages):
            pub_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            old_question.question_text = new_question.strip()
            old_question.pub_date = pub_date
            old_question.save()

            # 既にあったデータを消して新しく変更したデータを入れる
            for i in range(len(old_choice)):
                old_question.choice_set.filter(choice_text=old_choice[i]).delete()

            for select in select_all.values():
                if not only_space_check(select) and required_check(select):
                    old_question.choice_set.create(choice_text=select.strip())
            return redirect('/polls')

        return render(request, 'polls/modify.html', {'error_messages':error_messages, 'select_all':select_all, 'new_question':new_question, 'old_question':old_question})

    else:
        question = Question.objects.get(pk=question_id)
        old_question = Question.objects.get(pk=question_id)
        old_choice = old_question.choice_set.all()

        view_select = {'view_select':1}
        old_choice_votes = []
        no_modify = {}
        for i in old_choice:
            old_choice_votes.append(i.votes)

        if old_choice_votes.count(0) != len(old_choice_votes):
            no_modify['no_modify']= 0
            return render(request, '404.html', {'question':question, 'view_select':view_select, 'no_modify':no_modify})
        else:
            return render(request, 'polls/modify.html', {'question':question, 'view_select':view_select, 'no_modify':no_modify})


# 404、500エラー処理
class menuMixin(object):
    @cached_property
    def getMenuList(self):
        print("getMenuList")
        return {"blog_menu":Question.objects.all(),
                "coding_menu": Choice.objects.all()}

# 404、500エラー処理
def handler500(request):
    context = menuMixin().getMenuList
    response = render(request, "404.html", context=context)
    response.status_code = 500
    return response