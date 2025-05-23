from ..extensions import db

# TODO: GIORGIO
# Tänne voi määritellä tietokannan tauluja esimerkiksi jotenkin näin:

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))

# Alkuun ei tarvita ehkä muuta kuin joku Questions taulu, johon täytyy saada
#  id       : integer, primary
#  question : string, sisältää kymys tekstin
#  answer   : string, vastaus kysymykseen
#  used     : bool, onko kysmys käytetty vai ei
#  category : string, kysymyksen kategoria (en tiedä tarvitaanko edes)

# Jossain kohtaa voidaan määritellä Users taulukin, mutta toistaseks varmaan
# aiheuttas enemmän mankelia kun hyötyä.