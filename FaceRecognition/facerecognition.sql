-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 17, 2020 at 09:41 PM
-- Server version: 5.7.28-0ubuntu0.18.04.4
-- PHP Version: 7.2.24-0ubuntu0.18.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- CREATE DATABASE facerecognition;
-- Database: `facerecognition`
--

-- --------------------------------------------------------

--
-- Table structure for table `Customer`
--
DROP TABLE IF EXISTS `Customer`;
DROP TABLE IF EXISTS `Account`;
DROP TABLE IF EXISTS `Savings_Account`;
DROP TABLE IF EXISTS `Transaction`;
DROP TABLE IF EXISTS `Customer_Account`;


-- # Create TABLE 'Customer'
CREATE TABLE `Customer` (
  `customer_id` int NOT NULL PRIMARY KEY,
  `name` varchar(50) NOT NULL,
  `login_time` time NOT NULL,
  `login_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create Table "Account"
Create TABLE `Account`(
  `account_num` varchar(20) NOT NULL PRIMARY KEY,
  `currency` varchar(15) NOT NULL,
  `balance` int NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create table for a type of account 'Savings Account'
Create TABLE `Savings_Account`(
  `account_num` varchar(20) NOT NULL PRIMARY KEY,
  `currency` varchar(15) NOT NULL,
  `balance` int NOT NULL,
  `interest_rate` int NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- create table Transaction
Create TABLE `Transaction`(
  `trans_id` int NOT NULL PRIMARY KEY,
  `amount` int NOT NULL,
  `time` time NOT NULL,
  `date` date NOT NULL,
  `to` varchar(20) NOT NULL,
  `from` varchar(20) NOT NULL,
  FOREIGN KEY(`to`) REFERENCES `Account`(`account_num`),
  FOREIGN KEY(`from`) REFERENCES `Account`(`account_num`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- create table cutomer_owns_account
Create TABLE `Customer_Account`(
  `customer_id` int NOT NULL,
  `account_num` varchar(20) NOT NULL,
  FOREIGN KEY(`customer_id`) REFERENCES `Customer`(`customer_id`),
  FOREIGN KEY(`account_num`) REFERENCES `Account`(`account_num`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `Customer` WRITE;
/*!40000 ALTER TABLE `Customer` DISABLE KEYS */;
INSERT INTO `Customer` VALUES (1, "JACK", NOW(), '2021-09-01');
/*!40000 ALTER TABLE `Customer` ENABLE KEYS */;
UNLOCK TABLES;


# Create TABLE 'Account'
# Create TABLE 'Transaction'
# Create other TABLE...


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
