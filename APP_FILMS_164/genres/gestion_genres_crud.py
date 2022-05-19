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

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /personnes_afficher
    
    Test : ex : http://127.0.0.1:5005/personnes_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les genres.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/personnes_afficher/<string:order_by>/<int:id_genre_sel>", methods=['GET', 'POST'])
def personnes_afficher(order_by, id_genre_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_genre_sel == 0:
                    strsql_personnes_afficher = """SELECT id_personnes, nom, prenom, fonction FROM t_personnes ORDER BY id_personnes ASC"""
                    mc_afficher.execute(strsql_personnes_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_genre_selected_dictionnaire = {"value_id_genre_selected": id_genre_sel}
                    strsql_personnes_afficher = """SELECT id_personnes, nom,prenom,fonction FROM t_personnes WHERE id_personnes = %(value_id_genre_selected)s"""

                    mc_afficher.execute(strsql_personnes_afficher, valeur_id_genre_selected_dictionnaire)
                else:
                    strsql_personnes_afficher = """SELECT id_personnes, nom,prenom,fonction  FROM t_personnes ORDER BY id_personnes DESC"""

                    mc_afficher.execute(strsql_personnes_afficher)

                data_genres = mc_afficher.fetchall()

                print("data_genres ", data_genres, " Type : ", type(data_genres))

                # Différencier les messages si la table est vide.
                if not data_genres and id_genre_sel == 0:
                    flash("""La table "t_genre" est vide. !!""", "warning")
                elif not data_genres and id_genre_sel > 0:
                    # Si l'utilisateur change l'id_genre dans l'URL et que le genre n'existe pas,
                    flash(f"Le genre demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données personnes affichés!!", "success")

        except Exception as Exception_personnes_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{personnes_afficher.__name__} ; "
                                          f"{Exception_personnes_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("genres/personnes_afficher.html", data=data_genres)


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


@app.route("/genres_ajouter", methods=['GET', 'POST'])
def personnes_ajouter():
    form = FormWTFAjouterGenres()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                nom_personnes_wtf = form.nom_personnes_wtf.data
                name_genre = nom_personnes_wtf.lower()

                prenom_personnes_wtf = form.prenom_personnes_wtf.data
                prenom = prenom_personnes_wtf.lower()

                fonction_personnes_wtf = form.fonction_personnes_wtf.data
                fonction = fonction_personnes_wtf.lower()



                valeurs_insertion_dictionnaire = {"value_intitule_genre": name_genre, "Value_prenom_personne":prenom, "Value_fonction_personne":fonction}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_personnes = """INSERT INTO t_personnes (id_personnes,nom,prenom,fonction) VALUES (NULL,%(value_intitule_genre)s,%(Value_prenom_personne)s,%(Value_fonction_personne)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_personnes, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('personnes_afficher', order_by='DESC', id_genre_sel=0))

        except Exception as Exception_personnes_ajouter:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{personnes_ajouter.__name__} ; "
                                            f"{Exception_personnes_ajouter}")

    return render_template("genres/personnes_ajouter.html", form=form)



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


@app.route("/genre_update", methods=['GET', 'POST'])
def personnes_update():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_genre"
    id_genre_update = request.values['id_genre_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateGenre()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "personnes_update.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_genre_update = form_update.nom_personnes_update.data
            name_genre_update = name_genre_update.lower()

            prenom_personnes_update = form_update.nom_personnes_update.data
            prenom_personnes_update = prenom_personnes_update.lower()

            fonction_personnes_update = form_update.fonction_personnes_update.data
            fonction_personnes_update = fonction_personnes_update.lower()

            valeur_update_dictionnaire = {"value_id_genre": id_genre_update,
                                          "value_name_genre": name_genre_update,
                                          "value_prenom_personnes": prenom_personnes_update,
                                          "value_fonction_personnes": fonction_personnes_update,
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_nom_personne = """UPDATE t_personnes SET nom = %(value_name_genre)s, prenom = %(value_prenom_personnes)s, fonction = %(value_fonction_personnes)s \
             WHERE id_personnes = %(value_id_genre)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_nom_personne, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_genre_update"
            return redirect(url_for('personnes_afficher', order_by="ASC", id_genre_sel=id_genre_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
            str_sql_id_personne = "SELECT id_personnes, nom, prenom, fonction FROM t_personnes " \
                                   "WHERE id_personnes = %(value_id_genre)s"
            valeur_select_dictionnaire = {"value_id_genre": id_genre_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_personne, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_nom_genre = mybd_conn.fetchone()
            print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                  data_nom_genre["nom"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "personnes_update.html"
            form_update.nom_personnes_update.data = data_nom_genre["nom"]
            form_update.prenom_personnes_update.data = data_nom_genre["prenom"]
            form_update.fonction_personnes_update.data = data_nom_genre["fonction"]


    except Exception as Exception_personnes_update:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{personnes_update.__name__} ; "
                                      f"{Exception_personnes_update}")

    return render_template("genres/personnes_update.html", form_update=form_update)

"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "personnes_afficher.html"
    
    Remarque :  Dans le champ "nom_personnes_delete" du formulaire "genres/personnes_delete.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/genre_delete", methods=['GET', 'POST'])
def personnes_delete():
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
                str_sql_delete_personnes = """DELETE FROM t_personnes WHERE fk_personnes = %(value_id_genre)ss"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_genre_film"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_personnes, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_personnes, valeur_delete_dictionnaire)

                flash(f"Genre définitivement effacé !!", "success")
                print(f"Genre définitivement effacé !!")

                # afficher les données
                return redirect(url_for('personnes_afficher', order_by="ASC", id_genre_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_genre": id_genre_delete}
            print(id_genre_delete, type(id_genre_delete))

            # Requête qui affiche tous les films_genres qui ont le genre que l'utilisateur veut effacer
            str_sql_personnes_delete = """SELECT id_personnes, nom, prenom, fonction FROM t_personnes 
"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_personnes_delete, valeur_select_dictionnaire)
                data_films_attribue_genre_delete = mydb_conn.fetchall()
                print("data_films_attribue_genre_delete...", data_films_attribue_genre_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "genres/personnes_delete.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_genre_delete'] = data_films_attribue_genre_delete

                # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
                str_sql_id_telephones = "SELECT id_personnes, nom,prenom,fonction FROM t_personnes WHERE id_personnes = %(value_id_genre)s"

                mydb_conn.execute(str_sql_id_telephones, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
                data_nom_genre = mydb_conn.fetchone()
                print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                      data_nom_genre["nom"])
                print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                      data_nom_genre["prenom"])
                print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                      data_nom_genre["fonction"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "personnes_delete.html"
            form_delete.nom_personnes_delete.data = data_nom_genre["nom"]
            form_delete.nom_personnes_delete.data = data_nom_genre["prenom"]
            form_delete.nom_personnes_delete.data = data_nom_genre["fonction"]

            # Le bouton pour l'action "DELETE" dans le form. "personnes_delete.html" est caché.
            btn_submit_del = False

    except Exception as Exception_personnes_delete:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{personnes_delete.__name__} ; "
                                      f"{Exception_personnes_delete}")

    return render_template("genres/personnes_delete.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_genre_delete)
