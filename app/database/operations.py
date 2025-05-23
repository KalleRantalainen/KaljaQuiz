from ..extensions import db
# from .models import User

# TODO: GIORGIO
# Tänne pittäs määrittää operaatioita tietokannalle.
# Paras varmaan määrittää luokan metodeina, niin ei tarvi importtailla hirveetä listaa metodeita.
# Esim:

# class DbAPI():
#     def create_user(self, name):
#         user = User(name=name) # Taulu pitää muistaa importtaa models.py tiedostosta
#         db.session.add(user)
#         db.session.commit()
#         return user
    
#     def get_user(self, user_id):
#         return User.query.get(user_id)


# Tarvittavat metodit:

# get_question(self):
#  - Return: Pitäs palauttaa käyttämätön kysymys string ja vastaus string sille, esim tuple (question, answer)

# import_questions(self, path_to_json_file):
#  - path_to_json_file: string polku json tiedostoon.
#  - pitäs lisätä json tiedostosta kysymykset tauluun.
#  - tän hetkiset json tiedostot löytyy \app\QuizGame\QuizGameLogic\data\
#    ei tarvi huomioida mitään eri kieliversioita, mokkukalle tykitti niitä sinne
#    joskus keskellä yötä.


# Esimerkki käytöstä muissa moduuleissa:
# from app.db.operations import DbAPI

# user = DbAPI.create_user("Alice")
# retrieved = DbAPI.get_user(user.id)
# print(user, retrieved)
