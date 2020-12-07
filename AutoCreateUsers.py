#! /usr/bin/python3.9
# -*- coding:utf-8 -*-

# autocreate_users est un script Python pour automatiser l'ajout d'utilisateurs dans l'Active Directory depuis un fichier .txt.
# __author__      = "Steve Beyer"

import datetime
import os

# Préciser sur quel domaine la connexion s'effectue ainsi que l'OU et l'OU_groupe des utilisateurs       
domain_controller = 'DC=ledomaine,DC=com'
users_ou = 'OU=All,OU=Domain_Users,{}'.format(domain_controller)
groups_ou = 'OU=Domain_Users_Groups,{}'.format(domain_controller)

# Fonction qui crée le username(pour ouvrir une session sur le domaine), la fonction de l'utilisateur dans l'entreprise, le prénom et le nom complet.
def create_user(username, employee_id, display_name, active=False):
    """
    Créer un nouvel utilisateur dans l'AD
    :param username:
    :param employee_id:
    :param display_name:
    :param active:
    :return:
    """
    if active:
        disabled = 'no'
    else:
        disabled = 'yes'
    
    # Le module datetime donnera la date et l'heure auxquelles l'utilisateur a été créé dans la description du profil
    description = "Utilisateur ajouté par script python le  {}".format(datetime.datetime.now())
    default_password = 'P@55worD'

    dn = '"CN={},{}"'.format(username, users_ou)
    groups = '"cn=All,{}" '.format(groups_ou)
             
    command = 'dsadd user ' \
              '{} ' \
              '-samid "{}" ' \
              '-upn "{}" ' \
              '-display "{}" ' \
              '-empid "{}" ' \
              '-desc "{}" ' \
              '-disabled {} ' \
              '-pwd {} ' \
              '-mustchpwd yes ' \
              '-pwdneverexpires no ' \
              '-memberof {} ' \
              '-acctexpires never ' \
              ''.format(
                dn,
                username,
                username,
                display_name,
                employee_id,
                description,
                disabled,
                default_password,
                groups,
                )
    os.system(command)
    
# Se positionner dans le répertoire afin d'ouvrir le fichier texte
os.chdir(r'C:/Users/Administrateur/Documents/autocreate_users')
file = open('users.txt', 'rt')

# On rentre les lignes dans un tableau.
for line in file:
    # La fonction split() découpe une chaîne de caractères suivant les espaces qu'elle contient. Les paramètres sont délimités par la ",".
    users_paramaters_list = line.split(",")
    # On déclare un nouveau dictionnaire contenant les paramètres utilisateurs
    users_paramaters = {}
    users_paramaters['username'] = users_paramaters_list[0]
    users_paramaters['employee_id'] = users_paramaters_list[1]
    users_paramaters['display_name'] = users_paramaters_list[2]
    # On appel la fonction create_user pour associer les paramètres contenus dans le fichier texte 
    create_user(users_paramaters['username'],users_paramaters['employee_id'],users_paramaters['display_name'],active=True)
file.close()    

os.system("pause")
   

 
 
