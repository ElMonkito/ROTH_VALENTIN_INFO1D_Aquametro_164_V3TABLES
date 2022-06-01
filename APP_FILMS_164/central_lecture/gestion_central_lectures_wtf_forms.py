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


class FormWTFAjouterCentralLecture(FlaskForm):
    """
        Dans le formulaire "personnes_ajouter.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    central_lecture_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*[@.'\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    central_lecture_wtf = StringField("Entrer le central lecture ", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                                   Regexp(central_lecture_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])



    submit = SubmitField("Enregistrer")


class FormWTFUpdatCentralLecture(FlaskForm):
    """
        Dans le formulaire "personnes_update.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    central_lecture_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    central_lecture_update = StringField("Editez le mail", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                                          Regexp(central_lecture_update_regexp,
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


class FormWTFDeleteMails(FlaskForm):
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
