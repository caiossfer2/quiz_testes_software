import pytest
from model import Question, Choice


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct




def test_add_multiple_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')

    assert len(question.choices) == 3
    assert [choice.text for choice in question.choices] == ['a', 'b', 'c']

def test_remove_choice_by_id():
    question = Question(title='q1')
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')

    question.remove_choice_by_id(choice1.id)

    assert len(question.choices) == 1
    assert question.choices[0].id == choice2.id

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')

    question.remove_all_choices()

    assert len(question.choices) == 0

def test_choice_ids_are_sequential():
    question = Question(title='q1')
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    choice3 = question.add_choice('c')

    assert choice1.id == 1
    assert choice2.id == 2
    assert choice3.id == 3

def test_set_correct_choices():
    question = Question(title='q1')
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    choice3 = question.add_choice('c')

    question.set_correct_choices([choice1.id, choice3.id])

    assert choice1.is_correct
    assert not choice2.is_correct
    assert choice3.is_correct

def test_select_choices_returns_correct_selections():
    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('a', True)
    choice2 = question.add_choice('b', False)
    question.add_choice('c', True)

    selected = question.select_choices([choice1.id, choice2.id])

    assert selected == [choice1.id]

def test_max_selections_constraint():
    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    choice3 = question.add_choice('c')

    with pytest.raises(Exception) as excinfo:
        question.select_choices([choice1.id, choice2.id, choice3.id])

    assert "Cannot select more than 2 choices" in str(excinfo.value)

def test_invalid_choice_id_raises_exception():
    question = Question(title='q1')
    question.add_choice('a')

    with pytest.raises(Exception) as excinfo:
        question.remove_choice_by_id(999)

    assert "Invalid choice id 999" in str(excinfo.value)

def test_choice_text_constraints():
    question = Question(title='q1')

    with pytest.raises(Exception):
        question.add_choice('')

    with pytest.raises(Exception):
        question.add_choice('a' * 101)

def test_question_points_constraints():
    with pytest.raises(Exception):
        Question(title='q1', points=0)

    with pytest.raises(Exception):
        Question(title='q1', points=101)

    # Valid boundaries should work
    question1 = Question(title='q1', points=1)
    question2 = Question(title='q1', points=100)
    assert question1.points == 1
    assert question2.points == 100


@pytest.fixture
def questions():
    question = Question(title='q1', max_selections=2)
    question.add_choice('a', True)
    question.add_choice('b', False)
    question.add_choice('c', False)
    question.add_choice('d', True)
    question.add_choice('e', False)
    return question

def test_correct_choices_identification(questions):
    correct_ids = questions._correct_choice_ids()

    assert len(correct_ids) == 2
    assert questions.choices[0].id in correct_ids 
    assert questions.choices[3].id in correct_ids  

    assert questions.choices[1].id not in correct_ids  
    assert questions.choices[2].id not in correct_ids  
    assert questions.choices[4].id not in correct_ids  

def test_select_choices_with_max_selections(questions):
    choice_ids = [choice.id for choice in questions.choices]

    selected = questions.select_choices(choice_ids[:2])

    assert len(selected) == 1
    assert selected[0] == questions.choices[0].id  

def test_changing_correct_choices(questions):
    original_correct_ids = questions._correct_choice_ids()

    new_correct_ids = [questions.choices[1].id, questions.choices[4].id]  

    for choice in questions.choices:
        choice.is_correct = False

    questions.set_correct_choices(new_correct_ids)

    updated_correct_ids = questions._correct_choice_ids()
    assert len(updated_correct_ids) == 2
    assert questions.choices[1].id in updated_correct_ids  
    assert questions.choices[4].id in updated_correct_ids 
    assert questions.choices[0].id not in updated_correct_ids  
    assert questions.choices[3].id not in updated_correct_ids  

    assert set(original_correct_ids) != set(updated_correct_ids)