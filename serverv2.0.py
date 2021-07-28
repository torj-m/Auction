
#!/usr/bin/env python3

"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM,SOCK_DGRAM
from threading import Thread
from threading import Timer
from datetime import datetime
import select,time,threading
import os

vendeur =""
vente = False
test = False
nom_prod= "test"
acheteur =""
duree_vente= datetime.now()
prix = 0
global prixinit
joins =[]
done = False
factures={}

def facture_acheteur( nom_acheteur):
    """rechercher le nom de l'acheteur dans  factures.txt et afficher la ligne(s) correspondante(s)"""
    nombre_de_ligne = 0
    lignes = []
    # Open the file in read only mode
    with open("factures.txt", 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            nombre_de_ligne += 1
            if nom_acheteur in line:
                # If yes, then add the line number & line as a tuple in the list
                lignes.append((line.rstrip()))
    # Return list  lines where string is found
    print(*lignes, sep = "\n")
#processus time 
class TestThreading(object):
    global duree_vente
    global acheteur
    global vente
    global joins
    global prix
    global prixinit
    def __init__(self, interval=1):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        global duree_vente
        global acheteur
        global vente
        global done
        global joins
        global vendeur
        while True:
            # More statements comes here

            if ((datetime.now()-duree_vente).seconds==20 and not done):
                diffuserj(bytes("La vente aux enchères se termine dans 10 seconds" , "utf8"))
                done = True
            if ((datetime.now()-duree_vente).seconds>30): #vente ended
                bien = open("bien.txt","a")
                if (acheteur!=""): #acheteur exist
                    diffuserj(bytes("La vente aux enchères s'est terminé ,%s est le dernier acheteur" % acheteur, "utf8"))
                    vente = False
                    print("La vente aux enchères s'est terminé ,%s est le dernier acheteur" % acheteur)
                    bien.write(ligne_bien(nom_prod,prixinit,prix,"Vendu",acheteur+"\n"))
                    bien.close()
                    histo = open("histo.txt","a")
                    histo.write(ligne_historique(acheteur,prix,"succes\n"))
                    histo.close()
                    #ajouter a factures
                    if (acheteur not in list(factures.keys())):
                       fact = open("factures.txt","a")
                       fact.write(ligne_fact(acheteur,prix)+"\n")
                       fact.close()
                       factures[acheteur]=prix
                    else : #acheteur exist deja dans factures
                        factures[acheteur]=factures[acheteur]+prix
                        remplir()
                        
                    
                    vendeur = ""
                    joins=[]
                    acheteur=""
                    break
                
                else :  #no acheteur . produit disponible
                    if vente:
                        diffuserj(bytes("La vente aux enchères s'est terminé sans acheteurs", "utf8"))
                        print("La vente aux enchères s'est terminé sans acheteurs")
                        bien.write(ligne_bien(nom_prod,prixinit,prixinit,"Disponible","--\n"))
                        bien.close()
                        vente = False;
                        vendeur =""
                        joins=[]
                        break
                    
                    
                vente = False;
                joins=[]
                vendeur =""
                break
                
            time.sleep(self.interval)



#proccessus menu
class menu(object):
    global duree_vente
    global acheteur
    global vente
    global nom_prod
    global prix
    global prixinit
    global done
    def __init__(self, interval=1):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        global duree_vente
        global acheteur
        global vente
        global done
        global prix
        global prixinit
        global nom_prod
        while True:
            if not vente :
                print("1- Lancer une vente aux enchères");
                print("2-Consulter la liste des biens ")
                print("3-Consulter la facture d'un acheteur en précisant son nom")
                print("4-Consulter l'historique de toutes les propositions ")
                print("5- exit")
                reponse = input()
                if (reponse =="1"):
                    nom_prod = input("tapez la nom_prod du produit =")
                    prix = int(input("prix de départ du produit = "))
                    prixinit= prix
                    vente = True
                    done = False
                    vendeur = "Serveur"
                    histo = open("histo.txt","a")
                    histo.write("------------------\n")
                    histo.write("Produit "+nom_prod+" :\n")
                    histo.close()
                    duree_vente = datetime.now()
                    tr = TestThreading()
                    diffuser(bytes("Une nvlle vente s'est lancée du produit : "+nom_prod+ "de prix : "+str(prix), "utf8"))
                    diffuser(bytes("pour rejoindre la vente tapez add_me", "utf8"))
                    
                    print("en attente de connection(s) avec les clients")
                elif (reponse=="2"):
                    bien = open("bien.txt","r")
                    l = bien.readlines()
                    for i in l :
                        print(i)
                    bien.close()
                    #bien.read(strbien(nom_prod,prixinit,prix,etat,acheteur+"\n")
                   # bien.close()
                elif (reponse=="3"):
                    nom=input("tapez le nom de l'acheteur que vous voullez avoir sa facture d'achat(s) =")
                    facture_acheteur( nom)
                elif (reponse=="4"):
                    histo = open("histo.txt","r")
                    l = histo.readlines()
                    for i in l :
                        print(i)
                    histo.close()
                elif (reponse=="5"):
                      os._exit(0)
                else:
                    print("Valeur saisie non valide")
            

            time.sleep(self.interval)
            

def accepter_connexions():
    while True:
        try:
            client, client_address = SERVER.accept()
            client.send(bytes("Ecrire votre nom !","utf8"))
            addresses[client] = client_address
            Thread(target=gerer_client, args=(client,)).start()
        except:
            print("")
            break
        


def gerer_client(client):  
    nom = client.recv(BUFSIZ).decode("utf8")
    global prix
    global acheteur
    global duree_vente
    global vente
    global done
    global test
    global nom_prod
    global prix
    global prixinit
    global vendeur
    if 1 :
        
        client.send(bytes('Bienvenue %s! ' % nom, "utf8"))
        tr = TestThreading()
        if (vente):
            client.send(bytes('Une vente aux enchères est en cours du produit :'+nom_prod+" de prix : "+str(prix)+"\n", "utf8"))
            client.send(bytes("\n pour rejoindre la vente tapez add_me", "utf8"))
        else :
            client.send(bytes("pas de vente aux enchères pour le moment, Merci d'attendre la prochaine vente!", "utf8"))
            client.send(bytes("", "utf8"))
            client.send(bytes("pour commencer une nvlle vente aux enchères tapez vendre [nom_produit] [prix_produit] ", "utf8"))
           
            #msg = "%s has joined the vente" % nom
            #diffuser(bytes(msg, "utf8"))
        while True:
            
            clients[client] = nom
            msg = client.recv(BUFSIZ)
            stringdata = msg.decode('utf-8')
            
            if vente:

                if "vendre" in stringdata:
                    client.send(bytes("Vous ne pouvez pas commencer une vente,Il y a déjà une en cours! ", "utf8"))
                
                if msg == bytes("add_me", "utf8") and not joined(nom) and nom!=vendeur:
                    add(nom)
                    ms = "%s rejoint la vente" % nom
                    diffuserj(bytes(ms, "utf8"))
                    client.send(bytes(''+nom_prod+" , prix actuel ( "+str(prix)+" ) ,\n", "utf8"))
                    client.send(bytes("pour quitter utilisez quitter_vente ", "utf8"))
                    print(nom+" rejoint la vente"); 
                   
                else :
                    if msg == bytes("add_me", "utf8") and joined(nom):
                        client.send(bytes("Vous etes déjà dans cette vente aux enchères! ", "utf8"))
                    if msg == bytes("add_me", "utf8") and nom ==vendeur:
                        client.send(bytes("Vous ne pouvez pas rejoindre votre propre vente  ", "utf8"))
                        
                if joined(nom):
                    try :
                        msgint=int(msg)
                        #print(nom,"placed a new bid:"+msg)
                        if (msgint > prix): #prix valide
                            diffuserj(msg,nom+" a proposé un nv prix :")
                            
                            if (acheteur!=""):
                                histo = open("histo.txt","a")
                                histo.write(ligne_historique(acheteur,prix,"echec\n"))

                                histo.close()
                            
                            prix = msgint
                            acheteur = nom
                            duree_vente= datetime.now()
                            done = False
                            print("dernier acheteur : "+nom+"("+str(msgint)+"),"+duree_vente.strftime("%H:%M:%S"))
                        else :
                            if msg != bytes("quitter_vente", "utf8"):
                                client.send(bytes("mavais choix!", "utf8"))
                    
                    except:
                        if (msg != bytes("quitter_vente", "utf8") and msg != bytes("add_me", "utf8")):
                            client.send(bytes("mavais choix!", "utf8"))
                
                if msg == bytes("quitter_vente", "utf8"):
                    if not joined(nom):
                        client.send(bytes("Vous n etes pas dans la vente actuelle !", "utf8"))
                    if acheteur == nom and joined(nom):
                        client.send(bytes("Vous ne pouvez pas quitter,vous etes le dernier acheteur!", "utf8"))
                    if acheteur != nom and joined(nom):
                        diffuserj(bytes("%s a quitté la vente." % nom, "utf8"))
                        print(nom+" a quitté la vente")
                        client.send(bytes("pour rejoindre la vente actuelle,tapez add_me", "utf8"))
                        quit(nom)
                if not joined(nom) and msg != bytes("add_me", "utf8") and msg != bytes("/q", "utf8"):
                    client.send(bytes("  !", "utf8"))
            else :
                if "vendre" in stringdata:
                    try :
                        nom_prod = stringdata.split(" ")[1]
                        prix = int(stringdata.split(" ")[2])
                        prixinit=prix
                        test = True
                    except :
                        test = False
                    if test :
                        vente = True
                        print(nom+" a commencé une nvelle vente")
                        vendeur = str( nom)
                        diffuserv(bytes(nom+" a commencé une nvelle vente : "+nom_prod+str(prix), "utf8"))
                        diffuserv(bytes("Pour rejoindre la vente en cours tapez add_me.", "utf8"))
                        client.send(bytes("vous avez commencé une  vente de :" +nom_prod+" de prix :" +str(prix), "utf8"))
                        print("connexion en cours...")
                        duree_vente= datetime.now()
                        done = False
                        tr = TestThreading()
                    else :
                        client.send(bytes("to start a new vente use vendre [product] [price] !", "utf8"))

                else :    
                    client.send(bytes("input non valide", "utf8"))
                
        
                 
               


def diffuser(msg, prefix=""): 
  """envoyer un message a tous les clients connectés au serveur"""
  for sock in clients:
    sock.send(bytes(prefix, "utf8")+msg)
def diffuserj(msg, prefix=""): 
  """envoyer un message aux clients qui ont rejoint la vente y compris le vendeur """
  for sock in clients:
    if joined(clients[sock]) or clients[sock]==vendeur :
        sock.send(bytes(prefix, "utf8")+msg)
  
def diffuserv(msg, prefix=""): 
  """envoyer un message a tous les clients connectés sauf le vendeur"""
  global vendeur
  for sock in clients:
    if  clients[sock]!=vendeur:
        sock.send(bytes(prefix, "utf8")+msg)


def joined(nom):
  """tester à partir du nom du client s'il a rejoint la vente"""

  global joins
  for i in joins:
    if i==nom:
        return True
  return False
def add(nom):
  """ajouter un client à la liste des clients joints"""
  global joins
  joins.append(nom)

def quit(nom):
  """supprimer un client à la liste des clients joints"""
  global joins
  joins.remove(nom)

def remplirfactures():
  """"remplir le dictionnaire factures à partir duu fichier factures.txt"""

  global factures
  fact = open("factures.txt","a")
  fact.close()
  fact = open("factures.txt","r")
  l = fact.readlines()
  fact.close()
  for i in l:
    nom = i.split(" ")[0]
    prix_b = i.split(" ")[-1]
    if prix_b[-1]=="\n":
        prix_b = prix_b[:-1]
    factures[nom]=int(prix_b)

 
def remplir():
#remplir et mettre à jour le fichier factures apres un succes de vente
  global factures
  fact = open("factures.txt","a")
  fact.close()
  fact = open("factures.txt","w")
  for i in factures:
      fact.write(ligne_fact(i,factures[i])+"\n")
  fact.close()

def ligne_fact(nom,prix):
  """ Format d'une ligne dans le fichier factures ,
      utile pour l'écriture dans ce fichier """
  return "{0:10} | {1}".format(nom, str(prix))

def ligne_bien(produit,prix_int,prix_fin,etat,achet):
  """ Format d'une ligne dans le fichier bien ,
  utile pour l'écriture dans ce fichier """
  return "{0:10} | {1:10} | {2:10} | {3:10} | {4:1}".format(produit,str(prix_int),str(prix_fin),str(etat), str(achet))


def ligne_historique(achet,prix,etat):
  """ Format d'une ligne dans le fichier historique ,
  utile pour l'écriture dans ce fichier """
  achet = acheteur
  return "{0:10} | {1:10} | {2}".format(str(achet),str(prix),str(etat))



clients = {}
addresses = {}



"""HOST = ''
PORT = 33000"""
#########ADDED
HOST='127.0.0.1'
PORT=30000
BUFSIZ = 1024
ADDR = (HOST, PORT)
# TCP
SERVER = socket(AF_INET, SOCK_STREAM) #le type du socket : SOCK_STREAM pour le protocole TCP
SERVER.bind(ADDR)

#SERVER.setblocking(0)
if __name__ == "__main__":
    while True :

        remplirfactures()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        m=menu()   
        print("The server is online")
        SERVER.listen(5)
        ACCEPT_THREAD = Thread(target=accepter_connexions)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        SERVER.close()

"""
#udp 

SERVER = socket(AF_INET, SOCK_DGRAM) #le type du socket : SOCK_STREAM pour le protocole TCP
# Lier à l'adresse IP et le port
SERVER.bind(("127.0.0.1", 33000))
print("Serveur UDP à l'écoute")

#SERVER.setblocking(0)
if __name__ == "__main__":
    #while True :

  remplirfactures()
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  
  m=menu()   
  print("The server is online")
  #SERVER.listen(5)
  ACCEPT_THREAD = Thread(target=accepter_connexions)
  ACCEPT_THREAD.start()
  ACCEPT_THREAD.join()
  SERVER.close()"""
