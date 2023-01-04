from pprint import pprint
"""
  {"test_id": 4,
            "answer_id": 16},
            {"test_id": 5,
            "answer_id": 19}, 
            {"test_id": 6,
            "answer_id": 23},
            {"test_id": 7,
            "answer_id": 27},
"""
answer = \
[
    {
        "category": 4,
        "tests":[
            {   "test_id": 1,
                "answer_id": 3
            },
            {
                "test_id": 2,
                "answer_id": 7
            },
            {
                "test_id": 3,
                "answer_id": 10
            },
            {   "test_id": 4,
                "answer_id": 16
            },
            {
                "test_id": 5,
                "answer_id": 19
            }, 
            {
                "test_id": 6,
                "answer_id": 23
            },
            {
                "test_id": 7,
                "answer_id": 27
            },
        ]
    },
]

# print(answer[0]["tests"][0]["test_id"])
# print(answer[0]["tests"][0]["answer_id"])

def tests_answer(answer):
    answer_category = answer[0]['category']
    answer_tests = answer[0]['tests']
    # for test in answer_tests:
    #     print(f"test_id - {test['test_id']} / answer_id - {test['answer_id']}")
        
    

tests_answer(answer)







