# Käynnistys

## Dockerilla
1. Docker engine päälle
2. Aja `start.ps1` kansiossa ./kaljaQuiz
3. Pelin hostin osoite on http://127.0.0.1:8080/host
4. Puhelimella liittyvien pelaajien osoite printataan konsoliin muodossa: User URL: http://xx.xx.xx.xx:8080/user

## Ilman dockeria
1. Aja `python run.py` kansiossa ./kaljaQuiz
2. Osoitteet muuttuu, muuta ne näkee konsolista

## Sockets
Jos route/url vaihtuu, niin kaikki socketin roomiin liitetyt taistelijat katoavat.
Siis jos esim ollaan /waiting-room osotteessa ja pelaaja on liitetty room="room1" huoneeseen ja sitten siirrytään osotteeseen /quizgame niin pelaaja tippuu roomista ja
eventit eivät tule perille. Käytännössä sokettia pitää siis käyttää samassa näkymässä
tai liittää pelaaja aina uudestaan huoneseen.

Client ei pysty kai lähettämään eventtiä toiselle suoraan javascriptillä. Eli jos javascriptistä emittoidaan vaikka "player_ready" eventti, niin täytyy luoda python socket, joka ottaa vastaan tämän eventin ja emittoi sen uudestaan. Tälläin se tulee serveriltä ja kaikki muut clientit/pelaajat pystyy ottamaan sen vastaan. <- tää on ehkä semi hypoteettista mutta näytti toimivan.