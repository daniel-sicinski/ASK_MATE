from server_python.config import app
from data_manager import dm_general, dm_questions, dm_answers, dm_comments, dm_tags
from flask import request, redirect, render_template


@app.route('/')
def route_home():
    questions = dm_questions.get_5_questions_sql_sorted_by_submission_time()
    return render_template('index.html', questions=questions)


@app.route('/list')
def route_list():
    questions = dm_questions.get_all_questions_sql_sorted_by_submission_time()
    return render_template('list.html', questions=questions)


@app.route('/sort')
def route_sort_questions():
    feature_to_order_by = request.args.get('order_by', default='title', type=str)
    # todo > everywhere we receive user input - evein in URL - make checks if parameters exist
    # if feature_to_order_by not in ['title', 'message']:
    #     return 'Error: wrong parameter'
    order_direction = request.args.get('order_direction', default='asc', type=str)
    questions = dm_questions.get_questions_sorted(feature_to_order_by, order_direction)
    return render_template('list.html', questions=questions)


@app.route('/add', methods=['GET', 'POST'])
def route_add_question():
    action = '/add'
    if request.method == 'POST':
        dm_questions.add_question_sql(request.form)
        return redirect('/list')
    return render_template('form.html', action=action)


@app.route('/question/<question_id>/delete')
def route_delete_question(question_id):
    dm_questions.delete_question(question_id)
    return redirect('/list')


@app.route('/question_detail/<id>', methods=['GET', 'POST'])
def route_question_detail(id):
    # check if this try / except is necessary
    try:
        if request.method == 'GET':
            dm_questions.update_question_view_increase_count(id)
        question = dm_questions.get_question_sql_by_id(id)[0]
        answers = dm_answers.get_all_sql_answers_by_question_id(id)
        comments = dm_comments.show_question_comments_by_id(id)
        answer_comments = dm_comments.show_answer_comments_by_id(id)
        print('these are answer comments ', answers)
        print('neverwimsd')
        tags = dm_tags.get_tags_of_question_by_id(id)
        return render_template('qd.html', question=question, id=id, answers=answers, count=len(answers), comments=comments, answer_comments=answer_comments, tags=tags)
    except ValueError:
        return redirect('/')


@app.route('/question_detail/<id>/edit', methods=['POST', 'GET'])
def route_question_edit(id):
    action = '/question_detail/' + id + '/edit'
    question = dm_questions.get_question_sql_by_id(id)
    now = '1'
    if request.method == 'POST':
        dm_questions.update_question_sql(id, request.form)
        print(request.form)
        return redirect('/question_detail/' + id)
    return render_template('form.html', question=question, action=action, now=now)


@app.route('/question/<question_id>/vote-down')
def question_vote_down(question_id):
    dm_general.change_vote("question", question_id, -1)
    return redirect('/question_detail/' + question_id)


@app.route('/question/<question_id>/vote-up')
def question_vote_up(question_id):
    dm_general.change_vote("question", question_id, 1)
    return redirect('/question_detail/' + question_id)


