# エラーメッセージ一覧
class error_message:
    def question_required():
        return '質問を入力してください。'
    def only_space():
        return '質問に文字を入力してください。'
    def length(name, number=20):
        return '{0}は{1}桁数以内に入力してください'.format(name, number)
    def question_double():
        return 'この質問は既に存在しています。'
    def select_count():
        return '選択肢を2つ以上入力してください。'
    def select_double():
        return '選択肢が重複しないように登録してください。'
