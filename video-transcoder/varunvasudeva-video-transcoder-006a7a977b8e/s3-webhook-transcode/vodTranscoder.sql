-- MySQL dump 10.13  Distrib 8.0.30, for Linux (x86_64)
--
-- Host: localhost    Database: vodTranscoder
-- ------------------------------------------------------
-- Server version	8.0.30-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `s3transcoder`
--

DROP TABLE IF EXISTS `s3transcoder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `s3transcoder` (
  `dt` datetime DEFAULT NULL,
  `bucketname` varchar(50) DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
  `qc` tinyint(1) DEFAULT NULL,
  `isTranscoded` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `s3transcoder`
--

LOCK TABLES `s3transcoder` WRITE;
/*!40000 ALTER TABLE `s3transcoder` DISABLE KEYS */;
INSERT INTO `s3transcoder` VALUES ('2022-10-14 19:30:33','pti-octopus','pti-octopus/file_example_MP4_1920_18MG.mp4',0,0);
/*!40000 ALTER TABLE `s3transcoder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vodQC`
--

DROP TABLE IF EXISTS `vodQC`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vodQC` (
  `createdTime` datetime DEFAULT NULL,
  `filepath` varchar(100) DEFAULT NULL,
  `integritycheck` tinyint(1) DEFAULT NULL,
  `qccheck` tinyint(1) DEFAULT NULL,
  `lowresPath` varchar(100) DEFAULT NULL,
  `logfilePath` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vodQC`
--

LOCK TABLES `vodQC` WRITE;
/*!40000 ALTER TABLE `vodQC` DISABLE KEYS */;
/*!40000 ALTER TABLE `vodQC` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-10-14 19:35:42
