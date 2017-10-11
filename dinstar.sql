-- MySQL dump 10.16  Distrib 10.1.26-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: dinstar
-- ------------------------------------------------------
-- Server version	10.1.26-MariaDB-0+deb9u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `callhistory`
--

DROP TABLE IF EXISTS `callhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `callhistory` (
  `id` bigint(12) NOT NULL AUTO_INCREMENT,
  `gwname` varchar(45) DEFAULT NULL,
  `startdate` datetime DEFAULT NULL,
  `answerdate` datetime DEFAULT NULL,
  `calldirection` varchar(20) DEFAULT NULL,
  `source` varchar(20) DEFAULT NULL,
  `sourceip` varchar(15) DEFAULT NULL,
  `destination` varchar(20) DEFAULT NULL,
  `hangside` varchar(20) DEFAULT NULL,
  `reason` varchar(20) DEFAULT NULL,
  `duration` int(10) DEFAULT NULL,
  `rtpsend` int(10) DEFAULT NULL,
  `rtprecv` int(10) DEFAULT NULL,
  `rtplossrate` int(3) DEFAULT NULL,
  `jitter` int(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx1` (`startdate`,`calldirection`,`sourceip`,`destination`,`answerdate`,`source`,`gwname`),
  KEY `idx2` (`startdate`),
  KEY `idx3` (`destination`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `callhistory`
--

LOCK TABLES `callhistory` WRITE;
/*!40000 ALTER TABLE `callhistory` DISABLE KEYS */;
/*!40000 ALTER TABLE `callhistory` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-09-11 16:43:43
