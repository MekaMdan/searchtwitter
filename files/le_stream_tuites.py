#primeiro instalar o tweepy : $ sudo pip3 install tweepy
#funciona melhor no python3

#!/usr/bin/env python3
#!-*- coding: utf-8 -*-
# coding=utf-8
# coding: latin-1
from __future__ import unicode_literals

# módulo que dá acesso à API do twitter
import tweepy
# módulo que manipula data e tempo
import datetime
#módulo que trabalha com arquivos JSON
import json
# módulo de acesso a funções básicas do sistema operacional, como acesso a arquivos
import os
# módulo que permite a busca nomes de arquivos em diretórios, usando um padrão de nomes
import fnmatch
# módulo que trabalha com busca em strings por meio de expressões regulares
import re
import schedule
import time
import csv
import sys


# Incrementar esta lista
csv_path = 'data/data' + str(datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')) + '.csv'

# Um escutador de tuítes básico - armazena cada tuite recebido
class tuitesListener(tweepy.StreamListener):

    # método invocado automaticamente sempre que um novo tuíte que atende aos requistos de filtragem é produzido
    def on_data(self, data):
        # converte o string recebido para json
        tweet = json.loads(data)
        #if (tweet['user']["screen_name"] in usuarios_relevantes):
            # Sao essas as infos que voce realmente precisa
        print(tweet['created_at'])
        print(tweet['text'])
        print(tweet['user']["screen_name"])
        print(tweet['user']["location"])
        with open(csv_path, 'a') as file:
            format_string = tweet['created_at'] + "," + tweet['text'] + "," + tweet['user']["screen_name"] + "," + tweet['user']["location"] + "\n"
            file.write(format_string)
        #acrescenta o tuite recebido ao arquivo de tuítes corrente 

        return True

    def on_error(self, status):
        print ('Erro recebendo tuíte:')
        FILE = open('system/error_log.txt','a')
        FILE.write(str(datetime.datetime.now())+ ' Erro tuitesListener: '+ ' -> status ' + str(status) + "\n")
        FILE.close()
        return True

def carregaTags():
    # cada tag de interesse deve estar em uma linha separada neste arquivo
    FILE = open('data/tags.txt','r')
    tags = FILE.read()
    FILE.close()

    # cada um dos tags está em uma linha separada
    listaTags = tags.split('\n')

    return listaTags

def tweepyStream(api):
    while True:
        print("[re]Abrindo o leitor de tuites:")
        escutadorDeTuites = tuitesListener()
        stream = tweepy.Stream(api[1], escutadorDeTuites)

        tags = carregaTags()
        print("Tags de interesse: ")
        print(tags)

        try:
            print("Tenta abrir o leitor de tuites, manifestando interesse nos tags informados")
            stream.filter(track= tags, languages=['pt'])
            #print("Leitor de tuites iniciado:")
        except Exception as e:
            print ("Erro abrindo o leitor de tuites. Reiniciando.. registrando erro: ")
            FILE = open('system/error_log.txt','a')
            FILE.write(str(datetime.datetime.now())+ ' -> ' + str(e) + "\n")
            FILE.close()
    return True


# recupera as chaves que se encontram em um arquivo
def getAcessKeys():
    # este é o arquivo onde devem estar armazenadas as chaves
    FILE = open('system/keys.txt','r')
    keys0 = FILE.read()
    keys1 = []
    FILE.close()

    # cada uma dos conjuntos de chaves está em uma linha separada
    keys0 = keys0.split('\n')

    # os elementos da chave de acesso são separados por '@'
    for key in keys0:
        keys1.append(key.split('@'))

    last = len(keys1)-1

    del keys1[last]
    return keys1

def authenticate(CONSUMER_TOKEN, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET):
    # cria o objeto tratador da autenticação, usando as chaves passadas
    auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)

    # constrói o objeto de acesso à API
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True, retry_count=9080, retry_delay= 15)

    return [api,auth]

def main():
    apis = []
    keys_list = getAcessKeys()

    # testa o conjunto de chaves, de forma sequencial, para ver qual delas funciona primeiro
    for key in keys_list:
        apis.append(authenticate(key[0], key[1], key[2], key[3]))
    id = 0

    # testa o conjunto de chaves, de forma sequencial, para ver qual delas funciona primeiro
    for api in apis:
        print('Buscando acesso à API do Twitter')
        print(id)
        api.append(id)
        tweepyStream(api)
        id = id + 1
        print('Usando a chave de índice: '+id)
        # deu certo, então sai do loop
        break

    return True


if __name__ == '__main__':
    main()

schedule.every().day.at("23:50").do(main)

while 1:
    schedule.run_pending()
    time.sleep(1)
