# Käynnistys

## Torstaiks pitäs saada nämä valmiiks jos kerkijjää
* Listanäkymissä on tupla borderit koska laitoin sitten kaks tyyliä päällekkäin
* Jotkut listanäkymien boxit on liian leveitä, esim pelaajien nimet hostin odotusnäytöllä
* Tuloksien table on aika raffi, pittäs tehdä tyylit siihen
* Pylväsdiagrammi siisteillä particle effecteillä
* Retroteema on perseennäkönen
* 80s neon on vielä perseemmännäkönen, mutta käyttää siistä 3d kirjastoa joten siitä ei luovuta

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
tai liittää pelaaja aina uudestaan huoneseen. broadcast=True lähettää eventin kaikkialle, eli jos joku javascript kuuntelee sitä, niin se vastaanottaa sen vaikka ei olis roomissa.

Client ei pysty kai lähettämään eventtiä toiselle suoraan javascriptillä. Eli jos javascriptistä emittoidaan vaikka "player_ready" eventti, niin täytyy luoda python socket, joka ottaa vastaan tämän eventin ja emittoi sen uudestaan. Tälläin se tulee serveriltä ja kaikki muut clientit/pelaajat pystyy ottamaan sen vastaan. <- tää on ehkä semi hypoteettista mutta näytti toimivan.

## Quizgame idea rappakalja versio (sen jälkeen kun start game näppäintä on painettu)
- Hostin näytölle tulee kysymys ja senkuntikello, esim 30 sek aikaa (tämä vaikka emit next_question kautta)
- Pelaajien näytölle tulee vastauslaatikko ja submit button (submitista lähtee joku event, jonka host rekisteröi ja vastaukset tallennetaan esim game_state_storen johonkin dictiin joka täytyy tehdä)
- Kun kaikki pelaajat on vastannut tai aika loppuu -> siirrytään äänestykseen (tästä lähtee varmaan taas joku event)
- Äänestyksen aikana hostin ruudulla voi näkyä kaikkien vastaukset (ilman nimiä) ja oikea vastaus esim jossain a,b,c,.. listassa
- Pelaajien ruudulla näkyy kaikkien vastaukset + oikea vastaus kysymykseen ja jokainen pelaaja valitsee sen joka on heidän mielestään oikein
- Jos valitsee oikean vastauksen pelaaja saa yhden pisteen
- Jos valitsee jonkun toisen pelaajan vastauksen, se pelaaja jonka vastaus valittiin, saa pisteen
- Äänestyksen jälkeen voidaan näyttää vaikka pylväsdiagrammilla tai jotenkin siististi pistetilanne
- Tämän jälkeen emittoidaan taas next_question ja sama rumba jatkuu niin kauan kunnes joku question limiitti tulee täyteen.
- Kysymysten tallennus voidaan tehdä vaikka jsonilla tai xml llä tai tietokannalla, esim postegres.
- Jos tehdään kysymyksen tallennetaan tiedostoon niin, ne vois varmaan tallentaa johonkin QuizGameLogic/data kansiion ja tehdä jonkun funktion joka hakee sieltä joko randomisti tai jonkun kategoridan perusteella kysymyksen ja oikean vastauksen. Tällöin pelin seuranta kannattaa varmaan toteuttaa myös game_state_store.py tiedoston luokalla.
- Jos käytetään tietokantaa, niin kannattaa varmaan luoda uusi container jossa tietokanta asustaa ja vääntää siihen joku rajapinta. Jos tehdään tietokanta niin pelin seurannan vois varmaan kanssa siirtää sinne.
