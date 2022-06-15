from django.shortcuts import render
from .models import Question, Choice
from datetime import datetime
from .views import *
# スペースのみかをチェックする
def only_space_check(item):
    return True if required_check(item) and not required_check(item.strip()) else False

# 必須チェックする
def required_check(item):
    return True if len(item) > 0 else False

# 桁数チェック（20桁数）
def length_check(item):
    return True if len(item) > 20 else False

# 選択肢桁数チェック（20桁数）
def select_length_check(selectAll):
    count = 0
    for select in selectAll:
        if length_check(select):
            count += 1
    return True if count > 0 else False
        
# 選択肢数チェック
def select_count_check(selectAll):
    count = 0
    for select in selectAll: 
        if required_check(select.strip()):
            count += 1
    return True if count > 1 else False

# 選択肢重複チェック
def select_double_check(selectAll):
    checkArray=[]
    for select in selectAll:
        if not only_space_check(select) and required_check(select):
            checkArray.append(select.strip())
    return len(checkArray) != len(set(checkArray))

# 質問重複チェック
def question_double_check(question):
    question_list = Question.objects.all()
    for que in question_list:
        if str(question.strip()) == que.question_text:
            return True
    return False
    
# 日付Fromチェック
def validate_date_form_check_from(value):
    if len(value) == 10 :
        try:
            if "/"== value[4] and "/"== value[7]:
                return datetime.strptime(value, '%Y/%m/%d')
            elif "-"== value[4] and "-"== value[7]:
                return datetime.strptime(value, '%Y-%m-%d')

        except ValueError:
            False

    elif len(value) == 8 :
        try:
            return datetime.strptime(value, '%Y%m%d')

        except ValueError:
            False

    elif len(value) != 10 and value == str:
        context = {
            'error_massage5':"正しい日付フォーマットで入力してください。",}
            
        return render(value, 'polls/index.html/',context)

# 日付Toチェック
def validate_date_form_check_to(value):
    if len(value) == 10 :
        try:
            value2 = value[8:10]
            value3 = int(value2) + 1
            value4 = str(value3)
            value5 = value.replace(value[8:10],value4)

            if "/"== value[4] and "/"== value[7]:
                return datetime.strptime(value5, '%Y/%m/%d')
            elif "-"== value[4] and "-"== value[7]:
                return datetime.strptime(value5, '%Y-%m-%d')

        except ValueError:
            False

    elif len(value) == 8:
        try:
            value2 = value[6:8]
            value3 = int(value2) + 1
            value4 = str(value3)
            value5 = value.replace(value[6:8],value4)
            return datetime.strptime(value5, '%Y%m%d')

        except ValueError:
            False
    
    elif len(value) != 8 and value == str:
        context = {
            'error_massage5':"正しい日付フォーマットで入力してください。",}
            
        return render(value, 'polls/index.html/',context)
    
#modify質問重複チェック
def question_double_check_modify(old_question, new_question):
    all_question_list = list(Question.objects.all())
    check_question_list = []

    for i in range(len(all_question_list)): # 重複質問チェック
        if not all_question_list[i] == old_question:
            check_question_list.append(all_question_list[i].question_text)

    for chk_question in check_question_list:
        if str(new_question.strip()) == chk_question:
            return True

    return False
