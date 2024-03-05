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
        "tag": "numero_immatriculation",
        "patterns": [
            "Qu'est-ce que le numéro d'immatriculation du véhicule ?",
            "Comment est défini le numéro d'immatriculation d'un véhicule ?",
            "À quoi correspond le numéro d'immatriculation d'une voiture ?"
        ],
        "response": "Le numéro d'immatriculation d'un véhicule est un code unique attribué à ce véhicule lors de son enregistrement auprès des autorités compétentes. Il permet d'identifier de manière spécifique chaque véhicule circulant sur la voie publique. Ce numéro est généralement composé de lettres, de chiffres ou d'une combinaison des deux, selon les normes et réglementations en vigueur dans le pays concerné."
    },
    {
        "tag": "numero_identification",
        "patterns": [
            "Qu'est-ce que le numéro d'identification du véhicule ?",
            "En quoi consiste le numéro d'identification d'un véhicule ?",
            "À quoi sert le numéro d'identification d'une voiture ?"
        ],
        "response": "Le numéro d'identification du véhicule (NIV) est un identifiant unique attribué à un véhicule pour le distinguer des autres véhicules. Aussi connu sous le nom de numéro de châssis ou de numéro de série, il est généralement constitué d'une série de lettres et de chiffres spécifiques au véhicule. Le NIV est utilisé pour diverses raisons, notamment l'identification du véhicule lors d'opérations telles que l'achat, la vente, l'entretien et l'assurance."
    },
    {
        "tag": "date_1re_immatriculation",
        "patterns": [
            "Qu'est-ce que la date de 1re immatriculation du véhicule ?",
            "Comment est déterminée la date de 1re immatriculation d'un véhicule ?",
            "À quoi sert la date de 1re immatriculation d'une voiture ?"
        ],
        "response": "La date de 1re immatriculation d'un véhicule est la date à laquelle il a été officiellement enregistré pour la première fois auprès des autorités compétentes. Cette date est importante car elle permet de déterminer l'âge du véhicule et peut avoir un impact sur sa valeur, son admissibilité à certains programmes d'entretien ou de garantie, ainsi que sur sa conformité aux normes de sécurité et d'émissions en vigueur à cette époque."
    },
    {
        "tag": "marque",
        "patterns": [
            "Qu'est-ce que la marque d'un véhicule ?",
            "Comment est définie la marque d'une voiture ?",
            "À quoi correspond la marque d'un véhicule ?"
        ],
        "response": "La marque d'un véhicule est le nom commercial ou le logo sous lequel il est fabriqué et vendu par le fabricant. Il s'agit d'un élément distinctif qui permet d'identifier facilement le constructeur d'un véhicule. La marque peut être associée à une réputation de qualité, de fiabilité ou de prestige, ce qui peut influencer les choix des consommateurs lors de l'achat d'un véhicule."
    },
    {
        "tag": "type_variante_version",
        "patterns": [
            "Qu'est-ce que le type, la variante et la version d'un véhicule ?",
            "Comment sont définis le type, la variante et la version d'une voiture ?",
            "À quoi servent le type, la variante et la version d'un véhicule ?"
        ],
        "response": "Le type, la variante et la version d'un véhicule font référence à ses caractéristiques spécifiques qui le distinguent des autres modèles du même constructeur. Le type désigne la catégorie générale du véhicule, comme berline, break, SUV, etc. La variante se réfère à des variations mineures dans les caractéristiques, telles que la taille du moteur ou les options de finition. La version est une spécification particulière d'un modèle, souvent désignée par un code ou un nom spécifique, et peut inclure des équipements ou des fonctionnalités uniques."
    },
    {
        "tag": "genre_national",
        "patterns": [
            "Qu'est-ce que le genre national d'un véhicule ?",
            "Comment est défini le genre national d'une voiture ?",
            "À quoi correspond le genre national d'un véhicule ?"
        ],
        "response": "Le genre national d'un véhicule est une classification administrative qui identifie sa catégorie principale d'utilisation ou de construction selon les règlements et normes nationaux. Il peut s'agir de voitures particulières, de véhicules utilitaires, de motos, etc. Cette classification peut influencer divers aspects de la réglementation et de l'imposition, ainsi que des politiques liées à l'environnement et à la sécurité routière."
    },
    {
        "tag": "denomination_commerciale",
        "patterns": [
            "Qu'est-ce que la dénomination commerciale d'un véhicule ?",
            "Comment est définie la dénomination commerciale d'une voiture ?",
            "À quoi sert la dénomination commerciale d'un véhicule ?"
        ],
        "response": "La dénomination commerciale d'un véhicule est le nom donné par le fabricant pour identifier un modèle spécifique ou une gamme de modèles. Il s'agit souvent d'un nom de marque suivi d'un nom distinctif ou d'une série de lettres et de chiffres pour différencier les différentes versions ou configurations du modèle. La dénomination commerciale est utilisée dans la publicité, le marketing et la documentation associée au véhicule."
    },
    {
        "tag": "kilometrage_compteur",
        "patterns": [
            "Qu'est-ce que le kilométrage inscrit au compteur du véhicule ?",
            "Comment est mesuré le kilométrage inscrit au compteur d'une voiture ?",
            "À quoi sert le kilométrage inscrit au compteur d'un véhicule ?"
        ],
        "response": "Le kilométrage inscrit au compteur du véhicule est le nombre total de kilomètres parcourus par ce véhicule depuis sa mise en service ou depuis le dernier relevé du compteur. Il s'agit d'une mesure importante pour évaluer l'usure et l'entretien du véhicule, ainsi que pour déterminer sa valeur sur le marché de l'occasion. Le kilométrage est généralement enregistré par un dispositif mécanique ou électronique dans le tableau de bord du véhicule."
    },
    {
        "tag": "presence_certificat_immatriculation",
        "patterns": [
            "Qu'est-ce que la présence du certificat d'immatriculation ?",
            "Comment est déterminée la présence du certificat d'immatriculation d'un véhicule ?",
            "À quoi sert la présence du certificat d'immatriculation d'un véhicule ?"
        ],
        "response": "La présence du certificat d'immatriculation fait référence à la possession par le propriétaire du véhicule du document officiel délivré par les autorités compétentes et attestant de son immatriculation légale. Ce certificat, également appelé carte grise, est essentiel pour prouver la propriété du véhicule, ainsi que pour effectuer diverses transactions telles que la vente, l'assurance ou l'immatriculation dans un nouveau pays. La non-présentation du certificat peut entraîner des sanctions légales et administratives."
    }
]);
