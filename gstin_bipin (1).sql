-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jan 25, 2022 at 05:29 PM
-- Server version: 8.0.22-0ubuntu0.20.04.3
-- PHP Version: 7.4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `gstin_bipin`
--

-- --------------------------------------------------------

--
-- Table structure for table `agst_basic_original`
--

CREATE TABLE `agst_basic_original` (
  `id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `gstin` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  `status` varchar(50) NOT NULL,
  `gst_bd` varchar(10) NOT NULL,
  `gst_gd` varchar(10) NOT NULL,
  `gst_fd` varchar(10) NOT NULL,
  `gst_all` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `attendees`
--

CREATE TABLE `attendees` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `eventId` int DEFAULT NULL,
  `answer` enum('1','2','3') NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `cin_pan`
--

CREATE TABLE `cin_pan` (
  `id` int NOT NULL,
  `cin` varchar(21) DEFAULT NULL,
  `pan` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `event`
--

CREATE TABLE `event` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `when` datetime NOT NULL,
  `address` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `gstbasic`
--

CREATE TABLE `gstbasic` (
  `id` int NOT NULL,
  `gstin` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `userid` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '',
  `password` varchar(200) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '',
  `gst_gd` tinyint NOT NULL DEFAULT '0',
  `gst_bd` tinyint NOT NULL DEFAULT '0',
  `gst_fd` tinyint NOT NULL DEFAULT '0',
  `gst_all` tinyint NOT NULL DEFAULT '0',
  `datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `pan` varchar(10) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `pin` varchar(6) DEFAULT NULL,
  `link` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `gstin_filing_detail`
--

CREATE TABLE `gstin_filing_detail` (
  `id` int NOT NULL,
  `fy` varchar(20) NOT NULL,
  `taxp` varchar(20) NOT NULL,
  `mof` varchar(20) NOT NULL,
  `dof` varchar(20) NOT NULL,
  `rtntype` varchar(100) NOT NULL,
  `arn` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `insert_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `gstin` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `gst_basic`
--

CREATE TABLE `gst_basic` (
  `id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `gstid` varchar(30) NOT NULL,
  `state` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0',
  `gst_bd` varchar(5) NOT NULL DEFAULT '0',
  `gst_gd` varchar(5) NOT NULL DEFAULT '0',
  `gst_fd` varchar(5) NOT NULL DEFAULT '0',
  `gst_pan` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0',
  `insert_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `gst_business_detail`
--

CREATE TABLE `gst_business_detail` (
  `id` int NOT NULL,
  `adr` varchar(100) NOT NULL,
  `em` varchar(100) NOT NULL,
  `mb` varchar(100) NOT NULL,
  `addr` varchar(250) NOT NULL,
  `ntr` varchar(50) NOT NULL,
  `lastUpdatedDate` varchar(100) NOT NULL,
  `gstin` varchar(20) NOT NULL,
  `insert_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `gst_detail`
--

CREATE TABLE `gst_detail` (
  `id` int NOT NULL,
  `nba` varchar(250) NOT NULL,
  `mandatedeInvoice` varchar(250) NOT NULL,
  `aggreTurnOverFY` varchar(250) NOT NULL,
  `lgnm` varchar(250) NOT NULL,
  `dty` varchar(250) NOT NULL,
  `aggreTurnOver` varchar(250) NOT NULL,
  `cxdt` varchar(200) NOT NULL,
  `gstin` varchar(200) NOT NULL,
  `gtiFY` varchar(200) NOT NULL,
  `cmpRt` varchar(200) NOT NULL,
  `rgdt` varchar(200) NOT NULL,
  `ctb` varchar(200) NOT NULL,
  `sts` varchar(200) NOT NULL,
  `tradeNam` varchar(200) NOT NULL,
  `isFieldVisitConducted` varchar(200) NOT NULL,
  `ctj` varchar(200) NOT NULL,
  `percentTaxInCashFY` varchar(200) NOT NULL,
  `percentTaxInCash` varchar(200) NOT NULL,
  `compDetl` varchar(200) NOT NULL,
  `gti` varchar(200) NOT NULL,
  `adhrVFlag` varchar(20) NOT NULL,
  `ekycVFlag` varchar(20) NOT NULL,
  `stj` varchar(50) NOT NULL,
  `mbr` varchar(1000) NOT NULL,
  `insert_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `gst_name_tab`
--

CREATE TABLE `gst_name_tab` (
  `id` int NOT NULL,
  `name` varchar(200) NOT NULL,
  `status` int NOT NULL,
  `working` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `gst_order`
--

CREATE TABLE `gst_order` (
  `id` int NOT NULL,
  `user_id` varchar(50) DEFAULT NULL,
  `gstin` varchar(15) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `gst_search_querys`
--

CREATE TABLE `gst_search_querys` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `working` int NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `query-result-cache`
--

CREATE TABLE `query-result-cache` (
  `id` int NOT NULL,
  `identifier` varchar(255) DEFAULT NULL,
  `time` bigint NOT NULL,
  `duration` int NOT NULL,
  `query` text NOT NULL,
  `result` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `refresh_token`
--

CREATE TABLE `refresh_token` (
  `id` int NOT NULL,
  `rtoken` varchar(255) NOT NULL,
  `userId` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `serch`
--

CREATE TABLE `serch` (
  `id` int NOT NULL,
  `text` varchar(250) NOT NULL,
  `type` enum('pan','name') NOT NULL,
  `status` tinyint NOT NULL DEFAULT '0',
  `datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `token` varchar(255) NOT NULL,
  `currentHashedRefreshToken` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `agst_basic_original`
--
ALTER TABLE `agst_basic_original`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `attendees`
--
ALTER TABLE `attendees`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_4925989ece225c9c203da5c225c` (`eventId`);

--
-- Indexes for table `cin_pan`
--
ALTER TABLE `cin_pan`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `event`
--
ALTER TABLE `event`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `gstbasic`
--
ALTER TABLE `gstbasic`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `gstin` (`gstin`);

--
-- Indexes for table `gstin_filing_detail`
--
ALTER TABLE `gstin_filing_detail`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idex` (`taxp`,`fy`,`gstin`) USING BTREE;

--
-- Indexes for table `gst_basic`
--
ALTER TABLE `gst_basic`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`,`gstid`,`state`) USING BTREE;

--
-- Indexes for table `gst_business_detail`
--
ALTER TABLE `gst_business_detail`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `gst_detail`
--
ALTER TABLE `gst_detail`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `gstin` (`gstin`),
  ADD KEY `gstin_idx` (`lgnm`,`gstin`,`tradeNam`) USING BTREE,
  ADD KEY `gstin_tradeNam` (`id`,`tradeNam`);

--
-- Indexes for table `gst_name_tab`
--
ALTER TABLE `gst_name_tab`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `gst_order`
--
ALTER TABLE `gst_order`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id_gstin` (`user_id`,`gstin`);

--
-- Indexes for table `gst_search_querys`
--
ALTER TABLE `gst_search_querys`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `query-result-cache`
--
ALTER TABLE `query-result-cache`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `refresh_token`
--
ALTER TABLE `refresh_token`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_8e913e288156c133999341156ad` (`userId`);

--
-- Indexes for table `serch`
--
ALTER TABLE `serch`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `agst_basic_original`
--
ALTER TABLE `agst_basic_original`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `attendees`
--
ALTER TABLE `attendees`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `cin_pan`
--
ALTER TABLE `cin_pan`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `event`
--
ALTER TABLE `event`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `gstbasic`
--
ALTER TABLE `gstbasic`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `gstin_filing_detail`
--
ALTER TABLE `gstin_filing_detail`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `gst_basic`
--
ALTER TABLE `gst_basic`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `gst_business_detail`
--
ALTER TABLE `gst_business_detail`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `gst_detail`
--
ALTER TABLE `gst_detail`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `gst_name_tab`
--
ALTER TABLE `gst_name_tab`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `gst_order`
--
ALTER TABLE `gst_order`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `gst_search_querys`
--
ALTER TABLE `gst_search_querys`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `query-result-cache`
--
ALTER TABLE `query-result-cache`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `refresh_token`
--
ALTER TABLE `refresh_token`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `serch`
--
ALTER TABLE `serch`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `attendees`
--
ALTER TABLE `attendees`
  ADD CONSTRAINT `FK_4925989ece225c9c203da5c225c` FOREIGN KEY (`eventId`) REFERENCES `event` (`id`);

--
-- Constraints for table `refresh_token`
--
ALTER TABLE `refresh_token`
  ADD CONSTRAINT `FK_8e913e288156c133999341156ad` FOREIGN KEY (`userId`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
