def reading(user_name):
    import json
    import string
    from operator import itemgetter
    from termcolor import cprint

    cprint('-----------------------------', color='green')
    lol = string.ascii_lowercase + string.digits + string.ascii_uppercase + ' .,!?;:'

    with open('data_scores.json', 'r') as ds:
        data = json.load(ds)
    scores = []

    for item in data:
        temp_name = item['Name: ']
        temp_score = item['Score: ']
        temp_answers = item['Answers: ']
        if temp_name == user_name:
            scores.append((temp_name, temp_score, temp_answers))

    for name, scores, answer in sorted(scores, key=itemgetter(1), reverse=True):
        cprint('{}: {} баллов. Ответы: {}'.format(name, scores, answer), color='green')

    cprint('-----------------------------', color='green')
    input('Введите любой символ, чтобы вернуться в меню ')
