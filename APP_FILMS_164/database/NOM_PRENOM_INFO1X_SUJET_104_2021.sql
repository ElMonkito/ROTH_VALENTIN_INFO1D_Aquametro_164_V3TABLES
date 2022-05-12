--

-- Database: roth_valentin_info1d_aquametro_bd_164
-- Détection si une autre base de donnée du même nom existe

DROP DATABASE IF EXISTS roth_valentin_info1d_aquametro_bd_164;

-- Création d'un nouvelle base de donnée

CREATE DATABASE IF NOT EXISTS roth_valentin_info1d_aquametro_bd_164;

-- Utilisation de cette base de donnée

USE roth_valentin_info1d_aquametro_bd_164;
-- phpMyAdmin SQL Dump
-- version 4.2.7.1
-- http://www.phpmyadmin.net
--
-- Client :  localhost
-- Généré le :  Mar 10 Mai 2022 à 19:32
-- Version du serveur :  5.6.20-log
-- Version de PHP :  5.4.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de données :  `roth_valentin_info1d_aquametro_bd_164`
--

-- --------------------------------------------------------

--
-- Structure de la table `t_calculateur`
--

CREATE TABLE IF NOT EXISTS `t_calculateur` (
  `id_calculateur` int(11) NOT NULL,
  `type` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Contenu de la table `t_calculateur`
--

INSERT INTO `t_calculateur` (`id_calculateur`, `type`) VALUES
(1, 'CALEC® ST III Standard & Smart'),
(2, 'CALEC® ST II');

-- --------------------------------------------------------

--
-- Structure de la table `t_calculateur_avoir_emplacement`
--

CREATE TABLE IF NOT EXISTS `t_calculateur_avoir_emplacement` (
  `id_calculateur_avoir_emplacement` int(11) NOT NULL,
  `fk_calculateur` int(11) DEFAULT NULL,
  `fk_emplacement` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Contenu de la table `t_calculateur_avoir_emplacement`
--

INSERT INTO `t_calculateur_avoir_emplacement` (`id_calculateur_avoir_emplacement`, `fk_calculateur`, `fk_emplacement`) VALUES
(1, 1, 2),
(2, 2, 3);

-- --------------------------------------------------------

--
-- Structure de la table `t_calculateur_avoir_mise_en_service`
--

CREATE TABLE IF NOT EXISTS `t_calculateur_avoir_mise_en_service` (
  `id_calculateur_avoir_mise_en_service` int(11) NOT NULL,
  `fk_calculateur` int(11) DEFAULT NULL,
  `fk_mise_en_service` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Contenu de la table `t_calculateur_avoir_mise_en_service`
--

INSERT INTO `t_calculateur_avoir_mise_en_service` (`id_calculateur_avoir_mise_en_service`, `fk_calculateur`, `fk_mise_en_service`) VALUES
(1, 2, 5),
(2, 1, 6);

-- --------------------------------------------------------

--
-- Structure de la table `t_central_lecture`
--

CREATE TABLE IF NOT EXISTS `t_central_lecture` (
  `id_central_lecture` int(11) NOT NULL,
  `type` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Contenu de la table `t_central_lecture`
--

INSERT INTO `t_central_lecture` (`id_central_lecture`, `type`) VALUES
(1, 'aquaradio® smart RDC Standard');

-- --------------------------------------------------------

--
-- Structure de la table `t_central_lecture_avoir_emplacement`
--

CREATE TABLE IF NOT EXISTS `t_central_lecture_avoir_emplacement` (
  `id_central_lecture_avoir_emplacement` int(11) NOT NULL,
  `fk_central_lecture` int(11) DEFAULT NULL,
  `fk_emplacement` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Contenu de la table `t_central_lecture_avoir_emplacement`
--

INSERT INTO `t_central_lecture_avoir_emplacement` (`id_central_lecture_avoir_emplacement`, `fk_central_lecture`, `fk_emplacement`) VALUES
(1, 1, 3);

-- --------------------------------------------------------

--
-- Structure de la table `t_central_lecture_avoir_mise_en_service`
--

CREATE TABLE IF NOT EXISTS `t_central_lecture_avoir_mise_en_service` (
  `id_central_lecture_avoir_mise_en_service` int(11) NOT NULL,
  `fk_central_lecture` int(11) DEFAULT NULL,
  `fk_mise_en_service` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Contenu de la table `t_central_lecture_avoir_mise_en_service`
--

INSERT INTO `t_central_lecture_avoir_mise_en_service` (`id_central_lecture_avoir_mise_en_service`, `fk_central_lecture`, `fk_mise_en_service`) VALUES
(1, 1, 4);

-- --------------------------------------------------------

--
-- Structure de la table `t_compteur`
--

CREATE TABLE IF NOT EXISTS `t_compteur` (
  `id_compteur` int(11) NOT NULL,
  `type` varchar(50) DEFAULT NULL,
  `DN` int(3) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Contenu de la table `t_compteur`
--

INSERT INTO `t_compteur` (`id_compteur`, `type`, `DN`) VALUES
(1, 'TOPAS® SONIC', 50),
(2, 'RUBIN® SONIC', 200),
(3, 'RUBIN WP-MF', 80);

-- --------------------------------------------------------

--
-- Structure de la table `t_compteur_avoir_emplacement`
--

CREATE TABLE IF NOT EXISTS `t_compteur_avoir_emplacement` (
  `id_compteur_avoir_emplacement` int(11) NOT NULL,
  `fk_compteur` int(11) DEFAULT NULL,
  `fk_emplacement` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Contenu de la table `t_compteur_avoir_emplacement`
--

INSERT INTO `t_compteur_avoir_emplacement` (`id_compteur_avoir_emplacement`, `fk_compteur`, `fk_emplacement`) VALUES
(1, 1, 1),
(2, 2, 2),
(4, 4, 3);

-- --------------------------------------------------------

--
-- Structure de la table `t_compteur_avoir_mise_en_service`
--

CREATE TABLE IF NOT EXISTS `t_compteur_avoir_mise_en_service` (
  `id_compteur_avoir_mise_en_service` int(11) NOT NULL,
  `fk_compteur` int(11) DEFAULT NULL,
  `fk_mise_en_service` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Contenu de la table `t_compteur_avoir_mise_en_service`
--

INSERT INTO `t_compteur_avoir_mise_en_service` (`id_compteur_avoir_mise_en_service`, `fk_compteur`, `fk_mise_en_service`) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 3);

-- --------------------------------------------------------

--
-- Structure de la table `t_emplacement`
--

CREATE TABLE IF NOT EXISTS `t_emplacement` (
  `id_emplacement` int(11) NOT NULL,
  `adresse` varchar(50) DEFAULT NULL,
  `numero` int(3) DEFAULT NULL,
  `appartement` int(3) DEFAULT NULL,
  `NPA` int(4) DEFAULT NULL,
  `ville` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Contenu de la table `t_emplacement`
--

INSERT INTO `t_emplacement` (`id_emplacement`, `adresse`, `numero`, `appartement`, `NPA`, `ville`) VALUES
(1, 'Av. Claude-Nobs ', 2, 8, 1820, 'Montreux'),
(2, 'Pl. du Marché ', 6, 36, 1820, 'Montreux'),
(3, 'Rte du Vernay ', 34, 17, 1870, 'Monthey');

-- --------------------------------------------------------

--
-- Structure de la table `t_localisations`
--

CREATE TABLE IF NOT EXISTS `t_localisations` (
  `id_localisations` int(11) NOT NULL,
  `adresse` varchar(50) DEFAULT NULL,
  `numero` int(3) DEFAULT NULL,
  `NPA` int(4) DEFAULT NULL,
  `ville` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Contenu de la table `t_localisations`
--

INSERT INTO `t_localisations` (`id_localisations`, `adresse`, `numero`, `NPA`, `ville`) VALUES
(1, 'Rue du Jura', 10, 1800, 'Vevey'),
(2, ' Rue Jean-Jacques Rousseau', 6, 1800, 'Vevey'),
(3, 'Chemin du raffort', 73, 1616, 'Attalens'),
(4, 'Rte de remaufens', 11, 1617, 'Tatroz');

-- --------------------------------------------------------

--
-- Structure de la table `t_mails`
--

CREATE TABLE IF NOT EXISTS `t_mails` (
`id_mails` int(11) NOT NULL,
  `nom_mail` varchar(320) DEFAULT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=5 ;

--
-- Contenu de la table `t_mails`
--

INSERT INTO `t_mails` (`id_mails`, `nom_mail`) VALUES
(1, 'derbigny.maxime@gmail.com'),
(2, 'blanc.john@gmail.com'),
(3, 'dupont.remy@gmail.com'),
(4, 'roth.valentin@gmail.com');

-- --------------------------------------------------------

--
-- Structure de la table `t_mise_en_service`
--

CREATE TABLE IF NOT EXISTS `t_mise_en_service` (
  `id_mise_en_service` int(11) NOT NULL,
  `date_mise_en_service` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Contenu de la table `t_mise_en_service`
--

INSERT INTO `t_mise_en_service` (`id_mise_en_service`, `date_mise_en_service`) VALUES
(1, '2014-07-16'),
(2, '2018-01-18'),
(3, '2009-05-11'),
(4, '2021-01-29'),
(5, '2016-10-04'),
(6, '2010-07-27');

-- --------------------------------------------------------

--
-- Structure de la table `t_personnes`
--

CREATE TABLE IF NOT EXISTS `t_personnes` (
`id_personnes` int(11) NOT NULL,
  `nom` varchar(32) DEFAULT NULL,
  `prenom` varchar(32) DEFAULT NULL,
  `fonction` varchar(32) DEFAULT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=8 ;

--
-- Contenu de la table `t_personnes`
--

INSERT INTO `t_personnes` (`id_personnes`, `nom`, `prenom`, `fonction`) VALUES
(1, 'Derbigny', 'Maxime', 'Client'),
(2, 'Blanc', 'John', 'Client'),
(3, 'Berger', 'Jean', 'Client'),
(4, 'Dupont ', 'Remy', 'Directeur'),
(5, 'Roth', 'Valentin', 'Vendeur');

-- --------------------------------------------------------

--
-- Structure de la table `t_personnes_avoir_calculateur`
--

CREATE TABLE IF NOT EXISTS `t_personnes_avoir_calculateur` (
  `id_personnes-avoir_calculateur` int(11) NOT NULL,
  `fk_personnes` int(11) DEFAULT NULL,
  `fk_calculateur` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Contenu de la table `t_personnes_avoir_calculateur`
--

INSERT INTO `t_personnes_avoir_calculateur` (`id_personnes-avoir_calculateur`, `fk_personnes`, `fk_calculateur`) VALUES
(1, 1, 2),
(2, 2, 1),
(3, 3, 1);

-- --------------------------------------------------------

--
-- Structure de la table `t_personnes_avoir_central_lecture`
--

CREATE TABLE IF NOT EXISTS `t_personnes_avoir_central_lecture` (
  `id_personnes_avoir_central_lecture` int(11) NOT NULL,
  `fk_personnes` int(11) DEFAULT NULL,
  `fk_central_lecture` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Contenu de la table `t_personnes_avoir_central_lecture`
--

INSERT INTO `t_personnes_avoir_central_lecture` (`id_personnes_avoir_central_lecture`, `fk_personnes`, `fk_central_lecture`) VALUES
(1, 1, 1),
(2, 2, 1),
(3, 3, 1);

-- --------------------------------------------------------

--
-- Structure de la table `t_personnes_avoir_compteur`
--

CREATE TABLE IF NOT EXISTS `t_personnes_avoir_compteur` (
  `id_personnes_avoir_compteur` int(11) NOT NULL,
  `fk_personnes` int(11) DEFAULT NULL,
  `fk_compteur` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Contenu de la table `t_personnes_avoir_compteur`
--

INSERT INTO `t_personnes_avoir_compteur` (`id_personnes_avoir_compteur`, `fk_personnes`, `fk_compteur`) VALUES
(1, 1, 1),
(2, 3, 2),
(4, 2, 3);

-- --------------------------------------------------------

--
-- Structure de la table `t_personnes_avoir_localisations`
--

CREATE TABLE IF NOT EXISTS `t_personnes_avoir_localisations` (
  `id_personnes_avoir_localisations` int(11) NOT NULL,
  `fk_personnes` int(11) DEFAULT NULL,
  `fk_localisation` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Contenu de la table `t_personnes_avoir_localisations`
--

INSERT INTO `t_personnes_avoir_localisations` (`id_personnes_avoir_localisations`, `fk_personnes`, `fk_localisation`) VALUES
(1, 1, 3),
(2, 2, 2),
(3, 3, 4),
(4, 4, 1),
(5, 5, 1);

-- --------------------------------------------------------

--
-- Structure de la table `t_personnes_avoir_mails`
--

CREATE TABLE IF NOT EXISTS `t_personnes_avoir_mails` (
  `id_personnes_avoir_mail` int(11) NOT NULL,
  `fk_personnes` int(11) DEFAULT NULL,
  `fk_mails` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Contenu de la table `t_personnes_avoir_mails`
--

INSERT INTO `t_personnes_avoir_mails` (`id_personnes_avoir_mail`, `fk_personnes`, `fk_mails`) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 4, 3);

-- --------------------------------------------------------

--
-- Structure de la table `t_personnes_avoir_telephones`
--

CREATE TABLE IF NOT EXISTS `t_personnes_avoir_telephones` (
  `id_personnes_avoir_telephones` int(11) NOT NULL,
  `fk_personnes` int(11) DEFAULT NULL,
  `fk_telephones` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Contenu de la table `t_personnes_avoir_telephones`
--

INSERT INTO `t_personnes_avoir_telephones` (`id_personnes_avoir_telephones`, `fk_personnes`, `fk_telephones`) VALUES
(1, 1, 1),
(2, 2, 3),
(3, 3, 4),
(4, 5, 2),
(5, 4, 5);

-- --------------------------------------------------------

--
-- Structure de la table `t_telephones`
--

CREATE TABLE IF NOT EXISTS `t_telephones` (
  `id_telephones` int(11) NOT NULL,
  `numero_telephone` varchar(12) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Contenu de la table `t_telephones`
--

INSERT INTO `t_telephones` (`id_telephones`, `numero_telephone`) VALUES
(1, '0794554356'),
(2, '0793661461'),
(3, '0786551435'),
(4, '0798239013'),
(5, '0765228875');

--
-- Index pour les tables exportées
--

--
-- Index pour la table `t_calculateur`
--
ALTER TABLE `t_calculateur`
 ADD PRIMARY KEY (`id_calculateur`);

--
-- Index pour la table `t_calculateur_avoir_emplacement`
--
ALTER TABLE `t_calculateur_avoir_emplacement`
 ADD PRIMARY KEY (`id_calculateur_avoir_emplacement`), ADD KEY `fk_calculateur` (`fk_calculateur`), ADD KEY `fk_emplacement` (`fk_emplacement`);

--
-- Index pour la table `t_calculateur_avoir_mise_en_service`
--
ALTER TABLE `t_calculateur_avoir_mise_en_service`
 ADD PRIMARY KEY (`id_calculateur_avoir_mise_en_service`), ADD KEY `fk_calculateur` (`fk_calculateur`), ADD KEY `fk_mise_en_service` (`fk_mise_en_service`);

--
-- Index pour la table `t_central_lecture`
--
ALTER TABLE `t_central_lecture`
 ADD PRIMARY KEY (`id_central_lecture`);

--
-- Index pour la table `t_central_lecture_avoir_emplacement`
--
ALTER TABLE `t_central_lecture_avoir_emplacement`
 ADD PRIMARY KEY (`id_central_lecture_avoir_emplacement`), ADD KEY `fk_central_lecture` (`fk_central_lecture`), ADD KEY `fk_emplacement` (`fk_emplacement`);

--
-- Index pour la table `t_central_lecture_avoir_mise_en_service`
--
ALTER TABLE `t_central_lecture_avoir_mise_en_service`
 ADD PRIMARY KEY (`id_central_lecture_avoir_mise_en_service`), ADD KEY `fk_central_lecture` (`fk_central_lecture`), ADD KEY `fk_mise_en_service` (`fk_mise_en_service`);

--
-- Index pour la table `t_compteur`
--
ALTER TABLE `t_compteur`
 ADD PRIMARY KEY (`id_compteur`);

--
-- Index pour la table `t_compteur_avoir_emplacement`
--
ALTER TABLE `t_compteur_avoir_emplacement`
 ADD PRIMARY KEY (`id_compteur_avoir_emplacement`), ADD KEY `fk_compteur` (`fk_compteur`), ADD KEY `fk_emplacement` (`fk_emplacement`);

--
-- Index pour la table `t_compteur_avoir_mise_en_service`
--
ALTER TABLE `t_compteur_avoir_mise_en_service`
 ADD PRIMARY KEY (`id_compteur_avoir_mise_en_service`), ADD KEY `fk_compteur` (`fk_compteur`), ADD KEY `fk_mise_en_service` (`fk_mise_en_service`);

--
-- Index pour la table `t_emplacement`
--
ALTER TABLE `t_emplacement`
 ADD PRIMARY KEY (`id_emplacement`);

--
-- Index pour la table `t_localisations`
--
ALTER TABLE `t_localisations`
 ADD PRIMARY KEY (`id_localisations`);

--
-- Index pour la table `t_mails`
--
ALTER TABLE `t_mails`
 ADD PRIMARY KEY (`id_mails`);

--
-- Index pour la table `t_mise_en_service`
--
ALTER TABLE `t_mise_en_service`
 ADD PRIMARY KEY (`id_mise_en_service`);

--
-- Index pour la table `t_personnes`
--
ALTER TABLE `t_personnes`
 ADD PRIMARY KEY (`id_personnes`);

--
-- Index pour la table `t_personnes_avoir_calculateur`
--
ALTER TABLE `t_personnes_avoir_calculateur`
 ADD PRIMARY KEY (`id_personnes-avoir_calculateur`), ADD KEY `fk_personnes` (`fk_personnes`), ADD KEY `fk_calculateur` (`fk_calculateur`);

--
-- Index pour la table `t_personnes_avoir_central_lecture`
--
ALTER TABLE `t_personnes_avoir_central_lecture`
 ADD PRIMARY KEY (`id_personnes_avoir_central_lecture`), ADD KEY `fk_personnes` (`fk_personnes`), ADD KEY `fk_central_lecture` (`fk_central_lecture`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `t_mails`
--
ALTER TABLE `t_mails`
MODIFY `id_mails` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT pour la table `t_personnes`
--
ALTER TABLE `t_personnes`
MODIFY `id_personnes` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=8;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
