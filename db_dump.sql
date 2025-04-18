-- MySQL dump 10.13  Distrib 8.0.41, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: building
-- ------------------------------------------------------
-- Server version	8.0.41-0ubuntu0.24.04.1

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
-- Table structure for table `Attendance_attendance`
--

DROP TABLE IF EXISTS `Attendance_attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Attendance_attendance` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `device_id` varchar(255) DEFAULT NULL,
  `month` int DEFAULT NULL,
  `year` int DEFAULT NULL,
  `start_time` datetime(6) DEFAULT NULL,
  `pause_time` datetime(6) DEFAULT NULL,
  `resume_time` datetime(6) DEFAULT NULL,
  `stop_time` datetime(6) DEFAULT NULL,
  `total_hours` bigint NOT NULL,
  `user_id_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Attendance_attendance_user_id_id_2796c1a6_fk_Attendance_user_id` (`user_id_id`),
  CONSTRAINT `Attendance_attendance_user_id_id_2796c1a6_fk_Attendance_user_id` FOREIGN KEY (`user_id_id`) REFERENCES `Attendance_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Attendance_attendance`
--

LOCK TABLES `Attendance_attendance` WRITE;
/*!40000 ALTER TABLE `Attendance_attendance` DISABLE KEYS */;
/*!40000 ALTER TABLE `Attendance_attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Attendance_user`
--

DROP TABLE IF EXISTS `Attendance_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Attendance_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(150) NOT NULL,
  `role` varchar(10) NOT NULL,
  `location` varchar(255) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `latitude` varchar(255) DEFAULT NULL,
  `longitude` varchar(255) DEFAULT NULL,
  `email` varchar(254) NOT NULL,
  `profileStatus` varchar(255) DEFAULT NULL,
  `success` varchar(255) DEFAULT NULL,
  `mobile` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Attendance_user`
--

LOCK TABLES `Attendance_user` WRITE;
/*!40000 ALTER TABLE `Attendance_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `Attendance_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Kovais_attendance`
--

DROP TABLE IF EXISTS `Kovais_attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Kovais_attendance` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(255) NOT NULL,
  `latitude` varchar(255) DEFAULT NULL,
  `longitude` varchar(255) DEFAULT NULL,
  `check_in` datetime(6) DEFAULT NULL,
  `check_out` datetime(6) DEFAULT NULL,
  `employee_attendance_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Kovais_attendance_employee_attendance__44650cba_fk_Kovais_em` (`employee_attendance_id`),
  CONSTRAINT `Kovais_attendance_employee_attendance__44650cba_fk_Kovais_em` FOREIGN KEY (`employee_attendance_id`) REFERENCES `Kovais_employee` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Kovais_attendance`
--

LOCK TABLES `Kovais_attendance` WRITE;
/*!40000 ALTER TABLE `Kovais_attendance` DISABLE KEYS */;
/*!40000 ALTER TABLE `Kovais_attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Kovais_bonus`
--

DROP TABLE IF EXISTS `Kovais_bonus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Kovais_bonus` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `points` varchar(256) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `name_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Kovais_bonus_name_id_8c07ce4b_fk_Kovais_employee_id` (`name_id`),
  CONSTRAINT `Kovais_bonus_name_id_8c07ce4b_fk_Kovais_employee_id` FOREIGN KEY (`name_id`) REFERENCES `Kovais_employee` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Kovais_bonus`
--

LOCK TABLES `Kovais_bonus` WRITE;
/*!40000 ALTER TABLE `Kovais_bonus` DISABLE KEYS */;
/*!40000 ALTER TABLE `Kovais_bonus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Kovais_booking`
--

DROP TABLE IF EXISTS `Kovais_booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Kovais_booking` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `time_slot` datetime(6) NOT NULL,
  `bonus_id` bigint NOT NULL,
  `employee_id_id` bigint NOT NULL,
  `customer_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Kovais_booking_bonus_id_8f97bf69_fk_Kovais_bonus_id` (`bonus_id`),
  KEY `Kovais_booking_employee_id_id_6d046083_fk_Kovais_employee_id` (`employee_id_id`),
  KEY `Kovais_booking_customer_id_id_bb1aea5a_fk_Kovais_userdetails_id` (`customer_id_id`),
  CONSTRAINT `Kovais_booking_bonus_id_8f97bf69_fk_Kovais_bonus_id` FOREIGN KEY (`bonus_id`) REFERENCES `Kovais_bonus` (`id`),
  CONSTRAINT `Kovais_booking_customer_id_id_bb1aea5a_fk_Kovais_userdetails_id` FOREIGN KEY (`customer_id_id`) REFERENCES `Kovais_userdetails` (`id`),
  CONSTRAINT `Kovais_booking_employee_id_id_6d046083_fk_Kovais_employee_id` FOREIGN KEY (`employee_id_id`) REFERENCES `Kovais_employee` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Kovais_booking`
--

LOCK TABLES `Kovais_booking` WRITE;
/*!40000 ALTER TABLE `Kovais_booking` DISABLE KEYS */;
/*!40000 ALTER TABLE `Kovais_booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Kovais_employee`
--

DROP TABLE IF EXISTS `Kovais_employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Kovais_employee` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `role` varchar(10) NOT NULL,
  `mobile` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `attendance` varchar(15) DEFAULT NULL,
  `total_attendance` varchar(255) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `success` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Kovais_employee`
--

LOCK TABLES `Kovais_employee` WRITE;
/*!40000 ALTER TABLE `Kovais_employee` DISABLE KEYS */;
/*!40000 ALTER TABLE `Kovais_employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Kovais_employee_groups`
--

DROP TABLE IF EXISTS `Kovais_employee_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Kovais_employee_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `employee_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Kovais_employee_groups_employee_id_group_id_e7618792_uniq` (`employee_id`,`group_id`),
  KEY `Kovais_employee_groups_group_id_52ef16e3_fk_auth_group_id` (`group_id`),
  CONSTRAINT `Kovais_employee_grou_employee_id_214befb2_fk_Kovais_em` FOREIGN KEY (`employee_id`) REFERENCES `Kovais_employee` (`id`),
  CONSTRAINT `Kovais_employee_groups_group_id_52ef16e3_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Kovais_employee_groups`
--

LOCK TABLES `Kovais_employee_groups` WRITE;
/*!40000 ALTER TABLE `Kovais_employee_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `Kovais_employee_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Kovais_employee_user_permissions`
--

DROP TABLE IF EXISTS `Kovais_employee_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Kovais_employee_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `employee_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Kovais_employee_user_per_employee_id_permission_i_a33a7609_uniq` (`employee_id`,`permission_id`),
  KEY `Kovais_employee_user_permission_id_f54c2296_fk_auth_perm` (`permission_id`),
  CONSTRAINT `Kovais_employee_user_employee_id_b86b4b06_fk_Kovais_em` FOREIGN KEY (`employee_id`) REFERENCES `Kovais_employee` (`id`),
  CONSTRAINT `Kovais_employee_user_permission_id_f54c2296_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Kovais_employee_user_permissions`
--

LOCK TABLES `Kovais_employee_user_permissions` WRITE;
/*!40000 ALTER TABLE `Kovais_employee_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `Kovais_employee_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Kovais_gymorder`
--

DROP TABLE IF EXISTS `Kovais_gymorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Kovais_gymorder` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `gender` varchar(255) DEFAULT NULL,
  `age` varchar(255) DEFAULT NULL,
  `timeslot` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `plan` varchar(255) DEFAULT NULL,
  `attendance` varchar(255) DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
  `amount` longtext,
  `purchaseddate` longtext,
  `expiry_date` longtext,
  `payment_status` varchar(255) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `rating` double DEFAULT NULL,
  `comment` longtext,
  `employee_id_id` bigint DEFAULT NULL,
  `customer_id_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Kovais_gymorder_employee_id_id_72724cb3_fk_Kovais_employee_id` (`employee_id_id`),
  KEY `Kovais_gymorder_customer_id_id_f57163fe_fk_Kovais_userdetails_id` (`customer_id_id`),
  CONSTRAINT `Kovais_gymorder_customer_id_id_f57163fe_fk_Kovais_userdetails_id` FOREIGN KEY (`customer_id_id`) REFERENCES `Kovais_userdetails` (`id`),
  CONSTRAINT `Kovais_gymorder_employee_id_id_72724cb3_fk_Kovais_employee_id` FOREIGN KEY (`employee_id_id`) REFERENCES `Kovais_employee` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Kovais_gymorder`
--

LOCK TABLES `Kovais_gymorder` WRITE;
/*!40000 ALTER TABLE `Kovais_gymorder` DISABLE KEYS */;
/*!40000 ALTER TABLE `Kovais_gymorder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Kovais_hotelorder`
--

DROP TABLE IF EXISTS `Kovais_hotelorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Kovais_hotelorder` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `guest_name` varchar(255) DEFAULT NULL,
  `amount` varchar(255) DEFAULT NULL,
  `check_in` datetime(6) DEFAULT NULL,
  `check_out` datetime(6) DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
  `room_count` varchar(255) DEFAULT NULL,
  `guest_count` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `payment_status` varchar(255) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `rating` double DEFAULT NULL,
  `comment` longtext,
  `employee_id_id` bigint DEFAULT NULL,
  `customer_id_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Kovais_hotelorder_employee_id_id_93cf2831_fk_Kovais_employee_id` (`employee_id_id`),
  KEY `Kovais_hotelorder_customer_id_id_a653e439_fk_Kovais_us` (`customer_id_id`),
  CONSTRAINT `Kovais_hotelorder_customer_id_id_a653e439_fk_Kovais_us` FOREIGN KEY (`customer_id_id`) REFERENCES `Kovais_userdetails` (`id`),
  CONSTRAINT `Kovais_hotelorder_employee_id_id_93cf2831_fk_Kovais_employee_id` FOREIGN KEY (`employee_id_id`) REFERENCES `Kovais_employee` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Kovais_hotelorder`
--

LOCK TABLES `Kovais_hotelorder` WRITE;
/*!40000 ALTER TABLE `Kovais_hotelorder` DISABLE KEYS */;
/*!40000 ALTER TABLE `Kovais_hotelorder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Kovais_review`
--

DROP TABLE IF EXISTS `Kovais_review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Kovais_review` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `rating` double NOT NULL,
  `comment` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `customer_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Kovais_review_customer_id_id_fb8c67ff_fk_Kovais_userdetails_id` (`customer_id_id`),
  CONSTRAINT `Kovais_review_customer_id_id_fb8c67ff_fk_Kovais_userdetails_id` FOREIGN KEY (`customer_id_id`) REFERENCES `Kovais_userdetails` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Kovais_review`
--

LOCK TABLES `Kovais_review` WRITE;
/*!40000 ALTER TABLE `Kovais_review` DISABLE KEYS */;
/*!40000 ALTER TABLE `Kovais_review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Kovais_rooms`
--

DROP TABLE IF EXISTS `Kovais_rooms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Kovais_rooms` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `room` int DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `room` (`room`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Kovais_rooms`
--

LOCK TABLES `Kovais_rooms` WRITE;
/*!40000 ALTER TABLE `Kovais_rooms` DISABLE KEYS */;
/*!40000 ALTER TABLE `Kovais_rooms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Kovais_saloonorder`
--

DROP TABLE IF EXISTS `Kovais_saloonorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Kovais_saloonorder` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_type` varchar(255) DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
  `services` longtext,
  `payment_status` varchar(255) DEFAULT NULL,
  `payment_type` varchar(255) DEFAULT NULL,
  `amount` varchar(255) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `time` varchar(255) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `status` varchar(255) DEFAULT NULL,
  `rating` double DEFAULT NULL,
  `comment` longtext,
  `employee_id_id` bigint DEFAULT NULL,
  `customer_id_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Kovais_saloonorder_employee_id_id_df896b4c_fk_Kovais_employee_id` (`employee_id_id`),
  KEY `Kovais_saloonorder_customer_id_id_e3d711b5_fk_Kovais_us` (`customer_id_id`),
  CONSTRAINT `Kovais_saloonorder_customer_id_id_e3d711b5_fk_Kovais_us` FOREIGN KEY (`customer_id_id`) REFERENCES `Kovais_userdetails` (`id`),
  CONSTRAINT `Kovais_saloonorder_employee_id_id_df896b4c_fk_Kovais_employee_id` FOREIGN KEY (`employee_id_id`) REFERENCES `Kovais_employee` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Kovais_saloonorder`
--

LOCK TABLES `Kovais_saloonorder` WRITE;
/*!40000 ALTER TABLE `Kovais_saloonorder` DISABLE KEYS */;
INSERT INTO `Kovais_saloonorder` VALUES (1,NULL,NULL,NULL,'pending',NULL,NULL,NULL,NULL,'2025-04-17 05:45:25.779508',NULL,NULL,NULL,NULL,1),(2,NULL,NULL,NULL,'pending',NULL,NULL,NULL,NULL,'2025-04-17 05:46:14.871921',NULL,NULL,NULL,NULL,1);
/*!40000 ALTER TABLE `Kovais_saloonorder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Kovais_spaorder`
--

DROP TABLE IF EXISTS `Kovais_spaorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Kovais_spaorder` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `category` varchar(255) DEFAULT NULL,
  `services` longtext,
  `date` date DEFAULT NULL,
  `time` varchar(255) DEFAULT NULL,
  `amount` longtext,
  `payment_status` varchar(255) DEFAULT NULL,
  `payment_type` varchar(255) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `status` varchar(255) DEFAULT NULL,
  `rating` double DEFAULT NULL,
  `comment` longtext,
  `employee_id_id` bigint DEFAULT NULL,
  `customer_id_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Kovais_spaorder_employee_id_id_db613078_fk_Kovais_employee_id` (`employee_id_id`),
  KEY `Kovais_spaorder_customer_id_id_891c49e8_fk_Kovais_userdetails_id` (`customer_id_id`),
  CONSTRAINT `Kovais_spaorder_customer_id_id_891c49e8_fk_Kovais_userdetails_id` FOREIGN KEY (`customer_id_id`) REFERENCES `Kovais_userdetails` (`id`),
  CONSTRAINT `Kovais_spaorder_employee_id_id_db613078_fk_Kovais_employee_id` FOREIGN KEY (`employee_id_id`) REFERENCES `Kovais_employee` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Kovais_spaorder`
--

LOCK TABLES `Kovais_spaorder` WRITE;
/*!40000 ALTER TABLE `Kovais_spaorder` DISABLE KEYS */;
/*!40000 ALTER TABLE `Kovais_spaorder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Kovais_task`
--

DROP TABLE IF EXISTS `Kovais_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Kovais_task` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `assigned_to` varchar(255) DEFAULT NULL,
  `description` longtext NOT NULL,
  `status` varchar(255) DEFAULT NULL,
  `employee_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Kovais_task_employee_id_684e4f3a_fk_Kovais_employee_id` (`employee_id`),
  CONSTRAINT `Kovais_task_employee_id_684e4f3a_fk_Kovais_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `Kovais_employee` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Kovais_task`
--

LOCK TABLES `Kovais_task` WRITE;
/*!40000 ALTER TABLE `Kovais_task` DISABLE KEYS */;
/*!40000 ALTER TABLE `Kovais_task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Kovais_userdetails`
--

DROP TABLE IF EXISTS `Kovais_userdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Kovais_userdetails` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(256) DEFAULT NULL,
  `membership` varchar(20) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `subscribed` tinyint(1) DEFAULT NULL,
  `premium_amount` varchar(255) DEFAULT NULL,
  `emblem_url` varchar(500) DEFAULT NULL,
  `points` int NOT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `address` longtext,
  `aadhar` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Kovais_userdetails`
--

LOCK TABLES `Kovais_userdetails` WRITE;
/*!40000 ALTER TABLE `Kovais_userdetails` DISABLE KEYS */;
INSERT INTO `Kovais_userdetails` VALUES (1,'nitish','silver','pbkdf2_sha256$870000$T0xGhJyE8eHCjoutZ4pMOE$tuPO25fpzMf+9yyBPOh7+4WXgLtZPfR+1QPM2tIW+bw=',0,NULL,'https://i.postimg.cc/65jSL6gp/pngtree-champion-silver-award-medals-ribbons-png-image-6563618.png',200,NULL,NULL,'');
/*!40000 ALTER TABLE `Kovais_userdetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_banner`
--

DROP TABLE IF EXISTS `app_banner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_banner` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_banner`
--

LOCK TABLES `app_banner` WRITE;
/*!40000 ALTER TABLE `app_banner` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_banner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_landlisting`
--

DROP TABLE IF EXISTS `app_landlisting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_landlisting` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `detail_description` longtext NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `district_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_landlisting_district_id_c32b6d1b_fk_app_locationexample_id` (`district_id`),
  CONSTRAINT `app_landlisting_district_id_c32b6d1b_fk_app_locationexample_id` FOREIGN KEY (`district_id`) REFERENCES `app_locationexample` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_landlisting`
--

LOCK TABLES `app_landlisting` WRITE;
/*!40000 ALTER TABLE `app_landlisting` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_landlisting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_locationexample`
--

DROP TABLE IF EXISTS `app_locationexample`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_locationexample` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `country` varchar(20) NOT NULL,
  `state` varchar(20) NOT NULL,
  `district` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_locationexample`
--

LOCK TABLES `app_locationexample` WRITE;
/*!40000 ALTER TABLE `app_locationexample` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_locationexample` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_property`
--

DROP TABLE IF EXISTS `app_property`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_property` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `contact_number` varchar(15) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_property`
--

LOCK TABLES `app_property` WRITE;
/*!40000 ALTER TABLE `app_property` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_property` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=281 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add customer',7,'add_customer'),(26,'Can change customer',7,'change_customer'),(27,'Can delete customer',7,'delete_customer'),(28,'Can view customer',7,'view_customer'),(29,'Can add item list',8,'add_itemlist'),(30,'Can change item list',8,'change_itemlist'),(31,'Can delete item list',8,'delete_itemlist'),(32,'Can view item list',8,'view_itemlist'),(33,'Can add user',9,'add_customuser'),(34,'Can change user',9,'change_customuser'),(35,'Can delete user',9,'delete_customuser'),(36,'Can view user',9,'view_customuser'),(37,'Can add plan',10,'add_plan'),(38,'Can change plan',10,'change_plan'),(39,'Can delete plan',10,'delete_plan'),(40,'Can view plan',10,'view_plan'),(41,'Can add marker',11,'add_marker'),(42,'Can change marker',11,'change_marker'),(43,'Can delete marker',11,'delete_marker'),(44,'Can view marker',11,'view_marker'),(45,'Can add location',12,'add_location'),(46,'Can change location',12,'change_location'),(47,'Can delete location',12,'delete_location'),(48,'Can view location',12,'view_location'),(49,'Can add post',13,'add_post'),(50,'Can change post',13,'change_post'),(51,'Can delete post',13,'delete_post'),(52,'Can view post',13,'view_post'),(53,'Can add save json',14,'add_savejson'),(54,'Can change save json',14,'change_savejson'),(55,'Can delete save json',14,'delete_savejson'),(56,'Can view save json',14,'view_savejson'),(57,'Can add video upload',15,'add_videoupload'),(58,'Can change video upload',15,'change_videoupload'),(59,'Can delete video upload',15,'delete_videoupload'),(60,'Can view video upload',15,'view_videoupload'),(61,'Can add video frame',16,'add_videoframe'),(62,'Can change video frame',16,'change_videoframe'),(63,'Can delete video frame',16,'delete_videoframe'),(64,'Can view video frame',16,'view_videoframe'),(65,'Can add rooms',17,'add_rooms'),(66,'Can change rooms',17,'change_rooms'),(67,'Can delete rooms',17,'delete_rooms'),(68,'Can view rooms',17,'view_rooms'),(69,'Can add user details',18,'add_userdetails'),(70,'Can change user details',18,'change_userdetails'),(71,'Can delete user details',18,'delete_userdetails'),(72,'Can view user details',18,'view_userdetails'),(73,'Can add user',19,'add_employee'),(74,'Can change user',19,'change_employee'),(75,'Can delete user',19,'delete_employee'),(76,'Can view user',19,'view_employee'),(77,'Can add bonus',20,'add_bonus'),(78,'Can change bonus',20,'change_bonus'),(79,'Can delete bonus',20,'delete_bonus'),(80,'Can view bonus',20,'view_bonus'),(81,'Can add attendance',21,'add_attendance'),(82,'Can change attendance',21,'change_attendance'),(83,'Can delete attendance',21,'delete_attendance'),(84,'Can view attendance',21,'view_attendance'),(85,'Can add task',22,'add_task'),(86,'Can change task',22,'change_task'),(87,'Can delete task',22,'delete_task'),(88,'Can view task',22,'view_task'),(89,'Can add spa order',23,'add_spaorder'),(90,'Can change spa order',23,'change_spaorder'),(91,'Can delete spa order',23,'delete_spaorder'),(92,'Can view spa order',23,'view_spaorder'),(93,'Can add saloon order',24,'add_saloonorder'),(94,'Can change saloon order',24,'change_saloonorder'),(95,'Can delete saloon order',24,'delete_saloonorder'),(96,'Can view saloon order',24,'view_saloonorder'),(97,'Can add review',25,'add_review'),(98,'Can change review',25,'change_review'),(99,'Can delete review',25,'delete_review'),(100,'Can view review',25,'view_review'),(101,'Can add hotel order',26,'add_hotelorder'),(102,'Can change hotel order',26,'change_hotelorder'),(103,'Can delete hotel order',26,'delete_hotelorder'),(104,'Can view hotel order',26,'view_hotelorder'),(105,'Can add gym order',27,'add_gymorder'),(106,'Can change gym order',27,'change_gymorder'),(107,'Can delete gym order',27,'delete_gymorder'),(108,'Can view gym order',27,'view_gymorder'),(109,'Can add booking',28,'add_booking'),(110,'Can change booking',28,'change_booking'),(111,'Can delete booking',28,'delete_booking'),(112,'Can view booking',28,'view_booking'),(113,'Can add category',29,'add_category'),(114,'Can change category',29,'change_category'),(115,'Can delete category',29,'delete_category'),(116,'Can view category',29,'view_category'),(117,'Can add user',30,'add_customer'),(118,'Can change user',30,'change_customer'),(119,'Can delete user',30,'delete_customer'),(120,'Can view user',30,'view_customer'),(121,'Can add cart',31,'add_cart'),(122,'Can change cart',31,'change_cart'),(123,'Can delete cart',31,'delete_cart'),(124,'Can view cart',31,'view_cart'),(125,'Can add banner',32,'add_banner'),(126,'Can change banner',32,'change_banner'),(127,'Can delete banner',32,'delete_banner'),(128,'Can view banner',32,'view_banner'),(129,'Can add address',33,'add_address'),(130,'Can change address',33,'change_address'),(131,'Can delete address',33,'delete_address'),(132,'Can view address',33,'view_address'),(133,'Can add delivery partner',34,'add_deliverypartner'),(134,'Can change delivery partner',34,'change_deliverypartner'),(135,'Can delete delivery partner',34,'delete_deliverypartner'),(136,'Can view delivery partner',34,'view_deliverypartner'),(137,'Can add notification',35,'add_notification'),(138,'Can change notification',35,'change_notification'),(139,'Can delete notification',35,'delete_notification'),(140,'Can view notification',35,'view_notification'),(141,'Can add order',36,'add_order'),(142,'Can change order',36,'change_order'),(143,'Can delete order',36,'delete_order'),(144,'Can view order',36,'view_order'),(145,'Can add order tracking',37,'add_ordertracking'),(146,'Can change order tracking',37,'change_ordertracking'),(147,'Can delete order tracking',37,'delete_ordertracking'),(148,'Can view order tracking',37,'view_ordertracking'),(149,'Can add payment',38,'add_payment'),(150,'Can change payment',38,'change_payment'),(151,'Can delete payment',38,'delete_payment'),(152,'Can view payment',38,'view_payment'),(153,'Can add product',39,'add_product'),(154,'Can change product',39,'change_product'),(155,'Can delete product',39,'delete_product'),(156,'Can view product',39,'view_product'),(157,'Can add product image',40,'add_productimage'),(158,'Can change product image',40,'change_productimage'),(159,'Can delete product image',40,'delete_productimage'),(160,'Can view product image',40,'view_productimage'),(161,'Can add product variation',41,'add_productvariation'),(162,'Can change product variation',41,'change_productvariation'),(163,'Can delete product variation',41,'delete_productvariation'),(164,'Can view product variation',41,'view_productvariation'),(165,'Can add order item',42,'add_orderitem'),(166,'Can change order item',42,'change_orderitem'),(167,'Can delete order item',42,'delete_orderitem'),(168,'Can view order item',42,'view_orderitem'),(169,'Can add cart item',43,'add_cartitem'),(170,'Can change cart item',43,'change_cartitem'),(171,'Can delete cart item',43,'delete_cartitem'),(172,'Can view cart item',43,'view_cartitem'),(173,'Can add profile',44,'add_profile'),(174,'Can change profile',44,'change_profile'),(175,'Can delete profile',44,'delete_profile'),(176,'Can view profile',44,'view_profile'),(177,'Can add review',45,'add_review'),(178,'Can change review',45,'change_review'),(179,'Can delete review',45,'delete_review'),(180,'Can view review',45,'view_review'),(181,'Can add subcategory',46,'add_subcategory'),(182,'Can change subcategory',46,'change_subcategory'),(183,'Can delete subcategory',46,'delete_subcategory'),(184,'Can view subcategory',46,'view_subcategory'),(185,'Can add wishlist',47,'add_wishlist'),(186,'Can change wishlist',47,'change_wishlist'),(187,'Can delete wishlist',47,'delete_wishlist'),(188,'Can view wishlist',47,'view_wishlist'),(189,'Can add banner',48,'add_banner'),(190,'Can change banner',48,'change_banner'),(191,'Can delete banner',48,'delete_banner'),(192,'Can view banner',48,'view_banner'),(193,'Can add location example',49,'add_locationexample'),(194,'Can change location example',49,'change_locationexample'),(195,'Can delete location example',49,'delete_locationexample'),(196,'Can view location example',49,'view_locationexample'),(197,'Can add property',50,'add_property'),(198,'Can change property',50,'change_property'),(199,'Can delete property',50,'delete_property'),(200,'Can view property',50,'view_property'),(201,'Can add land listing',51,'add_landlisting'),(202,'Can change land listing',51,'change_landlisting'),(203,'Can delete land listing',51,'delete_landlisting'),(204,'Can view land listing',51,'view_landlisting'),(205,'Can add accessories',52,'add_accessories'),(206,'Can change accessories',52,'change_accessories'),(207,'Can delete accessories',52,'delete_accessories'),(208,'Can view accessories',52,'view_accessories'),(209,'Can add banner',53,'add_banner'),(210,'Can change banner',53,'change_banner'),(211,'Can delete banner',53,'delete_banner'),(212,'Can view banner',53,'view_banner'),(213,'Can add category',54,'add_category'),(214,'Can change category',54,'change_category'),(215,'Can delete category',54,'delete_category'),(216,'Can view category',54,'view_category'),(217,'Can add contact',55,'add_contact'),(218,'Can change contact',55,'change_contact'),(219,'Can delete contact',55,'delete_contact'),(220,'Can view contact',55,'view_contact'),(221,'Can add customer',56,'add_customer'),(222,'Can change customer',56,'change_customer'),(223,'Can delete customer',56,'delete_customer'),(224,'Can view customer',56,'view_customer'),(225,'Can add user',57,'add_userprofile'),(226,'Can change user',57,'change_userprofile'),(227,'Can delete user',57,'delete_userprofile'),(228,'Can view user',57,'view_userprofile'),(229,'Can add items',58,'add_items'),(230,'Can change items',58,'change_items'),(231,'Can delete items',58,'delete_items'),(232,'Can view items',58,'view_items'),(233,'Can add order',59,'add_order'),(234,'Can change order',59,'change_order'),(235,'Can delete order',59,'delete_order'),(236,'Can view order',59,'view_order'),(237,'Can add products',60,'add_products'),(238,'Can change products',60,'change_products'),(239,'Can delete products',60,'delete_products'),(240,'Can view products',60,'view_products'),(241,'Can add wish',61,'add_wish'),(242,'Can change wish',61,'change_wish'),(243,'Can delete wish',61,'delete_wish'),(244,'Can view wish',61,'view_wish'),(245,'Can add user',62,'add_user'),(246,'Can change user',62,'change_user'),(247,'Can delete user',62,'delete_user'),(248,'Can view user',62,'view_user'),(249,'Can add attendance',63,'add_attendance'),(250,'Can change attendance',63,'change_attendance'),(251,'Can delete attendance',63,'delete_attendance'),(252,'Can view attendance',63,'view_attendance'),(253,'Can add organization',64,'add_organization'),(254,'Can change organization',64,'change_organization'),(255,'Can delete organization',64,'delete_organization'),(256,'Can view organization',64,'view_organization'),(257,'Can add user',65,'add_employee'),(258,'Can change user',65,'change_employee'),(259,'Can delete user',65,'delete_employee'),(260,'Can view user',65,'view_employee'),(261,'Can add device',66,'add_device'),(262,'Can change device',66,'change_device'),(263,'Can delete device',66,'delete_device'),(264,'Can view device',66,'view_device'),(265,'Can add attendance',67,'add_attendance'),(266,'Can change attendance',67,'change_attendance'),(267,'Can delete attendance',67,'delete_attendance'),(268,'Can view attendance',67,'view_attendance'),(269,'Can add user',68,'add_customuser'),(270,'Can change user',68,'change_customuser'),(271,'Can delete user',68,'delete_customuser'),(272,'Can view user',68,'view_customuser'),(273,'Can add device',69,'add_device'),(274,'Can change device',69,'change_device'),(275,'Can delete device',69,'delete_device'),(276,'Can view device',69,'view_device'),(277,'Can add gps data',70,'add_gpsdata'),(278,'Can change gps data',70,'change_gpsdata'),(279,'Can delete gps data',70,'delete_gpsdata'),(280,'Can view gps data',70,'view_gpsdata');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$870000$DeOXi4ok07lITqM05d4EXG$3dhbsFsjL6BCqs2NwE5bd5YFYejxkmVOFrQB4O+bDsA=','2025-04-17 05:46:13.595557',1,'admin','','','',1,1,'2025-04-17 05:46:03.340897');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bike_accessories`
--

DROP TABLE IF EXISTS `bike_accessories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bike_accessories` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `image` varchar(256) DEFAULT NULL,
  `Product_reference_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bike_accessories_Product_reference_id_4e7b59ed_fk_bike_prod` (`Product_reference_id`),
  CONSTRAINT `bike_accessories_Product_reference_id_4e7b59ed_fk_bike_prod` FOREIGN KEY (`Product_reference_id`) REFERENCES `bike_products` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bike_accessories`
--

LOCK TABLES `bike_accessories` WRITE;
/*!40000 ALTER TABLE `bike_accessories` DISABLE KEYS */;
/*!40000 ALTER TABLE `bike_accessories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bike_banner`
--

DROP TABLE IF EXISTS `bike_banner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bike_banner` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bike_banner`
--

LOCK TABLES `bike_banner` WRITE;
/*!40000 ALTER TABLE `bike_banner` DISABLE KEYS */;
/*!40000 ALTER TABLE `bike_banner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bike_category`
--

DROP TABLE IF EXISTS `bike_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bike_category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bike_category`
--

LOCK TABLES `bike_category` WRITE;
/*!40000 ALTER TABLE `bike_category` DISABLE KEYS */;
/*!40000 ALTER TABLE `bike_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bike_contact`
--

DROP TABLE IF EXISTS `bike_contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bike_contact` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(254) NOT NULL,
  `subject` longtext,
  `description` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bike_contact`
--

LOCK TABLES `bike_contact` WRITE;
/*!40000 ALTER TABLE `bike_contact` DISABLE KEYS */;
/*!40000 ALTER TABLE `bike_contact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bike_customer`
--

DROP TABLE IF EXISTS `bike_customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bike_customer` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `address` longtext NOT NULL,
  `city` varchar(50) NOT NULL,
  `pincode` varchar(10) NOT NULL,
  `state` varchar(2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bike_customer`
--

LOCK TABLES `bike_customer` WRITE;
/*!40000 ALTER TABLE `bike_customer` DISABLE KEYS */;
/*!40000 ALTER TABLE `bike_customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bike_items`
--

DROP TABLE IF EXISTS `bike_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bike_items` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `price` longtext,
  `description` longtext,
  `stock` varchar(255) DEFAULT NULL,
  `Accessories_reference_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bike_items_Accessories_referenc_1c949932_fk_bike_acce` (`Accessories_reference_id`),
  CONSTRAINT `bike_items_Accessories_referenc_1c949932_fk_bike_acce` FOREIGN KEY (`Accessories_reference_id`) REFERENCES `bike_accessories` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bike_items`
--

LOCK TABLES `bike_items` WRITE;
/*!40000 ALTER TABLE `bike_items` DISABLE KEYS */;
/*!40000 ALTER TABLE `bike_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bike_order`
--

DROP TABLE IF EXISTS `bike_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bike_order` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `address` longtext NOT NULL,
  `wishlist_items` json DEFAULT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `order_status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `bike_order_user_id_18d8481c_fk_bike_userprofile_id` (`user_id`),
  CONSTRAINT `bike_order_user_id_18d8481c_fk_bike_userprofile_id` FOREIGN KEY (`user_id`) REFERENCES `bike_userprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bike_order`
--

LOCK TABLES `bike_order` WRITE;
/*!40000 ALTER TABLE `bike_order` DISABLE KEYS */;
/*!40000 ALTER TABLE `bike_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bike_products`
--

DROP TABLE IF EXISTS `bike_products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bike_products` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `Category_reference_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bike_products_Category_reference_id_1479672c_fk_bike_category_id` (`Category_reference_id`),
  CONSTRAINT `bike_products_Category_reference_id_1479672c_fk_bike_category_id` FOREIGN KEY (`Category_reference_id`) REFERENCES `bike_category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bike_products`
--

LOCK TABLES `bike_products` WRITE;
/*!40000 ALTER TABLE `bike_products` DISABLE KEYS */;
/*!40000 ALTER TABLE `bike_products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bike_userprofile`
--

DROP TABLE IF EXISTS `bike_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bike_userprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bike_userprofile`
--

LOCK TABLES `bike_userprofile` WRITE;
/*!40000 ALTER TABLE `bike_userprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `bike_userprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bike_userprofile_groups`
--

DROP TABLE IF EXISTS `bike_userprofile_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bike_userprofile_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `userprofile_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `bike_userprofile_groups_userprofile_id_group_id_eafd7e98_uniq` (`userprofile_id`,`group_id`),
  KEY `bike_userprofile_groups_group_id_afdcd049_fk_auth_group_id` (`group_id`),
  CONSTRAINT `bike_userprofile_gro_userprofile_id_9502cb84_fk_bike_user` FOREIGN KEY (`userprofile_id`) REFERENCES `bike_userprofile` (`id`),
  CONSTRAINT `bike_userprofile_groups_group_id_afdcd049_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bike_userprofile_groups`
--

LOCK TABLES `bike_userprofile_groups` WRITE;
/*!40000 ALTER TABLE `bike_userprofile_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `bike_userprofile_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bike_userprofile_user_permissions`
--

DROP TABLE IF EXISTS `bike_userprofile_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bike_userprofile_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `userprofile_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `bike_userprofile_user_pe_userprofile_id_permissio_1c57e164_uniq` (`userprofile_id`,`permission_id`),
  KEY `bike_userprofile_use_permission_id_1f2a6127_fk_auth_perm` (`permission_id`),
  CONSTRAINT `bike_userprofile_use_permission_id_1f2a6127_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `bike_userprofile_use_userprofile_id_46c74bd6_fk_bike_user` FOREIGN KEY (`userprofile_id`) REFERENCES `bike_userprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bike_userprofile_user_permissions`
--

LOCK TABLES `bike_userprofile_user_permissions` WRITE;
/*!40000 ALTER TABLE `bike_userprofile_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `bike_userprofile_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bike_wish`
--

DROP TABLE IF EXISTS `bike_wish`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bike_wish` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) DEFAULT NULL,
  `name` longtext,
  `price` decimal(10,2) DEFAULT NULL,
  `quantity` int unsigned NOT NULL,
  `added_at` datetime(6) NOT NULL,
  `gst` decimal(5,2) NOT NULL,
  `shipping_charge` decimal(10,2) NOT NULL,
  `item_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bike_wish_item_id_c21f7239_fk_bike_items_id` (`item_id`),
  KEY `bike_wish_user_id_47c7081b_fk_bike_userprofile_id` (`user_id`),
  CONSTRAINT `bike_wish_item_id_c21f7239_fk_bike_items_id` FOREIGN KEY (`item_id`) REFERENCES `bike_items` (`id`),
  CONSTRAINT `bike_wish_user_id_47c7081b_fk_bike_userprofile_id` FOREIGN KEY (`user_id`) REFERENCES `bike_userprofile` (`id`),
  CONSTRAINT `bike_wish_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bike_wish`
--

LOCK TABLES `bike_wish` WRITE;
/*!40000 ALTER TABLE `bike_wish` DISABLE KEYS */;
/*!40000 ALTER TABLE `bike_wish` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(48,'app','banner'),(51,'app','landlisting'),(49,'app','locationexample'),(50,'app','property'),(63,'Attendance','attendance'),(62,'Attendance','user'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(52,'bike','accessories'),(53,'bike','banner'),(54,'bike','category'),(55,'bike','contact'),(56,'bike','customer'),(58,'bike','items'),(59,'bike','order'),(60,'bike','products'),(57,'bike','userprofile'),(61,'bike','wish'),(5,'contenttypes','contenttype'),(33,'ecomapp','address'),(32,'ecomapp','banner'),(31,'ecomapp','cart'),(43,'ecomapp','cartitem'),(29,'ecomapp','category'),(30,'ecomapp','customer'),(34,'ecomapp','deliverypartner'),(35,'ecomapp','notification'),(36,'ecomapp','order'),(42,'ecomapp','orderitem'),(37,'ecomapp','ordertracking'),(38,'ecomapp','payment'),(39,'ecomapp','product'),(40,'ecomapp','productimage'),(41,'ecomapp','productvariation'),(44,'ecomapp','profile'),(45,'ecomapp','review'),(46,'ecomapp','subcategory'),(47,'ecomapp','wishlist'),(68,'gateway','customuser'),(69,'gateway','device'),(70,'gateway','gpsdata'),(21,'Kovais','attendance'),(20,'Kovais','bonus'),(28,'Kovais','booking'),(19,'Kovais','employee'),(27,'Kovais','gymorder'),(26,'Kovais','hotelorder'),(25,'Kovais','review'),(17,'Kovais','rooms'),(24,'Kovais','saloonorder'),(23,'Kovais','spaorder'),(22,'Kovais','task'),(18,'Kovais','userdetails'),(67,'officeapp','attendance'),(66,'officeapp','device'),(65,'officeapp','employee'),(64,'officeapp','organization'),(7,'profile_utility','customer'),(9,'profile_utility','customuser'),(8,'profile_utility','itemlist'),(12,'profile_utility','location'),(11,'profile_utility','marker'),(10,'profile_utility','plan'),(13,'profile_utility','post'),(14,'profile_utility','savejson'),(16,'profile_utility','videoframe'),(15,'profile_utility','videoupload'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'Attendance','0001_initial','2025-04-17 05:41:05.053802'),(2,'contenttypes','0001_initial','2025-04-17 05:41:05.354076'),(3,'contenttypes','0002_remove_content_type_name','2025-04-17 05:41:05.762275'),(4,'auth','0001_initial','2025-04-17 05:41:07.914125'),(5,'auth','0002_alter_permission_name_max_length','2025-04-17 05:41:08.016985'),(6,'auth','0003_alter_user_email_max_length','2025-04-17 05:41:08.119262'),(7,'auth','0004_alter_user_username_opts','2025-04-17 05:41:08.136576'),(8,'auth','0005_alter_user_last_login_null','2025-04-17 05:41:08.221533'),(9,'auth','0006_require_contenttypes_0002','2025-04-17 05:41:08.230816'),(10,'auth','0007_alter_validators_add_error_messages','2025-04-17 05:41:08.246642'),(11,'auth','0008_alter_user_username_max_length','2025-04-17 05:41:08.851823'),(12,'auth','0009_alter_user_last_name_max_length','2025-04-17 05:41:08.937980'),(13,'auth','0010_alter_group_name_max_length','2025-04-17 05:41:09.334902'),(14,'auth','0011_update_proxy_permissions','2025-04-17 05:41:09.369024'),(15,'auth','0012_alter_user_first_name_max_length','2025-04-17 05:41:09.757523'),(16,'Kovais','0001_initial','2025-04-17 05:41:16.208718'),(17,'admin','0001_initial','2025-04-17 05:41:18.360140'),(18,'admin','0002_logentry_remove_auto_add','2025-04-17 05:41:18.384492'),(19,'admin','0003_logentry_add_action_flag_choices','2025-04-17 05:41:18.469703'),(20,'app','0001_initial','2025-04-17 05:41:19.178553'),(21,'bike','0001_initial','2025-04-17 05:41:22.353102'),(22,'bike','0002_alter_order_user_alter_wish_user','2025-04-17 05:41:23.991627'),(23,'ecomapp','0001_initial','2025-04-17 05:41:34.041836'),(24,'gateway','0001_initial','2025-04-17 05:41:36.792434'),(25,'officeapp','0001_initial','2025-04-17 05:41:40.682463'),(26,'profile_utility','0001_initial','2025-04-17 05:41:50.108889'),(27,'sessions','0001_initial','2025-04-17 05:41:50.310193');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('cel2o79rolabaxtkk4sv2hgsvrkmx3o0','.eJxVjEEOwiAQRe_C2pAOSEGX7nsGMjAzUjU0Ke3KeHfbpAvd_vfef6uI61Li2niOI6mrAnX63RLmJ9cd0APrfdJ5qss8Jr0r-qBNDxPx63a4fwcFW9lqa1C4Z88dQRZryElAC3ImMRJykOSduUjogPsNJJu8OASmYIxPBOrzBQsaOMY:1u5I4j:Ypi-hTs19Q5esRNe7e_xvzAbhwWj2dsqFpcJ4Hue_yI','2025-05-01 05:46:13.605890');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecomapp_address`
--

DROP TABLE IF EXISTS `ecomapp_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecomapp_address` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `full_name` varchar(255) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `address_line_1` varchar(255) NOT NULL,
  `address_line_2` varchar(255) NOT NULL,
  `city` varchar(100) NOT NULL,
  `state` varchar(100) NOT NULL,
  `country` varchar(100) NOT NULL,
  `postal_code` varchar(10) NOT NULL,
  `is_default` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ecomapp_address_user_id_b04c4c8d_fk_ecomapp_customer_id` (`user_id`),
  CONSTRAINT `ecomapp_address_user_id_b04c4c8d_fk_ecomapp_customer_id` FOREIGN KEY (`user_id`) REFERENCES `ecomapp_customer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecomapp_address`
--

LOCK TABLES `ecomapp_address` WRITE;
/*!40000 ALTER TABLE `ecomapp_address` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecomapp_address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecomapp_banner`
--

DROP TABLE IF EXISTS `ecomapp_banner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecomapp_banner` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `image` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `prize_offer` varchar(255) NOT NULL,
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `shopkeeper_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ecomapp_banner_shopkeeper_id_44929b92_fk_ecomapp_customer_id` (`shopkeeper_id`),
  CONSTRAINT `ecomapp_banner_shopkeeper_id_44929b92_fk_ecomapp_customer_id` FOREIGN KEY (`shopkeeper_id`) REFERENCES `ecomapp_customer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecomapp_banner`
--

LOCK TABLES `ecomapp_banner` WRITE;
/*!40000 ALTER TABLE `ecomapp_banner` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecomapp_banner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecomapp_cart`
--

DROP TABLE IF EXISTS `ecomapp_cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecomapp_cart` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ecomapp_cart_user_id_1761241a_fk_ecomapp_customer_id` (`user_id`),
  CONSTRAINT `ecomapp_cart_user_id_1761241a_fk_ecomapp_customer_id` FOREIGN KEY (`user_id`) REFERENCES `ecomapp_customer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecomapp_cart`
--

LOCK TABLES `ecomapp_cart` WRITE;
/*!40000 ALTER TABLE `ecomapp_cart` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecomapp_cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecomapp_cartitem`
--

DROP TABLE IF EXISTS `ecomapp_cartitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecomapp_cartitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int unsigned NOT NULL,
  `cart_id` bigint NOT NULL,
  `product_variation_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ecomapp_cartitem_cart_id_2357df83_fk_ecomapp_cart_id` (`cart_id`),
  KEY `ecomapp_cartitem_product_variation_id_53b6e837_fk_ecomapp_p` (`product_variation_id`),
  CONSTRAINT `ecomapp_cartitem_cart_id_2357df83_fk_ecomapp_cart_id` FOREIGN KEY (`cart_id`) REFERENCES `ecomapp_cart` (`id`),
  CONSTRAINT `ecomapp_cartitem_product_variation_id_53b6e837_fk_ecomapp_p` FOREIGN KEY (`product_variation_id`) REFERENCES `ecomapp_productvariation` (`id`),
  CONSTRAINT `ecomapp_cartitem_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecomapp_cartitem`
--

LOCK TABLES `ecomapp_cartitem` WRITE;
/*!40000 ALTER TABLE `ecomapp_cartitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecomapp_cartitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecomapp_category`
--

DROP TABLE IF EXISTS `ecomapp_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecomapp_category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecomapp_category`
--

LOCK TABLES `ecomapp_category` WRITE;
/*!40000 ALTER TABLE `ecomapp_category` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecomapp_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecomapp_customer`
--

DROP TABLE IF EXISTS `ecomapp_customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecomapp_customer` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `mobile_number` varchar(15) NOT NULL,
  `role` varchar(20) NOT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `user_address` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `mobile_number` (`mobile_number`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecomapp_customer`
--

LOCK TABLES `ecomapp_customer` WRITE;
/*!40000 ALTER TABLE `ecomapp_customer` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecomapp_customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecomapp_customer_groups`
--

DROP TABLE IF EXISTS `ecomapp_customer_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecomapp_customer_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customer_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ecomapp_customer_groups_customer_id_group_id_260162bb_uniq` (`customer_id`,`group_id`),
  KEY `ecomapp_customer_groups_group_id_4bc9e778_fk_auth_group_id` (`group_id`),
  CONSTRAINT `ecomapp_customer_gro_customer_id_c4ffec19_fk_ecomapp_c` FOREIGN KEY (`customer_id`) REFERENCES `ecomapp_customer` (`id`),
  CONSTRAINT `ecomapp_customer_groups_group_id_4bc9e778_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecomapp_customer_groups`
--

LOCK TABLES `ecomapp_customer_groups` WRITE;
/*!40000 ALTER TABLE `ecomapp_customer_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecomapp_customer_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecomapp_customer_user_permissions`
--

DROP TABLE IF EXISTS `ecomapp_customer_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecomapp_customer_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customer_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ecomapp_customer_user_pe_customer_id_permission_i_21932fef_uniq` (`customer_id`,`permission_id`),
  KEY `ecomapp_customer_use_permission_id_a1680b6b_fk_auth_perm` (`permission_id`),
  CONSTRAINT `ecomapp_customer_use_customer_id_a335477a_fk_ecomapp_c` FOREIGN KEY (`customer_id`) REFERENCES `ecomapp_customer` (`id`),
  CONSTRAINT `ecomapp_customer_use_permission_id_a1680b6b_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecomapp_customer_user_permissions`
--

LOCK TABLES `ecomapp_customer_user_permissions` WRITE;
/*!40000 ALTER TABLE `ecomapp_customer_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecomapp_customer_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecomapp_deliverypartner`
--

DROP TABLE IF EXISTS `ecomapp_deliverypartner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecomapp_deliverypartner` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `vehicle_number` varchar(20) DEFAULT NULL,
  `is_available` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ecomapp_deliverypartner_user_id_3adf38b2_fk_ecomapp_customer_id` (`user_id`),
  CONSTRAINT `ecomapp_deliverypartner_user_id_3adf38b2_fk_ecomapp_customer_id` FOREIGN KEY (`user_id`) REFERENCES `ecomapp_customer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecomapp_deliverypartner`
--

LOCK TABLES `ecomapp_deliverypartner` WRITE;
/*!40000 ALTER TABLE `ecomapp_deliverypartner` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecomapp_deliverypartner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecomapp_notification`
--

DROP TABLE IF EXISTS `ecomapp_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecomapp_notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `message` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ecomapp_notification_user_id_d562c985_fk_ecomapp_customer_id` (`user_id`),
  CONSTRAINT `ecomapp_notification_user_id_d562c985_fk_ecomapp_customer_id` FOREIGN KEY (`user_id`) REFERENCES `ecomapp_customer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecomapp_notification`
--

LOCK TABLES `ecomapp_notification` WRITE;
/*!40000 ALTER TABLE `ecomapp_notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecomapp_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecomapp_order`
--

DROP TABLE IF EXISTS `ecomapp_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecomapp_order` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `total_price` decimal(10,2) NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ecomapp_order_user_id_cfea005f_fk_ecomapp_customer_id` (`user_id`),
  CONSTRAINT `ecomapp_order_user_id_cfea005f_fk_ecomapp_customer_id` FOREIGN KEY (`user_id`) REFERENCES `ecomapp_customer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecomapp_order`
--

LOCK TABLES `ecomapp_order` WRITE;
/*!40000 ALTER TABLE `ecomapp_order` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecomapp_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecomapp_orderitem`
--

DROP TABLE IF EXISTS `ecomapp_orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecomapp_orderitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int unsigned NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `order_id` bigint NOT NULL,
  `product_variation_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ecomapp_orderitem_order_id_1aa10080_fk_ecomapp_order_id` (`order_id`),
  KEY `ecomapp_orderitem_product_variation_id_6764dca0_fk_ecomapp_p` (`product_variation_id`),
  CONSTRAINT `ecomapp_orderitem_order_id_1aa10080_fk_ecomapp_order_id` FOREIGN KEY (`order_id`) REFERENCES `ecomapp_order` (`id`),
  CONSTRAINT `ecomapp_orderitem_product_variation_id_6764dca0_fk_ecomapp_p` FOREIGN KEY (`product_variation_id`) REFERENCES `ecomapp_productvariation` (`id`),
  CONSTRAINT `ecomapp_orderitem_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecomapp_orderitem`
--

LOCK TABLES `ecomapp_orderitem` WRITE;
/*!40000 ALTER TABLE `ecomapp_orderitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecomapp_orderitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecomapp_ordertracking`
--

DROP TABLE IF EXISTS `ecomapp_ordertracking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecomapp_ordertracking` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(50) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `order_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ecomapp_ordertracking_order_id_4232f41c_fk_ecomapp_order_id` (`order_id`),
  CONSTRAINT `ecomapp_ordertracking_order_id_4232f41c_fk_ecomapp_order_id` FOREIGN KEY (`order_id`) REFERENCES `ecomapp_order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecomapp_ordertracking`
--

LOCK TABLES `ecomapp_ordertracking` WRITE;
/*!40000 ALTER TABLE `ecomapp_ordertracking` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecomapp_ordertracking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecomapp_payment`
--

DROP TABLE IF EXISTS `ecomapp_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecomapp_payment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `payment_method` varchar(50) NOT NULL,
  `transaction_id` varchar(255) DEFAULT NULL,
  `amount` decimal(10,2) NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `order_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ecomapp_payment_order_id_68a5a8cb_fk_ecomapp_order_id` (`order_id`),
  KEY `ecomapp_payment_user_id_3839874e_fk_ecomapp_customer_id` (`user_id`),
  CONSTRAINT `ecomapp_payment_order_id_68a5a8cb_fk_ecomapp_order_id` FOREIGN KEY (`order_id`) REFERENCES `ecomapp_order` (`id`),
  CONSTRAINT `ecomapp_payment_user_id_3839874e_fk_ecomapp_customer_id` FOREIGN KEY (`user_id`) REFERENCES `ecomapp_customer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecomapp_payment`
--

LOCK TABLES `ecomapp_payment` WRITE;
/*!40000 ALTER TABLE `ecomapp_payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecomapp_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecomapp_product`
--

DROP TABLE IF EXISTS `ecomapp_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecomapp_product` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `brand` varchar(255) DEFAULT NULL,
  `description` longtext,
  `warranty` varchar(255) DEFAULT NULL,
  `return_policy` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `category_id` bigint DEFAULT NULL,
  `shop_id` bigint NOT NULL,
  `subcategory_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ecomapp_product_shop_id_2b45d768_fk_ecomapp_profile_id` (`shop_id`),
  KEY `ecomapp_product_subcategory_id_b92016dc_fk_ecomapp_s` (`subcategory_id`),
  KEY `ecomapp_product_category_id_14696d36_fk_ecomapp_category_id` (`category_id`),
  CONSTRAINT `ecomapp_product_category_id_14696d36_fk_ecomapp_category_id` FOREIGN KEY (`category_id`) REFERENCES `ecomapp_category` (`id`),
  CONSTRAINT `ecomapp_product_shop_id_2b45d768_fk_ecomapp_profile_id` FOREIGN KEY (`shop_id`) REFERENCES `ecomapp_profile` (`id`),
  CONSTRAINT `ecomapp_product_subcategory_id_b92016dc_fk_ecomapp_s` FOREIGN KEY (`subcategory_id`) REFERENCES `ecomapp_subcategory` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecomapp_product`
--

LOCK TABLES `ecomapp_product` WRITE;
/*!40000 ALTER TABLE `ecomapp_product` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecomapp_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecomapp_productimage`
--

DROP TABLE IF EXISTS `ecomapp_productimage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecomapp_productimage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ecomapp_productimage_product_id_53dbe922_fk_ecomapp_product_id` (`product_id`),
  CONSTRAINT `ecomapp_productimage_product_id_53dbe922_fk_ecomapp_product_id` FOREIGN KEY (`product_id`) REFERENCES `ecomapp_product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecomapp_productimage`
--

LOCK TABLES `ecomapp_productimage` WRITE;
/*!40000 ALTER TABLE `ecomapp_productimage` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecomapp_productimage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecomapp_productvariation`
--

DROP TABLE IF EXISTS `ecomapp_productvariation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecomapp_productvariation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `variation_type` varchar(50) NOT NULL,
  `value` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `offer_price` decimal(10,2) DEFAULT NULL,
  `stock` int unsigned NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ecomapp_productvaria_product_id_ec4ce4d9_fk_ecomapp_p` (`product_id`),
  CONSTRAINT `ecomapp_productvaria_product_id_ec4ce4d9_fk_ecomapp_p` FOREIGN KEY (`product_id`) REFERENCES `ecomapp_product` (`id`),
  CONSTRAINT `ecomapp_productvariation_chk_1` CHECK ((`stock` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecomapp_productvariation`
--

LOCK TABLES `ecomapp_productvariation` WRITE;
/*!40000 ALTER TABLE `ecomapp_productvariation` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecomapp_productvariation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecomapp_profile`
--

DROP TABLE IF EXISTS `ecomapp_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecomapp_profile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `shop_name` varchar(255) NOT NULL,
  `shop_image` varchar(100) DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `opening_time` time(6) NOT NULL,
  `closing_time` time(6) NOT NULL,
  `delivers_orders` tinyint(1) NOT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `category_id` bigint DEFAULT NULL,
  `employee_id` bigint NOT NULL,
  `subcategory_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ecomapp_profile_subcategory_id_d061ff31_fk_ecomapp_s` (`subcategory_id`),
  KEY `ecomapp_profile_category_id_8215b7f9_fk_ecomapp_category_id` (`category_id`),
  KEY `ecomapp_profile_employee_id_01d32b33_fk_ecomapp_customer_id` (`employee_id`),
  CONSTRAINT `ecomapp_profile_category_id_8215b7f9_fk_ecomapp_category_id` FOREIGN KEY (`category_id`) REFERENCES `ecomapp_category` (`id`),
  CONSTRAINT `ecomapp_profile_employee_id_01d32b33_fk_ecomapp_customer_id` FOREIGN KEY (`employee_id`) REFERENCES `ecomapp_customer` (`id`),
  CONSTRAINT `ecomapp_profile_subcategory_id_d061ff31_fk_ecomapp_s` FOREIGN KEY (`subcategory_id`) REFERENCES `ecomapp_subcategory` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecomapp_profile`
--

LOCK TABLES `ecomapp_profile` WRITE;
/*!40000 ALTER TABLE `ecomapp_profile` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecomapp_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecomapp_review`
--

DROP TABLE IF EXISTS `ecomapp_review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecomapp_review` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `rating` int NOT NULL,
  `comment` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `product_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ecomapp_review_product_id_ea011bbd_fk_ecomapp_product_id` (`product_id`),
  KEY `ecomapp_review_user_id_551efc83_fk_ecomapp_customer_id` (`user_id`),
  CONSTRAINT `ecomapp_review_product_id_ea011bbd_fk_ecomapp_product_id` FOREIGN KEY (`product_id`) REFERENCES `ecomapp_product` (`id`),
  CONSTRAINT `ecomapp_review_user_id_551efc83_fk_ecomapp_customer_id` FOREIGN KEY (`user_id`) REFERENCES `ecomapp_customer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecomapp_review`
--

LOCK TABLES `ecomapp_review` WRITE;
/*!40000 ALTER TABLE `ecomapp_review` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecomapp_review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecomapp_subcategory`
--

DROP TABLE IF EXISTS `ecomapp_subcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecomapp_subcategory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `category_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ecomapp_subcategory_category_id_b134b707_fk_ecomapp_category_id` (`category_id`),
  CONSTRAINT `ecomapp_subcategory_category_id_b134b707_fk_ecomapp_category_id` FOREIGN KEY (`category_id`) REFERENCES `ecomapp_category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecomapp_subcategory`
--

LOCK TABLES `ecomapp_subcategory` WRITE;
/*!40000 ALTER TABLE `ecomapp_subcategory` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecomapp_subcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecomapp_wishlist`
--

DROP TABLE IF EXISTS `ecomapp_wishlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecomapp_wishlist` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ecomapp_wishlist_product_id_81fd3e9d_fk_ecomapp_product_id` (`product_id`),
  KEY `ecomapp_wishlist_user_id_771ac8f6_fk_ecomapp_customer_id` (`user_id`),
  CONSTRAINT `ecomapp_wishlist_product_id_81fd3e9d_fk_ecomapp_product_id` FOREIGN KEY (`product_id`) REFERENCES `ecomapp_product` (`id`),
  CONSTRAINT `ecomapp_wishlist_user_id_771ac8f6_fk_ecomapp_customer_id` FOREIGN KEY (`user_id`) REFERENCES `ecomapp_customer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecomapp_wishlist`
--

LOCK TABLES `ecomapp_wishlist` WRITE;
/*!40000 ALTER TABLE `ecomapp_wishlist` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecomapp_wishlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gateway_customuser`
--

DROP TABLE IF EXISTS `gateway_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gateway_customuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(254) NOT NULL,
  `password` varchar(255) NOT NULL,
  `username` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gateway_customuser`
--

LOCK TABLES `gateway_customuser` WRITE;
/*!40000 ALTER TABLE `gateway_customuser` DISABLE KEYS */;
/*!40000 ALTER TABLE `gateway_customuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gateway_customuser_groups`
--

DROP TABLE IF EXISTS `gateway_customuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gateway_customuser_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `gateway_customuser_groups_customuser_id_group_id_4aee3621_uniq` (`customuser_id`,`group_id`),
  KEY `gateway_customuser_groups_group_id_308c402a_fk_auth_group_id` (`group_id`),
  CONSTRAINT `gateway_customuser_g_customuser_id_d245a74a_fk_gateway_c` FOREIGN KEY (`customuser_id`) REFERENCES `gateway_customuser` (`id`),
  CONSTRAINT `gateway_customuser_groups_group_id_308c402a_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gateway_customuser_groups`
--

LOCK TABLES `gateway_customuser_groups` WRITE;
/*!40000 ALTER TABLE `gateway_customuser_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `gateway_customuser_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gateway_customuser_user_permissions`
--

DROP TABLE IF EXISTS `gateway_customuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gateway_customuser_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `gateway_customuser_user__customuser_id_permission_f4ecbb72_uniq` (`customuser_id`,`permission_id`),
  KEY `gateway_customuser_u_permission_id_277e9e21_fk_auth_perm` (`permission_id`),
  CONSTRAINT `gateway_customuser_u_customuser_id_b3fc57b1_fk_gateway_c` FOREIGN KEY (`customuser_id`) REFERENCES `gateway_customuser` (`id`),
  CONSTRAINT `gateway_customuser_u_permission_id_277e9e21_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gateway_customuser_user_permissions`
--

LOCK TABLES `gateway_customuser_user_permissions` WRITE;
/*!40000 ALTER TABLE `gateway_customuser_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `gateway_customuser_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gateway_device`
--

DROP TABLE IF EXISTS `gateway_device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gateway_device` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `device` varchar(100) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device` (`device`),
  KEY `gateway_device_user_id_01871f71_fk_gateway_customuser_id` (`user_id`),
  CONSTRAINT `gateway_device_user_id_01871f71_fk_gateway_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `gateway_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gateway_device`
--

LOCK TABLES `gateway_device` WRITE;
/*!40000 ALTER TABLE `gateway_device` DISABLE KEYS */;
/*!40000 ALTER TABLE `gateway_device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gateway_gpsdata`
--

DROP TABLE IF EXISTS `gateway_gpsdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gateway_gpsdata` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `latitude` json DEFAULT NULL,
  `longitude` json DEFAULT NULL,
  `engine_status` json DEFAULT NULL,
  `speed_kmh` json DEFAULT NULL,
  `max_speed` json DEFAULT NULL,
  `battery_level` json DEFAULT NULL,
  `ignition_on` json DEFAULT NULL,
  `date` datetime(6) NOT NULL,
  `device_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gateway_gpsdata_device_id_6f2eff81_fk_gateway_device_id` (`device_id`),
  CONSTRAINT `gateway_gpsdata_device_id_6f2eff81_fk_gateway_device_id` FOREIGN KEY (`device_id`) REFERENCES `gateway_device` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gateway_gpsdata`
--

LOCK TABLES `gateway_gpsdata` WRITE;
/*!40000 ALTER TABLE `gateway_gpsdata` DISABLE KEYS */;
/*!40000 ALTER TABLE `gateway_gpsdata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `officeapp_attendance`
--

DROP TABLE IF EXISTS `officeapp_attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `officeapp_attendance` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `logs` json NOT NULL,
  `total_hours` double NOT NULL,
  `employee_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `officeapp_attendance_employee_id_d439a166_fk_officeapp` (`employee_id`),
  CONSTRAINT `officeapp_attendance_employee_id_d439a166_fk_officeapp` FOREIGN KEY (`employee_id`) REFERENCES `officeapp_employee` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `officeapp_attendance`
--

LOCK TABLES `officeapp_attendance` WRITE;
/*!40000 ALTER TABLE `officeapp_attendance` DISABLE KEYS */;
/*!40000 ALTER TABLE `officeapp_attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `officeapp_device`
--

DROP TABLE IF EXISTS `officeapp_device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `officeapp_device` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `device_id` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id` (`device_id`),
  KEY `officeapp_device_user_id_27d2553b_fk_officeapp_employee_id` (`user_id`),
  CONSTRAINT `officeapp_device_user_id_27d2553b_fk_officeapp_employee_id` FOREIGN KEY (`user_id`) REFERENCES `officeapp_employee` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `officeapp_device`
--

LOCK TABLES `officeapp_device` WRITE;
/*!40000 ALTER TABLE `officeapp_device` DISABLE KEYS */;
/*!40000 ALTER TABLE `officeapp_device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `officeapp_employee`
--

DROP TABLE IF EXISTS `officeapp_employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `officeapp_employee` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `device_id` varchar(255) DEFAULT NULL,
  `role` varchar(10) NOT NULL,
  `employee_id` varchar(20) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `employee_id` (`employee_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `device_id` (`device_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `officeapp_employee`
--

LOCK TABLES `officeapp_employee` WRITE;
/*!40000 ALTER TABLE `officeapp_employee` DISABLE KEYS */;
/*!40000 ALTER TABLE `officeapp_employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `officeapp_employee_groups`
--

DROP TABLE IF EXISTS `officeapp_employee_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `officeapp_employee_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `employee_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `officeapp_employee_groups_employee_id_group_id_1356e15d_uniq` (`employee_id`,`group_id`),
  KEY `officeapp_employee_groups_group_id_44f8d08d_fk_auth_group_id` (`group_id`),
  CONSTRAINT `officeapp_employee_g_employee_id_4af68fe1_fk_officeapp` FOREIGN KEY (`employee_id`) REFERENCES `officeapp_employee` (`id`),
  CONSTRAINT `officeapp_employee_groups_group_id_44f8d08d_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `officeapp_employee_groups`
--

LOCK TABLES `officeapp_employee_groups` WRITE;
/*!40000 ALTER TABLE `officeapp_employee_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `officeapp_employee_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `officeapp_employee_organizations`
--

DROP TABLE IF EXISTS `officeapp_employee_organizations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `officeapp_employee_organizations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `employee_id` bigint NOT NULL,
  `organization_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `officeapp_employee_organ_employee_id_organization_78999ead_uniq` (`employee_id`,`organization_id`),
  KEY `officeapp_employee_o_organization_id_e819883e_fk_officeapp` (`organization_id`),
  CONSTRAINT `officeapp_employee_o_employee_id_285cf95a_fk_officeapp` FOREIGN KEY (`employee_id`) REFERENCES `officeapp_employee` (`id`),
  CONSTRAINT `officeapp_employee_o_organization_id_e819883e_fk_officeapp` FOREIGN KEY (`organization_id`) REFERENCES `officeapp_organization` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `officeapp_employee_organizations`
--

LOCK TABLES `officeapp_employee_organizations` WRITE;
/*!40000 ALTER TABLE `officeapp_employee_organizations` DISABLE KEYS */;
/*!40000 ALTER TABLE `officeapp_employee_organizations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `officeapp_employee_user_permissions`
--

DROP TABLE IF EXISTS `officeapp_employee_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `officeapp_employee_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `employee_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `officeapp_employee_user__employee_id_permission_i_f42a5c32_uniq` (`employee_id`,`permission_id`),
  KEY `officeapp_employee_u_permission_id_9093be75_fk_auth_perm` (`permission_id`),
  CONSTRAINT `officeapp_employee_u_employee_id_d3e12940_fk_officeapp` FOREIGN KEY (`employee_id`) REFERENCES `officeapp_employee` (`id`),
  CONSTRAINT `officeapp_employee_u_permission_id_9093be75_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `officeapp_employee_user_permissions`
--

LOCK TABLES `officeapp_employee_user_permissions` WRITE;
/*!40000 ALTER TABLE `officeapp_employee_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `officeapp_employee_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `officeapp_organization`
--

DROP TABLE IF EXISTS `officeapp_organization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `officeapp_organization` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `address` varchar(100) NOT NULL,
  `phone` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `website` varchar(200) NOT NULL,
  `logo` varchar(100) NOT NULL,
  `key` varchar(10) NOT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `officeapp_organization`
--

LOCK TABLES `officeapp_organization` WRITE;
/*!40000 ALTER TABLE `officeapp_organization` DISABLE KEYS */;
/*!40000 ALTER TABLE `officeapp_organization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profile_utility_customer`
--

DROP TABLE IF EXISTS `profile_utility_customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profile_utility_customer` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `email_id` varchar(255) DEFAULT NULL,
  `course` varchar(100) DEFAULT NULL,
  `mobile` varchar(10) DEFAULT NULL,
  `designation` varchar(200) DEFAULT NULL,
  `college_name` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `resume` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profile_utility_customer`
--

LOCK TABLES `profile_utility_customer` WRITE;
/*!40000 ALTER TABLE `profile_utility_customer` DISABLE KEYS */;
/*!40000 ALTER TABLE `profile_utility_customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profile_utility_customuser`
--

DROP TABLE IF EXISTS `profile_utility_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profile_utility_customuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(10) NOT NULL,
  `location` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profile_utility_customuser`
--

LOCK TABLES `profile_utility_customuser` WRITE;
/*!40000 ALTER TABLE `profile_utility_customuser` DISABLE KEYS */;
/*!40000 ALTER TABLE `profile_utility_customuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profile_utility_customuser_groups`
--

DROP TABLE IF EXISTS `profile_utility_customuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profile_utility_customuser_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `profile_utility_customus_customuser_id_group_id_c3b84a73_uniq` (`customuser_id`,`group_id`),
  KEY `profile_utility_cust_group_id_22ed17bd_fk_auth_grou` (`group_id`),
  CONSTRAINT `profile_utility_cust_customuser_id_3ea261c5_fk_profile_u` FOREIGN KEY (`customuser_id`) REFERENCES `profile_utility_customuser` (`id`),
  CONSTRAINT `profile_utility_cust_group_id_22ed17bd_fk_auth_grou` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profile_utility_customuser_groups`
--

LOCK TABLES `profile_utility_customuser_groups` WRITE;
/*!40000 ALTER TABLE `profile_utility_customuser_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `profile_utility_customuser_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profile_utility_customuser_user_permissions`
--

DROP TABLE IF EXISTS `profile_utility_customuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profile_utility_customuser_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `profile_utility_customus_customuser_id_permission_10ed8e48_uniq` (`customuser_id`,`permission_id`),
  KEY `profile_utility_cust_permission_id_e56b56af_fk_auth_perm` (`permission_id`),
  CONSTRAINT `profile_utility_cust_customuser_id_e7fa8cf6_fk_profile_u` FOREIGN KEY (`customuser_id`) REFERENCES `profile_utility_customuser` (`id`),
  CONSTRAINT `profile_utility_cust_permission_id_e56b56af_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profile_utility_customuser_user_permissions`
--

LOCK TABLES `profile_utility_customuser_user_permissions` WRITE;
/*!40000 ALTER TABLE `profile_utility_customuser_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `profile_utility_customuser_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profile_utility_itemlist`
--

DROP TABLE IF EXISTS `profile_utility_itemlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profile_utility_itemlist` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) DEFAULT NULL,
  `total_floors` varchar(255) DEFAULT NULL,
  `no_of_employees` varchar(255) DEFAULT NULL,
  `project_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `profile_utility_item_project_id_fa03472d_fk_profile_u` (`project_id`),
  CONSTRAINT `profile_utility_item_project_id_fa03472d_fk_profile_u` FOREIGN KEY (`project_id`) REFERENCES `profile_utility_post` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profile_utility_itemlist`
--

LOCK TABLES `profile_utility_itemlist` WRITE;
/*!40000 ALTER TABLE `profile_utility_itemlist` DISABLE KEYS */;
/*!40000 ALTER TABLE `profile_utility_itemlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profile_utility_location`
--

DROP TABLE IF EXISTS `profile_utility_location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profile_utility_location` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `plan_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `profile_utility_loca_plan_id_0302992f_fk_profile_u` (`plan_id`),
  CONSTRAINT `profile_utility_loca_plan_id_0302992f_fk_profile_u` FOREIGN KEY (`plan_id`) REFERENCES `profile_utility_plan` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profile_utility_location`
--

LOCK TABLES `profile_utility_location` WRITE;
/*!40000 ALTER TABLE `profile_utility_location` DISABLE KEYS */;
/*!40000 ALTER TABLE `profile_utility_location` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profile_utility_marker`
--

DROP TABLE IF EXISTS `profile_utility_marker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profile_utility_marker` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `x` int NOT NULL,
  `y` int NOT NULL,
  `distance` double DEFAULT NULL,
  `plan_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `profile_utility_mark_plan_id_3dd64749_fk_profile_u` (`plan_id`),
  CONSTRAINT `profile_utility_mark_plan_id_3dd64749_fk_profile_u` FOREIGN KEY (`plan_id`) REFERENCES `profile_utility_plan` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profile_utility_marker`
--

LOCK TABLES `profile_utility_marker` WRITE;
/*!40000 ALTER TABLE `profile_utility_marker` DISABLE KEYS */;
/*!40000 ALTER TABLE `profile_utility_marker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profile_utility_plan`
--

DROP TABLE IF EXISTS `profile_utility_plan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profile_utility_plan` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `floor_or_name` varchar(255) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `floor_id` bigint DEFAULT NULL,
  `project_list_id` bigint DEFAULT NULL,
  `project_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `profile_utility_plan_project_id_0c3f1916_fk_profile_u` (`project_id`),
  KEY `profile_utility_plan_floor_id_d75eb686_fk_profile_u` (`floor_id`),
  KEY `profile_utility_plan_project_list_id_a2e5e05a_fk_profile_u` (`project_list_id`),
  CONSTRAINT `profile_utility_plan_floor_id_d75eb686_fk_profile_u` FOREIGN KEY (`floor_id`) REFERENCES `profile_utility_itemlist` (`id`),
  CONSTRAINT `profile_utility_plan_project_id_0c3f1916_fk_profile_u` FOREIGN KEY (`project_id`) REFERENCES `profile_utility_post` (`id`),
  CONSTRAINT `profile_utility_plan_project_list_id_a2e5e05a_fk_profile_u` FOREIGN KEY (`project_list_id`) REFERENCES `profile_utility_itemlist` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profile_utility_plan`
--

LOCK TABLES `profile_utility_plan` WRITE;
/*!40000 ALTER TABLE `profile_utility_plan` DISABLE KEYS */;
/*!40000 ALTER TABLE `profile_utility_plan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profile_utility_post`
--

DROP TABLE IF EXISTS `profile_utility_post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profile_utility_post` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `project_name` varchar(255) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `user_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `profile_utility_post_user_id_b4cc1c44_fk_profile_u` (`user_id`),
  CONSTRAINT `profile_utility_post_user_id_b4cc1c44_fk_profile_u` FOREIGN KEY (`user_id`) REFERENCES `profile_utility_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profile_utility_post`
--

LOCK TABLES `profile_utility_post` WRITE;
/*!40000 ALTER TABLE `profile_utility_post` DISABLE KEYS */;
/*!40000 ALTER TABLE `profile_utility_post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profile_utility_savejson`
--

DROP TABLE IF EXISTS `profile_utility_savejson`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profile_utility_savejson` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `data` json DEFAULT NULL,
  `floor_id` bigint DEFAULT NULL,
  `plan_id` bigint DEFAULT NULL,
  `project_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `profile_utility_save_floor_id_6c8f844b_fk_profile_u` (`floor_id`),
  KEY `profile_utility_save_plan_id_f7cb3165_fk_profile_u` (`plan_id`),
  KEY `profile_utility_save_project_id_a52c3070_fk_profile_u` (`project_id`),
  CONSTRAINT `profile_utility_save_floor_id_6c8f844b_fk_profile_u` FOREIGN KEY (`floor_id`) REFERENCES `profile_utility_itemlist` (`id`),
  CONSTRAINT `profile_utility_save_plan_id_f7cb3165_fk_profile_u` FOREIGN KEY (`plan_id`) REFERENCES `profile_utility_plan` (`id`),
  CONSTRAINT `profile_utility_save_project_id_a52c3070_fk_profile_u` FOREIGN KEY (`project_id`) REFERENCES `profile_utility_post` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profile_utility_savejson`
--

LOCK TABLES `profile_utility_savejson` WRITE;
/*!40000 ALTER TABLE `profile_utility_savejson` DISABLE KEYS */;
/*!40000 ALTER TABLE `profile_utility_savejson` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profile_utility_videoframe`
--

DROP TABLE IF EXISTS `profile_utility_videoframe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profile_utility_videoframe` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `frame_number` int NOT NULL,
  `image` varchar(100) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `json_id` bigint DEFAULT NULL,
  `plan_id` bigint DEFAULT NULL,
  `video_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `profile_utility_vide_json_id_4f9ee9c4_fk_profile_u` (`json_id`),
  KEY `profile_utility_vide_plan_id_1693936b_fk_profile_u` (`plan_id`),
  KEY `profile_utility_vide_video_id_2de25626_fk_profile_u` (`video_id`),
  CONSTRAINT `profile_utility_vide_json_id_4f9ee9c4_fk_profile_u` FOREIGN KEY (`json_id`) REFERENCES `profile_utility_savejson` (`id`),
  CONSTRAINT `profile_utility_vide_plan_id_1693936b_fk_profile_u` FOREIGN KEY (`plan_id`) REFERENCES `profile_utility_plan` (`id`),
  CONSTRAINT `profile_utility_vide_video_id_2de25626_fk_profile_u` FOREIGN KEY (`video_id`) REFERENCES `profile_utility_videoupload` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profile_utility_videoframe`
--

LOCK TABLES `profile_utility_videoframe` WRITE;
/*!40000 ALTER TABLE `profile_utility_videoframe` DISABLE KEYS */;
/*!40000 ALTER TABLE `profile_utility_videoframe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profile_utility_videoupload`
--

DROP TABLE IF EXISTS `profile_utility_videoupload`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profile_utility_videoupload` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `description` longtext NOT NULL,
  `file` varchar(100) DEFAULT NULL,
  `thumbnail` varchar(100) DEFAULT NULL,
  `upload_date` datetime(6) DEFAULT NULL,
  `floor_id` bigint DEFAULT NULL,
  `json_id` bigint DEFAULT NULL,
  `plan_id` bigint DEFAULT NULL,
  `user_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `profile_utility_vide_floor_id_4695e786_fk_profile_u` (`floor_id`),
  KEY `profile_utility_vide_json_id_b7e79a41_fk_profile_u` (`json_id`),
  KEY `profile_utility_vide_plan_id_9958b43a_fk_profile_u` (`plan_id`),
  KEY `profile_utility_vide_user_id_431bd84c_fk_profile_u` (`user_id`),
  CONSTRAINT `profile_utility_vide_floor_id_4695e786_fk_profile_u` FOREIGN KEY (`floor_id`) REFERENCES `profile_utility_itemlist` (`id`),
  CONSTRAINT `profile_utility_vide_json_id_b7e79a41_fk_profile_u` FOREIGN KEY (`json_id`) REFERENCES `profile_utility_savejson` (`id`),
  CONSTRAINT `profile_utility_vide_plan_id_9958b43a_fk_profile_u` FOREIGN KEY (`plan_id`) REFERENCES `profile_utility_plan` (`id`),
  CONSTRAINT `profile_utility_vide_user_id_431bd84c_fk_profile_u` FOREIGN KEY (`user_id`) REFERENCES `profile_utility_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profile_utility_videoupload`
--

LOCK TABLES `profile_utility_videoupload` WRITE;
/*!40000 ALTER TABLE `profile_utility_videoupload` DISABLE KEYS */;
/*!40000 ALTER TABLE `profile_utility_videoupload` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-17  5:46:20
