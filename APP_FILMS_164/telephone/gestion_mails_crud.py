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
from APP_FILMS_164.genres.gestion_genres_wtf_forms import FormWTFAjouterGenres
from APP_FILMS_164.genres.gestion_genres_wtf_forms import FormWTFDeleteGenre
from APP_FILMS_164.genres.gestion_genres_wtf_forms import FormWTFUpdateGenre
from APP_FILMS_164.mails.gestion_mails_wtf_forms import FormWTFAjouterMails

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /personnes_afficher
    
    Test : ex : http://127.0.0.1:5005/personnes_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les genres.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/telephones_afficher/<string:order_by>/<int:id_telephones_sel>", methods=['GET', 'POST'])
def telephones_afficher(order_by, id_telephones_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_telephones_sel == 0:
                    strsql_telephones_afficher = """SELECT id_telephones, numero_telephone FROM t_telephones ORDER BY id_telephones ASC"""
                    mc_afficher.execute(strsql_telephones_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_telephones_selected_dictionnaire = {"value_id_telephones_selected": id_telephones_sel}
                    strsql_telephones_afficher = """SELECT id_telephones, numero_telephone FROM t_telephones WHERE id_telephones = %(value_id_telephones_selected)s"""

                    mc_afficher.execute(strsql_telephones_afficher, valeur_id_telephones_selected_dictionnaire)
                else:
                    strsql_telephones_afficher = """SELECT id_mails, nom_mail FROM t_mails ORDER BY id_mails DESC"""

                    mc_afficher.execute(strsql_telephones_afficher)

                data_mails = mc_afficher.fetchall()

                print("data_telephones ", data_telephones, " Type : ", type(data_telephones))

                # Différencier les messages si la table est vide.
                if not data_telephones and id_telephones_sel == 0:
                    flash("""La table "t_genre" est vide. !!""", "warning")
                elif not data_telephones and id_telephones_sel > 0:
                    # Si l'utilisateur change l'id_genre dans l'URL et que le genre n'existe pas,
                    flash(f"Le genre demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données personnes affichés!!", "success")

        except Exception as Exception_telephones_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{telephones_afficher.__name__} ; "
                                          f"{Exception_telephones_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("mails/mails_afficher.html", data=data_mails)


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


@app.route("/mails_ajouter", methods=['GET', 'POST'])
def mails_ajouter():
    form = FormWTFAjouterMails()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                nom_mails_wtf = form.nom_mails_wtf.data
                name_mails = nom_mails_wtf.lower()



                valeurs_insertion_dictionnaire = {"value_nom_mails": name_mails}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_mails = """INSERT INTO t_mails (id_mails,nom_mail) VALUES (NULL,%(value_nom_mails)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_mails, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('mails_afficher', order_by='DESC', id_mails_sel=0))

        except Exception as Exception_mails_ajouter:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{mails_ajouter.__name__} ; "
                                            f"{Exception_mails_ajouter}")

    return render_template("mails/mails_ajouter.html", form=form)



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


@app.route("/mails_update", methods=['GET', 'POST'])
def mails_update():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_genre"
    id_mails_update = request.values['id_genre_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateGenre()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "personnes_update.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_mails_update = form_update.nom_mails_update.data
            name_mails_update = name_mails_update.lower()

            valeur_update_dictionnaire = {"value_id_mails": id_mails_update,
                                          "value_name_mails": name_mails_update,

                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_nom_mails = """UPDATE t_mails SET nom_mail = %(value_name_mails)s\
             WHERE id_mails = %(value_id_mails)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_nom_mails, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_genre_update"
            return redirect(url_for('mails_afficher', order_by="ASC", id_mails_sel=id_mails_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
            str_sql_id_mails = "SELECT id_mails, nom_mail FROM t_mails " \
                                   "WHERE id_mails = %(value_id_mails)s"
            valeur_select_dictionnaire = {"value_id_mails": id_mails_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_mails, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_nom_genre = mybd_conn.fetchone()
            print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                  data_nom_genre["nom_mail"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "personnes_update.html"
            form_update.nom_personnes_update.data = data_nom_genre["nom_mail"]



    except Exception as Exception_mails_update:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{mails_update.__name__} ; "
                                      f"{Exception_mails_update}")

    return render_template("mails/mails_update.html", form_update=form_update)

"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "personnes_afficher.html"
    
    Remarque :  Dans le champ "nom_personnes_delete" du formulaire "genres/personnes_delete.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/mails_delete", methods=['GET', 'POST'])
def mails_delete():
    data_films_attribue_genre_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_genre"
    id_genre_delete = request.values['id_genre_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleteGenre()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("personnes_afficher", order_by="ASC", id_genre_sel=0))

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
                valeur_delete_dictionnaire = {"value_id_genre": id_genre_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_personnes = """DELETE FROM t_personnes WHERE fk_personnes = %(value_id_genre)s"""
                str_sql_delete_telephones = """DELETE FROM t_telephones WHERE fk_telephones = %(value_id_genre)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_genre_film"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_personnes, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_telephones, valeur_delete_dictionnaire)

                flash(f"Genre définitivement effacé !!", "success")
                print(f"Genre définitivement effacé !!")

                # afficher les données
                return redirect(url_for('personnes_afficher', order_by="ASC", id_genre_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_genre": id_genre_delete}
            print(id_genre_delete, type(id_genre_delete))

            # Requête qui affiche tous les films_genres qui ont le genre que l'utilisateur veut effacer
            str_sql_personnes_delete = """SELECT id_personnes, nom, prenom, fonction, id_mails, nom_mail, id_telephones,numero_telephone  FROM t_personnes 
                                            INNER JOIN t_mails ON t_personnes.fk_mails = t_mails.id_mails
                                            INNER JOIN t_telephones ON t_personnes.fk_telephones = t_telephones.id_telephones
                                            WHERE fk_telephones = %(value_id_genre)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_personnes_delete, valeur_select_dictionnaire)
                data_films_attribue_genre_delete = mydb_conn.fetchall()
                print("data_films_attribue_genre_delete...", data_films_attribue_genre_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "genres/personnes_delete.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_genre_delete'] = data_films_attribue_genre_delete

                # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
                str_sql_id_telephones = "SELECT id_telephones, numero_telephone FROM t_telephones WHERE id_telephones = %(value_id_genre)s"

                mydb_conn.execute(str_sql_id_telephones, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
                data_nom_genre = mydb_conn.fetchone()
                print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                      data_nom_genre["intitule_genre"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "personnes_delete.html"
            form_delete.nom_personnes_delete.data = data_nom_genre["intitule_genre"]

            # Le bouton pour l'action "DELETE" dans le form. "personnes_delete.html" est caché.
            btn_submit_del = False

    except Exception as Exception_personnes_delete:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{mails_delete.__name__} ; "
                                      f"{Exception_personnes_delete}")

    return render_template("genres/personnes_delete.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_genre_delete)
