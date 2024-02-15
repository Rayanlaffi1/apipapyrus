var db = db.getSiblingDB('papyrusdb');
db.intents.insertMany([
    {
        "tag": "nom",
        "patterns": [
            "Quel est ton nom ?", 
            "Peux-tu me dire quel est ton prénom ?", 
            "Sous quel nom es-tu connu(e) ?", 
            "Quel est ton prénom ?", 
            "Quel est ton nom ?", 
            "Comment tu t'appelle ?", 
            "Comment te nommes-tu ?" 
        ],
        "responses": [
            "Je m'appelle Papyrus.", 
            "Mon prénom est Papyrus.", 
            "Mon nom est Papyrus.", 
            "Salut moi c'est Papyrus." 
        ]
    },
    {
        "tag": "cestquoinumimmat",
        "patterns": [
            "C'est quoi un numéro d'immatriculation de véhicule ?", 
            "Peux-tu me dire ce qu'est un numéro d'immatriculation ?", 
            "Qu'est ce qu'est un numéro d'immatriculation ?",  
            "C'est quoi une plaque d'immatriculation ?", 
            "Je ne comprend pas ce qu'est un numéro d'immatriculation ?"
        ],
        "responses": [
            "Le numéro d'immatriculation est une série alphanumérique qui permet de définir l'identité d'un véhicule. Afin de circuler sur la voie publique, ce numéro est obligatoire pour tous les véhicules circulant sur nos routes. Depuis 2009, les numéros d'immatriculation sont attribués par le Système d'Immatriculation des Véhicules (SIV) au niveau national, de manière chronologique et uniformisée au format AA-123-AA. Ce numéro n'est plus modifié lors d'un changement de propriétaire ou d'un changement d'adresse. Il est attribué pour la durée de vie entière du véhicule et est inscrit dans le champ A de la carte grise. En effet, il ne change pas même pour un nouveau titulaire ou une demande de duplicata de certificat d'immatriculation par exemple." 
        ]
    },
    {
        "tag": "aquoisertnumimmat",
        "patterns": [
            "Ou trouver le numéro d'immatriculation de mon véhicule ?", 
            "Comment faire pour trouver le numéro d'immatriculation de mon véhicule ?", 
            "Où est situé le numéro d'immatriculation de mon véhicule ?", 
            "Où est trouver le numéro d'immatriculation sur la carte grise ?",
            "A quoi sert le numéro d'immatriculation ?", 
            "A quoi sert l'immatriculation ?", 
            "Ca sert à quoi le numéro d'immatriculation ?", 
            "Où est mentionné le numéro d'immatriculation sur la carte grise ?"
        ],
        "responses": [
            "Le numéro d'immatriculation est affecté à chaque véhicule circulant sur la voie publique. Il est reproduit sur une plaque d'immatriculation installée sur le véhicule. Ce numéro d'immatriculation est indiqué sur le certificat d'immatriculation du véhicule. Ce numéro figure en haut de la carte grise mais aussi sur le coupon détachable. C'est d'ailleurs la première information donnée. En effet, vous pouvez le trouver en case A du certificat d'immatriculation (CI). En case A.1, vous trouverez également l'ancien numéro d'immatriculation ainsi que la première date d'immatriculation en case B." 
        ]
    }
]);
