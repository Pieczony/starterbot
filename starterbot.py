# -*- coding: utf-8 -*-

import os
import time
from slackclient import SlackClient

import logging
from datetime import datetime
from datetime import date
import sys
import schedule


LOGFILE = os.path.join('..', 'starterbot.log')

TOKEN = 'xoxb-74982025765-LOiHfNzh4RkcxsFLzi06LMrq'
TALK_CHANNEL_ID = '_talk'
DUTY_CHANNEL_ID = '_talk'

# odzywki slacka
KTO_DYZURNY_KANAL = 'Czółko! W tym tygodniu dyżur przypada gołębiom: '
KTO_DYZURNY = 'Siemanko! W tym tygodniu jesteś dyżurnym w cudownym duecie '
PRZYPOMINAJKA = 'Gołąbeczku! Pamiętasz o swoim dyżurze? Żeby nie zapomnieć wstań i rezejrzyj się wokół siebie'
PRZYP_ZMYWARKA = 'Zmywareczko powiedz przecie, kto jest najpełniejszy na świecie? Może czas powyciągać naczynia?'
PRZYP_MYDLO = 'Mydło lubię zabawę! zobacz czy nie skończyło się w łazienkach i w kuchni'
PRZYP_PAPIER = 'Znasz to, że życie jest jak papier toaletowy? Przypomnij mi, żeby Ci opowiedzieć. a tymczasem uzupełnij papier w łazienkach...'
PRZYP_SMIECI = 'Śmieci planują ucieczkę balkonem. Pomóż im bezpiecznie dostać się do śmietników! W szufladzie obok zlewu czekają worki. Uwolnij (w)orki!'
PRZYP_GARY = 'Gołąby! W kuchni piętrzą się brudne gary i nie można nic ugotować! Nie będę wymieniał z nazwiska, ale kto zeżarł swój obiad i zostawił brudne garnki - marsz do kuchni!' 

def connect(token):
    sc = SlackClient(token)
    if not sc.rtm_connect():
        return None
    else:
        return sc

def get_message(sc):
    overheard = sc.rtm_read()
    if len(overheard) > 0:
        return (overheard[0])
    else:
        return {}
        
def wypisz_dyzurnych(sc):
	#napisz na kanale kto jest dyzurnym
	ludzie=generuj()
	wiadomosc = KTO_DYZURNY_KANAL + "<@%s>, <@%s>" %(ludzie[0],ludzie[1])
	sc.rtm_send_message("codzienne", wiadomosc)
	#wyslij wiadomosc do kazdego czlowieka
	wiadomosc = KTO_DYZURNY + "<@%s>, <@%s>" %(ludzie[0],ludzie[1])
	for czlowiek in ludzie:
		id = sc.server.users.find(czlowiek).id
		sc.api_call("chat.postMessage", as_user="true:", channel=id, text=wiadomosc)
		#sc.rtm_send_message(id, wiadomosc)
	
	     	     
def przypomnij(sc):
	wiadomosc = PRZYPOMINAJKA
	ludzie=generuj()
	#wyslij wiadomosc z przypomnieniem
	for czlowiek in ludzie:
		id = sc.server.users.find(czlowiek).id
		sc.api_call("chat.postMessage", as_user="true:", channel=id, text=wiadomosc)
		#sc.rtm_send_message(id, wiadomosc)
		
def generuj():
	dyzurni = ["don_czipon","kluklu","mevah","dudu","ewacialowicz","robert","javvie","kth","e.skowron","weedoo","kocia_ciocia","waski","marti","magdalena","magda_pamela","d.sokol","piotrek","nalesnik","alicja"]
	tydzien=date.today().isocalendar()[1]
	dyzurny1=(tydzien*2-1)%len(dyzurni)
	dyzurny2=(tydzien*2-2)%len(dyzurni)
	lista = [dyzurni[dyzurny1], dyzurni[dyzurny2]]
	return lista
	
def zmywarka(sc):
	wiadomosc = PRZYP_ZMYWARKA
	ludzie=generuj()
	#wyslij wiadomosc z przypomnieniem
	for czlowiek in ludzie:
		id = sc.server.users.find(czlowiek).id
		sc.api_call("chat.postMessage", as_user="true:", channel=id, text=wiadomosc)
		#sc.rtm_send_message(id, wiadomosc)
		
def mydlo(sc):
	wiadomosc = PRZYP_MYDLO
	ludzie=generuj()
	#wyslij wiadomosc z przypomnieniem
	for czlowiek in ludzie:
		id = sc.server.users.find(czlowiek).id
		sc.api_call("chat.postMessage", as_user="true:", channel=id, text=wiadomosc)
		#sc.rtm_send_message(id, wiadomosc)
	
def papier(sc):
	wiadomosc = PRZYP_PAPIER
	ludzie=generuj()
	#wyslij wiadomosc z przypomnieniem
	for czlowiek in ludzie:
		id = sc.server.users.find(czlowiek).id
		sc.api_call("chat.postMessage", as_user="true:", channel=id, text=wiadomosc)
		#sc.rtm_send_message(id, wiadomosc)	
		
def smieci(sc):
	wiadomosc = PRZYP_SMIECI
	ludzie=generuj()
	#wyslij wiadomosc z przypomnieniem
	for czlowiek in ludzie:
		id = sc.server.users.find(czlowiek).id
		sc.api_call("chat.postMessage", as_user="true:", channel=id, text=wiadomosc)
		#sc.rtm_send_message(id, wiadomosc)  
		
def gary(sc):
	wiadomosc = PRZYP_GARY
	#wyslij wiadomosc z przypomnieniem
	sc.rtm_send_message("codzienne", wiadomosc)

# komendy slacka
commands_dict = {
	'!dyzurni': wypisz_dyzurnych,
	'!przypomnij': przypomnij,
	'!zmywarka': zmywarka,
	'!mydlo': mydlo,
	'!papier': papier,
	'!smieci': smieci,
	'!gary': gary,
	}
        

if __name__ == '__main__':
    print("Uruchamiam e-woźną")

    sc = connect(TOKEN)
    if sc is None:
        sys.exit(0)
        
    schedule.every().monday.at("10:30").do(wypisz_dyzurnych, sc)
             
    while True:
        
        overheard = get_message(sc)

        if 'text' in overheard and overheard['text'] in commands_dict:
            message = overheard['text']
            commands_dict[message](sc)
            
        schedule.run_pending()
        time.sleep(1)
            
    