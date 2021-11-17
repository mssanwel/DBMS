-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:82
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
DROP TABLE IF EXISTS `Transaction`;
DROP TABLE IF EXISTS `Savings_Account`;
DROP TABLE IF EXISTS `Customer_Account`;
DROP TABLE IF EXISTS `Account`;
DROP TABLE IF EXISTS `Customer`;


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

-- LOCK TABLES `Customer`, `Account`, `Savings_Account`, `Transaction`, `Customer_Account`  WRITE;
-- /*!40000 ALTER TABLE `Customer` DISABLE KEYS */;
INSERT INTO `Customer` VALUES (0, "Areeb", NOW(), '2021-09-01');
INSERT INTO `Customer` VALUES (2, "Saad", NOW(), '2021-09-01');
INSERT INTO `Account` VALUES ("A10001", "HKD", 1000);
INSERT INTO `Account` VALUES ("A10002", "HKD", 1000);
INSERT INTO `Account` VALUES ("A10003", "CNY", 15000);
INSERT INTO `Savings_Account` VALUES ("A10003", "CNY", 15000, 5);
INSERT INTO `Transaction` VALUES (10, 1000, NOW(), '2021-09-01', "A10001", "A10002");
INSERT INTO `Transaction` VALUES (100, 2500, NOW(), '2020-09-01', "A10002", "A10001");
INSERT INTO `Transaction` VALUES (20, 3000, NOW(), '2021-10-01', "A10002", "A10003");
INSERT INTO `Transaction` VALUES (2000, 35000, NOW(), '2021-06-01', "A10003", "A10002");
INSERT INTO `Transaction` VALUES (70, 3500, NOW(), '2021-05-04', "A10003", "A10001");
INSERT INTO `Customer_Account` VALUES (0, "A10001");
INSERT INTO `Customer_Account` VALUES (2, "A10002");
INSERT INTO `Customer_Account` VALUES (0, "A10003");
/*!40000 ALTER TABLE `Customer` ENABLE KEYS */;
-- UNLOCK TABLES;

INSERT INTO `Transaction` VALUES (14, 1000, NOW(), '2021-09-01', "A10001", "A10002"),
(11, 1000, NOW(), '2021-10-01', "A10001", "A10002"),
(12, 2000, NOW(), '2021-10-02', "A10002", "A10001"),
(13, 3000, NOW(), '2021-11-01', "A10001", "A10002");








# Create TABLE 'Account'
# Create TABLE 'Transaction'
# Create other TABLE...


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
