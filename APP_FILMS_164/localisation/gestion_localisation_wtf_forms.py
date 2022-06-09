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


class FormWTFAjouterLocalisation(FlaskForm):
    """
        Dans le formulaire "personnes_ajouter.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    adresse_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+"
    adresse_wtf = StringField("Entrer l'adresse ", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                                   Regexp(adresse_regexp,
                                                                          message="Pas de lettres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])
    numero_regexp = "[-+]?[0-9]*\.?[0-9]*"
    numero_wtf = StringField("Entrer le numero ", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                               Regexp(numero_regexp,
                                                                      message="Pas de lettres, de caractères "
                                                                              "spéciaux, "
                                                                              "d'espace à double, de double "
                                                                              "apostrophe, de double trait union")
                                                               ])
    NPA_regexp = "[-+]?[0-9]*\.?[0-9]*"
    NPA_wtf = StringField("Entrer le NPA ", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                              Regexp(NPA_regexp,
                                                                     message="Pas de lettres, de caractères "
                                                                             "spéciaux, "
                                                                             "d'espace à double, de double "
                                                                             "apostrophe, de double trait union")
                                                              ])
    ville_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+"
    ville_wtf = StringField("Entrer la ville", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                              Regexp(ville_regexp,
                                                                     message="Pas de lettres, de caractères "
                                                                             "spéciaux, "
                                                                             "d'espace à double, de double "
                                                                             "apostrophe, de double trait union")
                                                              ])



    submit = SubmitField("Enregistrer")


class FormWTFUpdateLocalisation(FlaskForm):
    """
        Dans le formulaire "personnes_update.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    adresse_regexp =  "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+"
    adresse_update = StringField("Editez l'adresse", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                                          Regexp(adresse_regexp,
                                                                                 message="Pas de lettre, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    numero_regexp = "[-+]?[0-9]*\.?[0-9]*"
    numero_update = StringField("Editez le numero", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                                 Regexp(numero_regexp,
                                                                        message="Pas de lettre, de "
                                                                                "caractères "
                                                                                "spéciaux, "
                                                                                "d'espace à double, de double "
                                                                                "apostrophe, de double trait "
                                                                                "union")
                                                                 ])
    NPA_regexp = "[-+]?[0-9]*\.?[0-9]*"
    NPA_update = StringField("Editez le NPA", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                                 Regexp(NPA_regexp,
                                                                        message="Pas de lettre, de "
                                                                                "caractères "
                                                                                "spéciaux, "
                                                                                "d'espace à double, de double "
                                                                                "apostrophe, de double trait "
                                                                                "union")
                                                                 ])
    ville_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+"
    ville_update = StringField("Editez la ville", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                                 Regexp(ville_regexp,
                                                                        message="Pas de lettre, de "
                                                                                "caractères "
                                                                                "spéciaux, "
                                                                                "d'espace à double, de double "
                                                                                "apostrophe, de double trait "
                                                                                "union")
                                                                 ])


    date_genre_wtf_essai = DateField("Essai date", validators=[InputRequired("Date obligatoire"),
                                                               DataRequired("Date non valide")])
    submit = SubmitField("Update genre")


class FormWTFDeleteLocalisation(FlaskForm):
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
