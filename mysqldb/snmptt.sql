-- phpMyAdmin SQL Dump
-- version 3.3.7deb5build0.10.10.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Oct 18, 2011 at 11:03 PM
-- Server version: 5.1.49
-- PHP Version: 5.3.3-1ubuntu9.5

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `snmptt`
--

-- --------------------------------------------------------

--
-- Table structure for table `id_info`
--

CREATE TABLE IF NOT EXISTS `id_info` (
  `deamon_id` varchar(64) NOT NULL,
  `index_id` int(16) DEFAULT NULL,
  `deamon_name` varchar(16) DEFAULT NULL,
  `time_stamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`deamon_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `log`
--

CREATE TABLE IF NOT EXISTS `log` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `logtime` varchar(50) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `severity_old` varchar(50) DEFAULT NULL,
  `severity_new` varchar(50) DEFAULT NULL,
  `category_old` varchar(50) DEFAULT NULL,
  `category_new` varchar(50) DEFAULT NULL,
  `comment_old` varchar(50) DEFAULT NULL,
  `comment_new` varchar(50) DEFAULT NULL,
  `description_old` varchar(50) DEFAULT NULL,
  `description_new` varchar(50) DEFAULT NULL,
  `acknowledge_old` varchar(50) DEFAULT NULL,
  `acknowledge_new` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `snmptt`
--

CREATE TABLE IF NOT EXISTS `snmptt` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `eventname` varchar(50) DEFAULT NULL,
  `eventid` varchar(50) DEFAULT NULL,
  `trapoid` varchar(100) DEFAULT NULL,
  `enterprise` varchar(100) DEFAULT NULL,
  `community` varchar(20) DEFAULT NULL,
  `hostname` varchar(100) DEFAULT NULL,
  `agentip` varchar(16) DEFAULT NULL,
  `category` varchar(20) DEFAULT NULL,
  `severity` varchar(20) DEFAULT NULL,
  `uptime` varchar(20) DEFAULT NULL,
  `traptime` varchar(30) DEFAULT NULL,
  `formatline` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7258 ;

-- --------------------------------------------------------

--
-- Table structure for table `snmptt_statistics`
--

CREATE TABLE IF NOT EXISTS `snmptt_statistics` (
  `stat_time` varchar(30) DEFAULT NULL,
  `total_received` bigint(20) DEFAULT NULL,
  `total_translated` bigint(20) DEFAULT NULL,
  `total_ignored` bigint(20) DEFAULT NULL,
  `total_unknown` bigint(20) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `snmptt_unknown`
--

CREATE TABLE IF NOT EXISTS `snmptt_unknown` (
  `trapoid` varchar(100) DEFAULT NULL,
  `enterprise` varchar(100) DEFAULT NULL,
  `community` varchar(20) DEFAULT NULL,
  `hostname` varchar(100) DEFAULT NULL,
  `agentip` varchar(16) DEFAULT NULL,
  `uptime` varchar(20) DEFAULT NULL,
  `traptime` varchar(30) DEFAULT NULL,
  `formatline` varchar(255) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
