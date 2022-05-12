"""
    Fichier : gestion_genres_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp


class FormWTFAjouterGenres(FlaskForm):
    """
        Dans le formulaire "personnes_ajouter.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_personnes_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_personnes_wtf = StringField("Entrer le nom ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                   Regexp(nom_personnes_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])
    prenom_personnes_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    prenom_personnes_wtf = StringField("Entrer le prenom ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                  Regexp(prenom_personnes_regexp,
                                                                         message="Pas de chiffres, de caractères "
                                                                                 "spéciaux, "
                                                                                 "d'espace à double, de double "
                                                                                 "apostrophe, de double trait union")
                                                                  ])
    fonction_personnes_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    fonction_personnes_wtf = StringField("Entrer la fonction ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                  Regexp(fonction_personnes_regexp,
                                                                         message="Pas de chiffres, de caractères "
                                                                                 "spéciaux, "
                                                                                 "d'espace à double, de double "
                                                                                 "apostrophe, de double trait union")
                                                                  ])


    submit = SubmitField("Enregistrer")


class FormWTFUpdateGenre(FlaskForm):
    """
        Dans le formulaire "personnes_update.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_personnes_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_personnes_update = StringField("Editez le nom ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(nom_personnes_update_regexp,
                                                                                 message="Pas de chiffres, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    prenom_personnes_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    prenom_personnes_update = StringField("Editez le prenom ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                     Regexp(prenom_personnes_update_regexp,
                                                                            message="Pas de chiffres, de "
                                                                                    "caractères "
                                                                                    "spéciaux, "
                                                                                    "d'espace à double, de double "
                                                                                    "apostrophe, de double trait "
                                                                                    "union")
                                                                     ])
    fonction_personnes_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    fonction_personnes_update = StringField("Editez la fonction ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                     Regexp(fonction_personnes_update_regexp,
                                                                            message="Pas de chiffres, de "
                                                                                    "caractères "
                                                                                    "spéciaux, "
                                                                                    "d'espace à double, de double "
                                                                                    "apostrophe, de double trait "
                                                                                    "union")
                                                                     ])

    date_genre_wtf_essai = DateField("Essai date", validators=[InputRequired("Date obligatoire"),
                                                               DataRequired("Date non valide")])
    submit = SubmitField("Update genre")


class FormWTFDeleteGenre(FlaskForm):
    """
        Dans le formulaire "personnes_delete.html"

        nom_personnes_delete : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    nom_personnes_delete = StringField("Effacer ce genre")
    submit_btn_del = SubmitField("Effacer genre")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
