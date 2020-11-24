#! /usr/bin/python3.9
# -*- coding:utf-8 -*-

import datetime
import os
import ldap

conn = ldap.initialize('ldap://127.0.0.1')
conn.protocol_version = 3
conn.set_option(ldap.OPT_REFERRALS, 0)
conn.simple_bind_s('Administrateur@ledomaine.com','deusEx156!')
        
domain_controller = 'DC=ledomaine,DC=com'
users_ou = 'OU=All,OU=Domain_Users,{}'.format(domain_controller)
groups_ou = 'OU=Domain_Users_Groups,{}'.format(domain_controller)

def create_user(username, employee_id, display_name,  active=False):
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

    description = "Utilisateur ajouté par script python à  {}".format(datetime.datetime.now())
    default_password = 'P@55worD'

    dn = '"CN={},{}"'.format(username, users_ou)
    groups = '"cn=All,{}" ' \
             '"cn=Users_Deny,{}" '.format(groups_ou, groups_ou)
             
    command = 'dsadd user ' \
              '{} ' \
              '-samid "{}" ' \
              '-upn "{}" ' \
              '-display "{}" ' \
              '-empid "{}" ' \
              '-desc "{}" ' \
              '-disabled {} ' \
              '-pwd {} ' \
              '-pwdneverexpires yes ' \
              '-mustchpwd yes ' \
              '-canchpwd yes ' \
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
    
create_user('jdoe','Commercial','John Doe',active=True)
#create_user('jadoe','Comptable','Jane Doe',active=True)
 
 
