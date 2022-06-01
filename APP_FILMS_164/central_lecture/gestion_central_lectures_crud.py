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
from APP_FILMS_164.central_lecture.gestion_central_lectures_wtf_forms import FormWTFAjouterCentralLecture, \
    FormWTFUpdatCentralLecture
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.mails.gestion_mails_wtf_forms import FormWTFDeleteMails


"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /personnes_afficher
    
    Test : ex : http://127.0.0.1:5005/personnes_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les genres.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/central_lectures_afficher/<string:order_by>/<int:id_central_lectures_sel>", methods=['GET', 'POST'])
def central_lectures_afficher(order_by, id_central_lectures_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_central_lectures_sel == 0:
                    strsql_central_lectures_afficher = """SELECT id_central_lecture, type FROM t_central_lecture ORDER BY id_central_lecture ASC"""
                    mc_afficher.execute(strsql_central_lectures_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_central_lectures_selected_dictionnaire = {"value_id_central_lectures_selected": id_central_lectures_sel}
                    strsql_central_lectures_afficher = """SELECT id_central_lecture, type FROM t_central_lecture WHERE id_central_lecture = %(id_central_lectures_sel)s"""

                    mc_afficher.execute(strsql_central_lectures_afficher, valeur_id_central_lectures_selected_dictionnaire)
                else:
                    strsql_central_lectures_afficher = """SELECT id_central_lecture, type FROM t_central_lecture ORDER BY id_central_lecture DESC"""

                    mc_afficher.execute(strsql_central_lectures_afficher)

                data_central_lectures = mc_afficher.fetchall()

                print("data_mails ", data_central_lectures, " Type : ", type(data_central_lectures))

                # Différencier les messages si la table est vide.
                if not data_central_lectures and id_central_lectures_sel == 0:
                    flash("""La table "t_genre" est vide. !!""", "warning")
                elif not data_central_lectures and id_central_lectures_sel > 0:
                    # Si l'utilisateur change l'id_genre dans l'URL et que le genre n'existe pas,
                    flash(f"Le genre demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données personnes affichés!!", "success")

        except Exception as Exception_central_lectures_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{central_lectures_afficher.__name__} ; "
                                          f"{Exception_central_lectures_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("central_lectures/central_lectures_afficher.html", data=data_central_lectures)


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


@app.route("/central_lectures_ajouter", methods=['GET', 'POST'])
def central_lectures_ajouter():
    form = FormWTFAjouterCentralLecture()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                central_lecture_wtf = form.central_lecture_wtf.data
                central_lecture = central_lecture_wtf.lower()



                valeurs_insertion_dictionnaire = {"value_central_lecture": central_lecture}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_central_lecture = """INSERT INTO t_central_lecture (id_central_lecture,type) VALUES (NULL,%(value_central_lecture)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_central_lecture, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('central_lectures_afficher', order_by='DESC', id_central_lectures_sel=0))

        except Exception as Exception_central_lecture_ajouter:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{central_lectures_ajouter.__name__} ; "
                                            f"{Exception_central_lecture_ajouter}")

    return render_template("central_lectures/central_lectures_ajouter.html", form=form)



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


@app.route("/central_lectures_update", methods=['GET', 'POST'])
def central_lectures_update():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_genre"
    id_central_lecture_update = request.values['id_genre_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdatCentralLecture()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "personnes_update.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            central_lecture_update = form_update.central_lecture_update.data
            central_lecture_update = central_lecture_update.lower()

            valeur_update_dictionnaire = {"value_id_central_lecture": id_central_lecture_update,
                                          "value_central_lecture": central_lecture_update,

                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_central_lecture = """UPDATE t_central_lecture SET type = %(value_central_lecture)s\
             WHERE id_central_lecture = %(value_id_central_lecture)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_central_lecture, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_genre_update"
            return redirect(url_for('central_lectures_afficher', order_by="ASC", id_central_lecture_sel=0))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
            str_sql_id_central_lecture = "SELECT id_central_lecture, type FROM t_central_lecture " \
                                   "WHERE id_central_lecture = %(value_id_central_lecture)s"
            valeur_select_dictionnaire = {"value_id_central_lecture": id_central_lecture_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_central_lecture, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_central_lecture = mybd_conn.fetchone()
            print("data_central_lecture ", data_central_lecture, " type ", type(data_central_lecture), " genre ",
                  data_central_lecture["numero_telephone"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "personnes_update.html"
            form_update.central_lecture_update.data = data_central_lecture["type"]



    except Exception as Exception_mails_update:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{central_lecture_update.__name__} ; "
                                      f"{Exception_mails_update}")

    return render_template("central_lectures/central_lectures_update.html", form_update=form_update)

"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "personnes_afficher.html"
    
    Remarque :  Dans le champ "nom_personnes_delete" du formulaire "genres/personnes_delete.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/central_lectures_delete", methods=['GET', 'POST'])
def central_lectures_delete():
    data_films_attribue_genre_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_genre"
    id_mails_delete = request.values['id_genre_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleteMails()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("mails_afficher", order_by="ASC", id_mails_sel=0))

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
                valeur_delete_dictionnaire = {"value_id_mails": id_mails_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_mails = """DELETE FROM t_mails WHERE fk_mails = %(value_id_mails)s"""
               # str_sql_delete_mails = """DELETE FROM t_mails WHERE fk_mails = %(value_id_mails)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_genre_film"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_mails, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_mails, valeur_delete_dictionnaire)

                flash(f"Genre définitivement effacé !!", "success")
                print(f"Genre définitivement effacé !!")

                # afficher les données
                return redirect(url_for('mails_afficher', order_by="ASC", id_mails_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_mails": id_mails_delete}
            print(id_mails_delete, type(id_mails_delete))

            # Requête qui affiche tous les films_genres qui ont le genre que l'utilisateur veut effacer
            str_sql_delete_personnes = """DELETE FROM t_personnes WHERE fk_personnes = %(value_id_genre)s"""
            str_sql_mails_delete = """SELECT id_mails, nom_mail FROM t_mails"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_delete_personnes, valeur_select_dictionnaire)
                mydb_conn.execute(str_sql_mails_delete, valeur_select_dictionnaire)
                data_films_attribue_genre_delete = mydb_conn.fetchall()
                print("data_films_attribue_genre_delete...", data_films_attribue_genre_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "genres/personnes_delete.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_genre_delete'] = data_films_attribue_genre_delete

                # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
                str_sql_mails_delete = """SELECT id_personnes_avoir_mails , nom_mail, id_mails, nom, prenom, fonction FROM t_personnes_avoir_mails 
                                                            INNER JOIN t_mails ON t_personnes_avoir_mails.fk_mails = t_mails.id_mails
                                                            INNER JOIN t_personnes ON t_personnes_avoir_mails.fk_personnes = t_personnes.id_personnes
                                                            WHERE fk_personnes = %(value_id_genre)s"""

                mydb_conn.execute(str_sql_mails_delete, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
                data_nom_mail= mydb_conn.fetchone()
                print("data_nom_mail ", data_nom_mail, " type ", type(data_nom_mail), " genre ",
                      data_nom_mail["nom_mail"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "personnes_delete.html"
            form_delete.nom_personnes_delete.data = data_nom_mail["nom_mail"]

            # Le bouton pour l'action "DELETE" dans le form. "personnes_delete.html" est caché.
            btn_submit_del = False

    except Exception as Exception_mails_delete:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{central_lectures_delete.__name__} ; "
                                      f"{Exception_mails_delete}")

    return render_template("mails/mails_delete.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_genre_delete)
