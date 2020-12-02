
Qu'est ce que autocreate_users ?

autocreate_users est un script Python pour automatiser l'ajout d'utilisateurs dans l'Active Directory depuis un fichier .txt. Il est possible d'ajouter autant d'utilisateurs que nécessaire. Il est également possible de modifier le script pour utiliser les paramètres voulus. Ici, nous utiliserons le paramètre 'username' pour l'ouverture d'une session sur le domaine, le paramètre 'employee_id' pour la fonction de l'utilisateur dans l'entreprise, le paramètre 'display_name' pour le nom complet de l'utilisateur. le paramètre 'mustchpwd yes' est aussi activé pour autoriser l'utilisateur à changer son mot de passe à l'ouverture de la session. Un mot de passe par défaut est attribuer à la création du compte.
1. Importer les modules nécessaires au bon fonctionnement du script.

Le module ldap-python: Ce module va initialiser une connexion avec l'active afin de pouvoir la modifier. Il est impératif de se connecter avec le compte Administrateur pour les modification de l'AD.
https://www.python-ldap.org/en/python-ldap-3.3.0/installing.html

Le module datetime: Ce module informera sur la date et l'heure auxquelles les utilisateurs ont été créés.

Le module os: Le module os servira pour l'envoie de la commande 'dsadd user' avec ses paramètre vers le DOS(cmd). Il peut également pour se positionner dans le répertoire du projet.

2. Le 1er bloc pour initialiser la connexion à l'AD via ldap.

Le script est lancé depuis le serveur disposant lui-même du service Active Directory. Vous pouvez tester votre connexion ldap depuis internet explorer en entrant l'adresse de votre serveur avec le protocole ldap, ici: ldap://127.0.0.1

conn = ldap.initialize('ldap://127.0.0.1')

Nous utilisons le module python_ldap-3.3.1 donc la version 3
conn.protocol_version = 3

Pour pouvoir s'authentifier
conn.set_option(ldap.OPT_REFERRALS, 0)

Nous nous connectons avec le compte Administrateur et son mot de passe.
conn.simple_bind_s('Administrateur@ledomaine.com','password')

3. La déclaration du domaine et des OU (Unité Organisationnelle)

Le domaine controller sur lequel nous allons ajouter nos utilisateurs
ici ledomaine.com
domain_controller = 'DC=ledomaine,DC=com'

L'OU dans laquelle nos utilisateurs vont être créés Ici, ce sera dans l'OU 'All' de l'OU Domain_Users 
users_ou = 'OU=All,OU=Domain_Users,{}'.format(domain_controller)

L'OU dans laquelle se trouve le groupe utilisateurs ici, Domain_Users_Groups
groups_ou = 'OU=Domain_Users_Groups,{}'.format(domain_controller)

4. Création de la fonction 'create_user' avec ses paramètres

Nous allons demander à la fonction d'envoyer à 'cmd' la création d'un utilisateur via la commande 'dsadd user' avec les paramètres 'username', 'employee_id', 'display_name'. le boléen 'active' sera 'False' par défaut.

def create_user(username, employee_id, display_name, active=False):
"""
Créé un nouvel utilisateur dans l'AD
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

Le module datetime donnera la date et l'heure auxquelles l'utilisateur a été créé dans la description du profil.
Et nous déclarons le mot de par défaut de l'utilisateur.
description = "Utilisateur ajouté par script python le {}".format(datetime.datetime.now())
default_password = 'P@55worD'

Nous déclarons le dn (Distinguished Name) qui sera donc le 'username' dans l'OU 'All' et le groups dans le groupe 'All' \
dn = '"CN={},{}"'.format(username, users_ou) \
groups = '"cn=All,{}" '.format(groups_ou)

Remarque : Vous pouvez modifier selon les besoins

Nous déclarons, ensuite, la commande à utiliser \
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
''.format( dn, username, username, display_name, employee_id, description, disabled, default_password, groups, )

Nous envoyons la commande à 'cmd'
os.system(command)

5. Récupérer les paramètres dans un fichier texte(.txt) et appeler la fonction 'create_user'

On se positionne dans le répertoire où se trouve le script et le fichier .txt ouis on ouvre le fichier .txt \
os.chdir(r'C:/Users/Administrateur/Documents/autocreate_users') \
file = open('users.txt', 'rt')

le fichier .txt devra être écrit de la manière suivante:
jdoe,Commercial,John Doe
jadoe,Comptable,Jane Doe

Pour les lignes dans le fichier
for line in file:
La méthode strip() supprime tous les caractères à droite et à gauche de la chaîne de caractères.
La fonction split() va découper la chaîne de caractères en délimitant les blocs par la ",".
users_paramaters_list = line.strip().split(",")
On déclare un nouveau dictionnaire contenant les paramètres utilisateurs(0=username, 1=employee_id, 2=display_name)
users_paramaters = {}
users_paramaters['username'] = users_paramaters_list[0]
users_paramaters['employee_id'] = users_paramaters_list[1]
users_paramaters['display_name'] = users_paramaters_list[2]
On appelle la fonction create_user pour associer les paramètres contenus dans le fichier texte et on active le profil
create_user(users_paramaters['username'],users_paramaters['employee_id'],users_paramaters['display_name'],active=True)

On ferme le fichier
file.close()

Et on met le système en pause afin de voir le retour du script
os.system("pause")

Si le script est correctement écrit, vous devriez avoir ce retour dans 'cmd'
dsadd réussite:CN=jdoe,OU=All,OU=Domain_Users,DC=ledomaine,DC=com
dsadd réussite:CN=jadoe,OU=All,OU=Domain_Users,DC=ledomaine,DC=com
