import json
import random
import os


"""
    Käyttö: 
    question_api_fi = QuestionAPI("fi")
    random_question1 = question_api_fi.get_rand_question() # Palauttaa randomin kysmyksen randomiin kategoriaan
    answer_question1 = get_answer_by_question(random_question1) # Palauttaa oikean vastauksen kysymykseen

    TAI 

    random_question2 = question_api_fi.get_rand_question_by_category("HISTORY") # Palauttaa randomin kysmyksen HISTORY kategoriaan
    answer_question2 = get_answer_by_question(answer_question2) # Palauttaa oikean vastauksen kysymykseen
"""
class QuestionAPI():
    def __init__(self, lang="fi"):
        # Kategoridoiden nimet / tiedostojen nimet, jossa kysymykset ovat
        self.categories = ["HISTORY", "SCIENCE", "MISCELLANEOUS", "CHATGPTRAPPA", "EXPLAIN"]
        # Pitää kirjaa käytetyistä kysymyksistä, ettei samaa kysymystä kysytä monesti
        self.used_question_ids = [] # Formaatti [{"category": "HISTORY", "used_ids": [1,3]}, {"category": "SCIENCE", "used_ids": []}, ...]
        # Kieli, jolla kysymys ja vastaus haetaan
        self.lang = lang
        # Initialisoidaan used_question_ids lista
        self._init_used_questions()

    # Private methods:
    def _read_json(self, category):
        # Lukee json tiedoston
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, "data")
        filename = os.path.join(path, f"{category}.json")
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}
        return data
    
    def _mark_question_used(self, category, question_id):
        # Asettaa kysymyksen käytetyksi
        for entry in self.used_question_ids:
            if entry["category"] == category:
                entry["used_ids"].append(question_id)
    
    def _init_used_questions(self):
        # Alustaa käyettyjen kysymysten listan
        for categ in self.categories:
            info = {
                "category": categ,
                "used_ids": []
            }
            self.used_question_ids.append(info)

    def _get_available_question_id(self, quest_count, category):
        # Hakee randomin käyttämättömän kysymyksen idn määritellystä kategoriasta
        used_ids = []
        for used in self.used_question_ids:
            if used["category"] == category:
                used_ids = used["used_ids"]
                break
    
        if len(used_ids) == quest_count:
            # Kaikki kysymykset kategoriasta käytetty. -> Pitää olla enemmän kysymyksiä,
            # kuin kierroksia pelissä niin ei tule tätä ongelmaa.
            return None
        
        # Kaikkien kysymysten idt
        all_quest_ids = list(range(0, quest_count))
        # Otetaan vain käyttämättömät kysymykset
        unused_ids = list(set(used_ids) ^ set(all_quest_ids))
        # Palautetaan random id
        return random.choice(unused_ids)


    
    # Public methods:
    def get_rand_question_by_category(self, category):
        # Palauttaa random kysymyksen määritellystä kategoriasta
        json_object = self._read_json(category)
        if json_object:
            questions = json_object["questions"]
            question_count = len(questions)
            rand_question_id = self._get_available_question_id(question_count, category)
            self._mark_question_used(category, rand_question_id)
            if self.lang == "fi":
                return questions[rand_question_id]["question_fi"]
            else:
                return questions[rand_question_id]["question_en"]
            
        else:
            return "READING FILE FAILED!! get_rand_question_by_category"

    def get_rand_question(self):
        # Palauttaa random kysymyksen mistä tahansa kategoriasta
        random_categ = random.choice(self.categories)
        rand_quest = self.get_rand_question_by_category(random_categ)
        return rand_quest

    def get_answer_by_id(self, question_id, category):
        # Palauttaa oikean vastauksen kysymykseen kysymyksen id:n ja kategorian perusteella
        json_object = self._read_json(category)
        if json_object:
            questions = json_object["questions"]
            if self.lang == "fi":
                return questions[question_id]["answer_fi"]
            else:
                return questions[question_id]["answer_en"]
        else:
            return "READING FILE FAILED!! get_answer_by_id"

    def get_answer_by_question(self, question):
        # Palauttaa oikean vastauksen kysymykseen kysymyksen (stringin) perusteella
        # mistä tahansa kategoriasta
        for categ in self.categories:
            json_object = self._read_json(categ)
            questions = json_object["questions"]
            for quest_data in questions:
                if self.lang == "fi":
                    if quest_data["question_fi"] == question:
                        return quest_data["answer_fi"]
                else:
                    if quest_data["question_en"] == question:
                        return quest_data["answer_en"]
                    
        return f"NO ANSWER FOUND FOR QUESTION: {question}"
    
    def get_all_question_data(self):
        # Vois tehdä ehkä funktion joka hakee kaikki yhteen kysymykseen liittyvät tiedot
        # ja palauttaa sen jsonina? Ei tarvis hakea kysymystä ja vastausta erikseen jos
        # ei tahdo.
        return NotImplementedError



# Testausta varten kaikki alla oleva. Voi kommentoida pois jos aiheuttaa ongelmia
if __name__ == "__main__":
    question_api_fi = QuestionAPI("fi")
    question_api_en = QuestionAPI("en")

    random_question_history_fi = question_api_fi.get_rand_question_by_category("HISTORY")
    random_question_history_en = question_api_en.get_rand_question_by_category("HISTORY")
    print()
    print("=== get_rand_question_by_category ===")
    print(" - random history quest fi:")
    print(f"   - {random_question_history_fi}")
    print()
    print(" - random history quest en:")
    print(f"   - {random_question_history_en}")
    print()


    answer_history_fi = question_api_fi.get_answer_by_question(random_question_history_fi)
    answer_history_en = question_api_en.get_answer_by_question(random_question_history_en)
    print()
    print("=== get_answer_by_question ===")
    print(" - answer_history_fi:")
    print(f"   - {answer_history_fi}")
    print()
    print(" - answer_history_en:")
    print(f"   - {answer_history_en}")
    print()

    random_question_fi = question_api_fi.get_rand_question()
    random_question_en = question_api_en.get_rand_question()
    print()
    print("=== get_rand_question ===")
    print(" - random_question_fi:")
    print(f"   - {random_question_fi}")
    print()
    print(" - random_question_en:")
    print(f"   - {random_question_en}")
    print()

    answer_fi = question_api_fi.get_answer_by_question(random_question_fi)
    answer_en = question_api_en.get_answer_by_question(random_question_en)
    print()
    print("=== get_answer_by_question ===")
    print(" - answer_fi:")
    print(f"   - {answer_fi}")
    print()
    print(" - answer_en:")
    print(f"   - {answer_en}")
    print()


    fixed_id = 3
    answer_history_3_fi = question_api_fi.get_answer_by_id(fixed_id, "HISTORY")
    answer_history_3_en = question_api_en.get_answer_by_id(fixed_id, "HISTORY")
    print()
    print("=== get_answer_by_id ===")
    print(" - answer_history_3_fi:")
    print(f"   - {answer_history_3_fi}")
    print()
    print(" - answer_history_3_en:")
    print(f"   - {answer_history_3_en}")
    print()



