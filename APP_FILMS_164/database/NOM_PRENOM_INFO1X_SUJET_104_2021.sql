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
-- Généré le :  Mer 08 Juin 2022 à 07:04
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
-- Structure de la table `t_compteur`
--

CREATE TABLE IF NOT EXISTS `t_compteur` (
`id_compteur` int(11) NOT NULL,
  `type` varchar(50) DEFAULT NULL,
  `DN` int(3) DEFAULT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=4 ;

--
-- Contenu de la table `t_compteur`
--

INSERT INTO `t_compteur` (`id_compteur`, `type`, `DN`) VALUES
(1, 'TOPAS® SONIC', 50),
(2, 'RUBIN® SONIC', 200),
(3, 'RUBIN WP-MF', 80);

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=5 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=6 ;

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
-- Index pour la table `t_compteur`
--
ALTER TABLE `t_compteur`
 ADD PRIMARY KEY (`id_compteur`);

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
-- Index pour la table `t_personnes`
--
ALTER TABLE `t_personnes`
 ADD PRIMARY KEY (`id_personnes`);

--
-- Index pour la table `t_telephones`
--
ALTER TABLE `t_telephones`
 ADD PRIMARY KEY (`id_telephones`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `t_compteur`
--
ALTER TABLE `t_compteur`
MODIFY `id_compteur` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT pour la table `t_localisations`
--
ALTER TABLE `t_localisations`
MODIFY `id_localisations` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=5;
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
--
-- AUTO_INCREMENT pour la table `t_telephones`
--
ALTER TABLE `t_telephones`
MODIFY `id_telephones` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=6;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;



