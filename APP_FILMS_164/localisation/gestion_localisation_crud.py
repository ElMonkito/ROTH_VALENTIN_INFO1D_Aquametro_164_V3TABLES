"""Gestion des "routes" FLASK et des données pour les genres.
Fichier : gestion_genres_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
# from APP_FILMS_164.telephone.gestion_telephones_wtf_forms import FormWTFAjouterTelephones
from APP_FILMS_164.localisation.gestion_localisation_wtf_forms import FormWTFAjouterLocalisation, \
    FormWTFUpdateLocalisation, FormWTFDeleteLocalisation
from APP_FILMS_164.telephone.gestion_telephones_wtf_forms import FormWTFDeleteTelephones
from APP_FILMS_164.telephone.gestion_telephones_wtf_forms import FormWTFUpdateTelephones
from APP_FILMS_164.telephone.gestion_telephones_wtf_forms import FormWTFAjouterTelephones

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /personnes_afficher
    
    Test : ex : http://127.0.0.1:5005/personnes_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les genres.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/localisation_afficher/<string:order_by>/<int:id_localisation_sel>", methods=['GET', 'POST'])
def localisation_afficher(order_by, id_localisation_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_localisation_sel == 0:
                    strsql_localisation_afficher = """SELECT id_localisations, adresse, numero, NPA, ville  FROM t_localisations ORDER BY id_localisations ASC"""
                    mc_afficher.execute(strsql_localisation_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_localisation_selected_dictionnaire = {"value_id_localisation_selected": id_localisation_sel}
                    strsql_localisation_afficher = """SELECT id_localisations, adresse, numero, NPA, ville FROM t_localisations WHERE id_localisations = %(value_id_localisation_selected)s"""

                    mc_afficher.execute(strsql_localisation_afficher, valeur_id_localisation_selected_dictionnaire)
                else:
                    strsql_localisation_afficher = """SELECT id_localisations, adresse, numero, NPA, ville FROM t_localisations ORDER BY id_localisations DESC"""

                    mc_afficher.execute(strsql_localisation_afficher)

                data_localisation = mc_afficher.fetchall()

                print("data_localisation ", data_localisation, " Type : ", type(data_localisation))

                # Différencier les messages si la table est vide.
                if not data_localisation and id_localisation_sel == 0:
                    flash("""La table "t_genre" est vide. !!""", "warning")
                elif not data_localisation and id_localisation_sel > 0:
                    # Si l'utilisateur change l'id_genre dans l'URL et que le genre n'existe pas,
                    flash(f"Le genre demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données personnes affichés!!", "success")

        except Exception as Exception_localisation_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{localisation_afficher.__name__} ; "
                                          f"{Exception_localisation_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("localisations/localisation_afficher.html", data=data_localisation)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /genres_ajouter
    
    Test : ex : http://127.0.0.1:5005/genres_ajouter
    
    Paramètres : sans
    
    But : Ajouter un genre pour un film
    
    Remarque :  Dans le champ "name_genre_html" du formulaire "genres/genres_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/localisation_ajouter", methods=['GET', 'POST'])
def localisation_ajouter():
    form = FormWTFAjouterLocalisation()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                adresse_wtf = form.adresse_wtf.data
                adresse = adresse_wtf.lower()
                numero_wtf = form.numero_wtf.data
                numero = numero_wtf.lower()
                NPA_wtf = form.NPA_wtf.data
                npa = NPA_wtf.lower()
                ville_wtf = form.ville_wtf.data
                ville = ville_wtf.lower()



                valeurs_insertion_dictionnaire = {"value_adresse": adresse, "value_numero": numero, "value_npa": npa, "value_ville": ville,}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_localisation = """INSERT INTO t_localisations (id_localisations,adresse,numero,NPA,ville) VALUES (NULL,%(value_adresse)s,%(value_numero)s,%(value_npa)s,%(value_ville)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_localisation, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('localisation_afficher', order_by='DESC', id_localisation_sel=0))

        except Exception as Exception_localisation_ajouter:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{localisation_ajouter.__name__} ; "
                                            f"{Exception_localisation_ajouter}")

    return render_template("localisations/localisation_ajouter.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update
    
    Test : ex cliquer sur le menu "genres" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "personnes_afficher.html"
    
    Remarque :  Dans le champ "nom_personnes_update" du formulaire "genres/personnes_update.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/localisation_update", methods=['GET', 'POST'])
def localisation_update():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_genre"
    id_localisation_update = request.values['id_genre_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateLocalisation()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "personnes_update.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            adresse_update = form_update.adresse_update.data
            adresse_update = adresse_update.lower()

            numero_update = form_update.numero_update.data
            numero_update = numero_update.lower()

            NPA_update = form_update.NPA_update.data
            NPA_update = NPA_update.lower()

            ville_update = form_update.ville_update.data
            ville_update = ville_update.lower()

            valeur_update_dictionnaire = {"value_id_localisation": id_localisation_update,
                                          "value_adresse": adresse_update,
                                          "value_numero": numero_update,
                                          "value_npa": NPA_update,
                                          "value_ville": ville_update,

                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_localisation = """UPDATE t_localisations SET adresse = %(value_adresse)s, numero = %(value_numero)s, NPA = %(value_npa)s, ville = %(value_ville)s  WHERE id_localisations = %(value_id_localisation)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_localisation, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_genre_update"
            return redirect(url_for('localisation_afficher', order_by="ASC", id_localisation_sel=0))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
            str_sql_id_localisation = "SELECT id_localisations, adresse,numero,NPA,ville FROM t_localisations " \
                                   "WHERE id_localisations = %(value_id_localisation)s"
            valeur_select_dictionnaire = {"value_id_localisation": id_localisation_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_localisation, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_localisation = mybd_conn.fetchone()
            print("data_localisation ", data_localisation, " type ", type(data_localisation), " genre ",
                  data_localisation["adresse"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "personnes_update.html"
            form_update.adresse_update.data = data_localisation["adresse"]
            form_update.numero_update.data = data_localisation["numero"]
            form_update.NPA_update.data = data_localisation["NPA"]
            form_update.ville_update.data = data_localisation["ville"]

    except Exception as Exception_localisation_update:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{localisation_update.__name__} ; "
                                      f"{Exception_localisation_update}")

    return render_template("localisations/localisation_update.html", form_update=form_update)
"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "personnes_afficher.html"
    
    Remarque :  Dans le champ "nom_personnes_delete" du formulaire "genres/personnes_delete.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/localisation_delete", methods=['GET', 'POST'])
def localisation_delete():
    data_films_attribue_genre_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_genre"
    id_localisation_delete = request.values['id_genre_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleteLocalisation()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("localisation_afficher", order_by="ASC", id_mails_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "genres/personnes_delete.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_genre_delete = session['data_films_attribue_genre_delete']
                print("data_films_attribue_genre_delete ", data_films_attribue_genre_delete)

                flash(f"Effacer le genre de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_localisation": id_localisation_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_personnes = """DELETE FROM t_localisations WHERE id_localisations = %(value_id_localisation)s"""
                str_sql_delete_localisation = """DELETE FROM t_personnes_avoir_localisations WHERE fk_localisation = %(value_id_localisation)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_genre_film"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_personnes, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_localisation, valeur_delete_dictionnaire)

                flash(f"Genre définitivement effacé !!", "success")
                print(f"Genre définitivement effacé !!")

                # afficher les données
                return redirect(url_for('localisation_afficher', order_by="ASC", id_localisation_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_localisation": id_localisation_delete}
            print(id_localisation_delete, type(id_localisation_delete))

            # Requête qui affiche tous les films_genres qui ont le genre que l'utilisateur veut effacer
            str_sql_personnes_delete = """SELECT id_personnes, nom, prenom, fonction, id_localisations,adresse,numero,NPA,ville  FROM t_personnes_avoir_localisations 
                                            INNER JOIN t_personnes ON t_personnes_avoir_localisations.fk_personnes = t_personnes.id_personnes
                                            INNER JOIN t_localisations ON t_personnes_avoir_localisations.fk_localisation = t_localisations.id_localisations
                                            WHERE fk_localisation = %(value_id_localisation)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_personnes_delete, valeur_select_dictionnaire)
                data_films_attribue_genre_delete = mydb_conn.fetchall()
                print("data_films_attribue_genre_delete...", data_films_attribue_genre_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "genres/personnes_delete.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_genre_delete'] = data_films_attribue_genre_delete

                # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
                str_sql_id_localisation= "SELECT id_localisations, adresse,numero,NPA,ville FROM t_localisations WHERE id_localisations = %(value_id_localisation)s"

                mydb_conn.execute(str_sql_id_localisation, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
                data_localisation = mydb_conn.fetchone()
                print("data_localisation ", data_localisation, " type ", type(data_localisation), " genre ",
                      data_localisation["adresse"])
                print("data_localisation ", data_localisation, " type ", type(data_localisation), " genre ",
                      data_localisation["numero"])
                print("data_localisation ", data_localisation, " type ", type(data_localisation), " genre ",
                      data_localisation["NPA"])
                print("data_localisation ", data_localisation, " type ", type(data_localisation), " genre ",
                      data_localisation["ville"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "personnes_delete.html"
            form_delete.nom_personnes_delete.data = data_localisation["adresse"]
            form_delete.nom_personnes_delete.data = data_localisation["numero"]
            form_delete.nom_personnes_delete.data = data_localisation["NPA"]
            form_delete.nom_personnes_delete.data = data_localisation["ville"]

            # Le bouton pour l'action "DELETE" dans le form. "personnes_delete.html" est caché.
            btn_submit_del = False

    except Exception as Exception_localisation_delete:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{localisation_delete.__name__} ; "
                                      f"{Exception_localisation_delete}")

    return render_template("localisations/localisation_delete.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_genre_delete)
