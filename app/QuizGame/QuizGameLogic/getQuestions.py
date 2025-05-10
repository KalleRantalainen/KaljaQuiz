def example_get_questions(num):
    if num == 0:
        kysymys = {
            "text": "Kuinka monta kaljaa Kalle juo ennen sammumista.",
            "choices": [1, 4, 9, 1000],
            "answer": 4
        }
        return kysymys
    
    return {
            "text": "BLANK",
            "choices": [0],
            "answer": -1
        }