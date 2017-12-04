#Form filler
#It fills a given form made with Google Form with random names and surnames and fake emails or with names, surnames and emails
#of the people of Mathematics department ''Guido Castelnuovo'' (Sapienza University of Rome) taking the data from the people page of
#the department itself.

#Author: Matteo Gardini
#Institution: Sapienza University of Rome
#Date: 18/11/2017

#requested third-party libraries: requests, beautiful soup 4.

import requests
import bs4
import random
import time

class Persona():
    def __init__(self, nome, cognome, ruolo, mail):
        self.nome = nome
        self.cognome = cognome
        self.ruolo = ruolo
        self.mail = mail
    
    def __str__(self):
        return('nome: {}\ncognome: {}\nruolo: {}\nmail: {}\n\n'.format(self.nome, self.cognome, self.ruolo, self.mail))

#Parametri
send_flag = True
randomChoice = True
nomi_cognomi_da_lista = True

#
lista_nomi_check = False
lista_cognomi_check = False

number_people = 5
max_time_to_sleep = 2 #in secondi

#Dati del form
#Il form seguente e' scaduto percio' pubblicando il link non si arreca alcun danno.
form_link = 'https://docs.google.com/forms/d/e/1FAIpQLScVFJB4a3f-PsRCp78NlHIcpP1VR0vYr5ig7u5N0sR_ho3UcA/formResponse'

nome_form = 'entry.1161570529'
cognome_form = 'entry.346358819'
matricola_form = 'entry.885363435'
indirizzo_form = 'entry.1399104453'
ruolo_form = 'entry.2142530771'
ruolo_answers = ['Primo anno di corso, Laurea Triennale in Matematica','Secondo anno di corso, Laurea Triennale in Matematica','Terzo anno di corso o successivi, Laurea Triennale in Matematica','Laurea Magistrale in Matematica o Laurea Magistrale in Matematica per le Applicazioni','Dottorando / Assegnista','Docente / Personale Tecnico Amministrativo']
orario_form = 'entry.969781418'
orario_answers = ['Indifferente','Primo spettacolo (ore 15)','Secondo spettacolo (ore 17:30)']

#url per nomi e cognomi
url_nomi = 'https://gist.githubusercontent.com/pdesterlich/2562329/raw/7c09ac44d769539c61df15d5b3c441eaebb77660/nomi_italiani.txt'
url_cognomi = 'https://gist.githubusercontent.com/pdesterlich/2562407/raw/9fbc510830f1a65a7103742aeed30c0422590ec1/cognomi.txt'

#url dipartimento
url_dip = 'https://www.mat.uniroma1.it/dipartimento/persone'

random.seed()

if randomChoice:
    #creazione delle liste di nomi e cognomi
    if nomi_cognomi_da_lista:
        try:
            with open('nomi.txt','r') as fobj:
                lista_nomi = fobj.read().split('\n')
            lista_nomi_check = True
            print('[+] lista nomi creata da file.')
        except FileNotFoundError:
            lista_nomi_check = False
            print('[-] file con lista nomi non trovato.')
        
        try:
            with open('cognomi.txt','r') as fobj:
                lista_cognomi = fobj.read().split('\n')
            lista_cognomi_check = True
            print('[+] lista cognomi creata da file.')
        except FileNotFoundError:
            lista_cognomi_check = False
            print('[-] file con lista cognomi non trovato.')
            
    if not(lista_nomi_check):
        res = requests.get(url_nomi)
        if res.status_code == 200:
            lista_nomi = res.text.split('\n')[7:]
            lista_nomi_check = True
            print('[+] lista nomi scaricata dalla pagina web: {}.'.format(url_nomi))
        else:
            lista_nomi_check = False
            print(u'[-] la pagina web {} non è raggiungibile.'.format(url_nomi))

    if not(lista_cognomi_check):
        res = requests.get(url_cognomi)
        if res.status_code == 200:
            lista_cognomi = res.text.split('\n')[7:]
            lista_cognomi_check = True
            print('[+] lista nomi scaricata dalla pagina web: {}.'.format(url_cognomi))
        else:
            lista_cognomi_check = False
            print(u'[-] la pagina web {} non è raggiungibile.'.format(url_nomi))
        
    if lista_nomi_check and lista_cognomi_check:
        print('\n- Dati inseriti -\n')
        for n in range(number_people):
            nome = random.choice(lista_nomi)
            nome = nome.lower()
            cognome = random.choice(lista_cognomi)
            cognome = cognome.lower()
            random_ruolo_int = random.randint(0,5)
            ruolo = ruolo_answers[random_ruolo_int]
            if random_ruolo_int in [4,5]:
                matricola = '000000'
                if random.randint(0,1):
                    indirizzo = '{}.{}@uniroma1.it'.format(nome.replace(' ',''), cognome.replace(' ',''))
                else:
                    indirizzo = '{}@mat.uniroma1.it'.format(cognome.replace(' ',''))
            else:
                matricola = str(random.randint(193451,9863122))
                indirizzo = '{}.{}@studenti.uniroma1.it'.format(cognome.replace(' ',''), matricola)
            orario = random.choice(orario_answers)
            print('Nome: {}\nCognome: {}\nMatricola: {}\nIndirizzo: {}\nRuolo: {}\nOrario: {}\n'.format(nome.capitalize(), cognome.capitalize(), matricola, indirizzo, ruolo, orario))
            if send_flag:
                r = requests.post(form_link, data={nome_form: nome.capitalize(), cognome_form: cognome.capitalize(), matricola_form: matricola, indirizzo_form: indirizzo, ruolo_form: ruolo, orario_form: orario})
            if n != number_people-1:
                time.sleep(random.randint(0,max_time_to_sleep))
else:
    personale = []
            
    res = requests.get(url_dip)
    soup = bs4.BeautifulSoup(res.text,'html.parser')
    result = soup.select('tr')
    for element in result[:20]:
        try:
            persona, ruolo = element.find('a')['title'].split(' - ')
            persona = persona.strip()
            ruolo = ruolo.strip()
            nome_cognome = persona.split()
            if len(nome_cognome) > 2:
                print(persona)
                nome = input('nome: ')
                cognome = persona[len(nome)+1:]
            else:
                nome = nome_cognome[0]
                cognome = nome_cognome[1]
            
            mail = element.find('img')['alt'].replace('#AT#','@')
            
            personale.append(Persona(nome, cognome, ruolo, mail))
        
        except KeyError:
            pass
        except TypeError:
            pass

    for individuo in personale:
        if 'dottorand' in individuo.ruolo.lower():
            ruolo = ruolo_answers[4]
        elif 'assegnista' in individuo.ruolo.lower():
            ruolo = ruolo_answers[4]
        elif 'ricercat' in individuo.ruolo.lower():
            ruolo = ruolo_answers[5]
        elif 'professor' in individuo.ruolo.lower():
            ruolo = ruolo_answers[5]
        else:
            ruolo = ruolo_answers[5]
        matricola = '000000'
        orario = random.choice(orario_answers)
        print('Nome: {}\nCognome: {}\nMatricola: {}\nIndirizzo: {}\nRuolo: {}\nOrario: {}\n'.format(individuo.nome.capitalize(), individuo.cognome.capitalize(), matricola, individuo.mail, ruolo, orario))
        if send_flag:
            r = requests.post(form_link, data={nome_form: nome.capitalize(), cognome_form: cognome.capitalize(), matricola_form: matricola, indirizzo_form: indirizzo, ruolo_form: ruolo, orario_form: orario})
        time.sleep(random.randint(0,max_time_to_sleep))