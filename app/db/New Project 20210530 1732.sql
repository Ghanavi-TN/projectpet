-- MySQL Administrator dump 1.4
--
-- ------------------------------------------------------
-- Server version	5.5.19


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


--
-- Create schema onlineexam
--

CREATE DATABASE IF NOT EXISTS onlineexam;
USE onlineexam;

--
-- Definition of table `quest`
--

DROP TABLE IF EXISTS `quest`;
CREATE TABLE `quest` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `qid` int(10) unsigned NOT NULL,
  `quest` longtext NOT NULL,
  `answer` longtext NOT NULL,
  `mark` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `quest`
--

/*!40000 ALTER TABLE `quest` DISABLE KEYS */;
/*!40000 ALTER TABLE `quest` ENABLE KEYS */;


--
-- Definition of table `result`
--

DROP TABLE IF EXISTS `result`;
CREATE TABLE `result` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `rollno` varchar(45) NOT NULL,
  `qid` int(10) unsigned NOT NULL,
  `mark` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `result`
--

/*!40000 ALTER TABLE `result` DISABLE KEYS */;
/*!40000 ALTER TABLE `result` ENABLE KEYS */;


--
-- Definition of table `student`
--

DROP TABLE IF EXISTS `student`;
CREATE TABLE `student` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `rollno` varchar(45) NOT NULL,
  `name` varchar(45) NOT NULL,
  `dept` varchar(45) NOT NULL,
  `sem` varchar(10) DEFAULT NULL,
  `mono` varchar(45) NOT NULL,
  `email` varchar(145) NOT NULL,
  `addr` varchar(255) NOT NULL,
  `pass` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `student`
--

/*!40000 ALTER TABLE `student` DISABLE KEYS */;
/*!40000 ALTER TABLE `student` ENABLE KEYS */;


--
-- Definition of table `student_upload`
--

DROP TABLE IF EXISTS `student_upload`;
CREATE TABLE `student_upload` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `rollno` varchar(45) NOT NULL,
  `qid` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `student_upload`
--

/*!40000 ALTER TABLE `student_upload` DISABLE KEYS */;
/*!40000 ALTER TABLE `student_upload` ENABLE KEYS */;




/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
