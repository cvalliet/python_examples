#!/usr/bin/env python3

import argparse
from immo_tools import calculator


# Achat MASSY
def Achat(bien_immobilier, bien_mobilier, frais_agence, taux_notaire):
    prix_bien = bien_immobilier + bien_mobilier
    prix_vente = prix_bien + frais_agence
 
    taux_notaire /= 100
    frais_notaire = bien_immobilier * taux_notaire

    montant = prix_vente + frais_notaire

    print('### ACHAT ###################')
    print('')
    print(' Bien immobilier     %6d €' % bien_immobilier)
    print(' Bien mobilier     + %6d €' % bien_mobilier)
    print('                   ---------')
    print('                   = %6d €' % prix_bien)
    print(' Frais agence      + %6d €' % frais_agence)
    print('                   ---------')
    print('                   = %6d €' % prix_vente)
    print(' Frais notaire     + %6d €' % frais_notaire)
    print(' (taux : %.01f %%)' % (taux_notaire * 100))
    print('                   ---------')
    print('           Total   = %6d €' % montant)
    print('')
    print('')

    return montant


# Vente SAULX
def Vente(bien_immobilier, bien_mobilier, frais_agence, encours):
    prix_bien = bien_immobilier + bien_mobilier
    prix_vente = prix_bien - frais_agence
    restant = prix_vente - encours
    
    print('### VENTE ###################')
    print('')
    print(' Bien immobilier     %6d €' % bien_immobilier)
    print(' Bien mobilier     + %6d €' % bien_mobilier)
    print('                   ---------')
    print('                   = %6d €' % prix_bien)
    print(' Frais agence      - %6d €' % frais_agence)
    print('                   ---------')
    print('                   = %6d €' % prix_vente)
    print(' Ancien credit     - %6d €' % encours)
    print('                   ---------')
    print('           Total   = %6d €' % restant)
    print('')
    print('')

    return restant


# Prêt
def Pret(achat, vente, apport, duree, tp, ta):
    emprunt = achat - (vente + apport) 
    
    pret = calculator.build_loan(
        duree, 
        emprunt, 
        tp, 
        ta, 
        build_summary=True, 
        duration_unit='month')

    # Tableau d'amortissement :
    summary = pret.summary

    # montant total des intérêts payés :
    #print(pret.get_interests())

    # mensualités sans assurance :
    #monthly = pret.get_monthly()

    # Coût de l'emprunt au bout de la duree :
    #print(pret.get_cost(duree // 12))

    print('### PRET ####################')
    print('')
    print(' Achat               %6d €' % achat)
    print(' Vente             - %6d €' % vente)
    print(' Apport            - %6d €' % apport)
    print('                   ---------')
    print('           Total   = %6d €' % emprunt)
    print('')
    print(' Taux              %0.2f %%' % tp)
    print(' Taux assurance    %0.2f %%' % ta)
    print(' Duree             %d mois' % duree)
    print('')
    print(summary)
    print('')
    print('')
   

if __name__ == '__main__':
    print('')

    #parser = argparse.ArgumentParser(description='')
    #parser.add_argument()
    #args = parser.parse_args()

    achat_bien_immobilier = 601000
    achat_bien_mobilier = 9000
    achat_frais_agence = 29000 
    achat_taux_notaire = 8

    vente_bien_immobilier = 370000
    vente_bien_mobilier = 10000
    vente_frais_agence = 14620
    vente_encours = 29800
    
    apport = 30000 + 35000
    duree = 240
    tp = 1.3
    ta = 0.8

    achat = Achat(achat_bien_immobilier, achat_bien_mobilier, achat_frais_agence, achat_taux_notaire)
    vente = Vente(vente_bien_immobilier, vente_bien_mobilier, vente_frais_agence, vente_encours)
   
    Pret(achat, vente, apport, duree, tp, ta)
    
