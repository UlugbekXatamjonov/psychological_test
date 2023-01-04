from .models import Category, Test, Test_answer

# Create your tests here.
"""
1) shunchaki ballar qo'shiladi
2) E1 + E2 = shunchaki ballar qo'shiladi
3) E1-E2+35 
"""

""" test qilish uchun olingan request """
selected_answers = {
        "category": 4,
        "tests":[
            {"test_id": 1,
            "answer_id": 3},
            {"test_id": 2,
            "answer_id": 7},
            {"test_id": 3,
            "answer_id": 10},
            {"test_id": 4,
            "answer_id": 16},
            {"test_id": 5,
            "answer_id": 19}, 
            {"test_id": 6,
            "answer_id": 23},
            {"test_id": 7,
            "answer_id": 27},
            ]
        }

def tests_answer(selected_answers):
    """ Kelayotgan resuest dan belgilangan category va test hamda uning variantlarini yuklab olamiz """
    answer_category = selected_answers.get('category') # belgilangan category idsi
    answer_tests = selected_answers.get['tests'] # belgilangan test va javob idlari
    
    answer_tests_id = [] # belgilangan test idlari
    for test in answer_tests:
        answer_tests_id.append(test['test_id'])
        
    answer_answer_id = [] # belgilangan javoblar idlari
    for awr in answer_tests:
        answer_answer_id.append(awr['answer_id'])
        
    """ requstdan kelgan test va kategoriya idlari asosida o'zimizda bor test va category larni yig'ib olamiz """
    category = Category.objects.filter(id=answer_category) # belgilangan category obyekti
    
    total_tests = [] # belgilangan test obyekti(ro'yhat)
    for testid in answer_tests_id:
        total_tests.append(Test.objects.filter(id=testid))
    
    """ testlarni formulasi bo'yicha ajratib olamiz; E1 va E2 """    
    test_e1 = [] # belgilangan E1 test obyekti(ro'yhat)
    for testid in answer_tests_id:
        test_e1.append(Test.objects.filter(id=testid, form=1))
        
    test_e2 = [] # belgilangan E2 test obyekti(ro'yhat)
    for testid in answer_tests_id:
        test_e2.append(Test.objects.filter(id=testid, form=2)) 
    
    """ Javoblarni ham ajratib olamiz """
    answer = [] # belgilangan answer obyekti(ro'yhat)
    for answerid in answer_answer_id:
        answer.append(Test_answer.objects.filter(id=answerid))
    
    """ E1 turidagi teslarni idsi javoblardagi 'test_id' bilan birxil bo'la; yani javob E1 turidagi
        testga tegishli bo'lsa o'sha javobni  'ball'lini 'e1' degan o'zgaruvchiga yig'amiz.
        Va natijada hamma E1 turidagi testlarning javoblari ostidagi ballar yig'indisini topamiz. 
        Huddi shu ish E2 turidagi testlar ushun ham takrorlangan. """
    
    """ E1 turidagi tstlar uchun """
    e1 = 0
    for test in test_e1:
        for asw in answer:
            if asw.test_id == test.id:
                e1 += answer.ball
    """ E2 turidagi tstlar uchun """         
    e2 = 0
    for test in test_e2:
        for asw in answer:
            if asw.test_id == test.id:
                e2 += answer.ball
            
    """  ---------------------   Ballni hisoblash ---------------------- """
    total_ball = 0 # ummumiy ball
    if category.ball35 > 0 and category == answer_category:
        """ E1-E2+35 """
        total_ball = e1 - e2 + category.ball35
    elif category.ball35 == 0 and category == answer_category:
        total_ball = e1 + e2
    else:
        print("Ballni hisoblashda xatolik sodir bo'ldi!!!")

    return(total_ball)










