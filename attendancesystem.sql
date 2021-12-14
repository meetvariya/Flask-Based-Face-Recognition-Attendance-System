-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 14, 2021 at 05:19 AM
-- Server version: 10.4.6-MariaDB
-- PHP Version: 7.2.22

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `attendancesystem`
--

-- --------------------------------------------------------

--
-- Table structure for table `adminlogin`
--

CREATE TABLE `adminlogin` (
  `username` varchar(10) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `adminlogin`
--

INSERT INTO `adminlogin` (`username`, `password`) VALUES
('meet', '123');

-- --------------------------------------------------------

--
-- Table structure for table `coursedetails`
--

CREATE TABLE `coursedetails` (
  `courseid` varchar(10) NOT NULL,
  `facultyname` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `coursedetails`
--

INSERT INTO `coursedetails` (`courseid`, `facultyname`) VALUES
('3cp01', 'kirtisir'),
('3cp02', 'kirtisir'),
('3cp03', 'mehul'),
('3cp04', 'hemantsir');

-- --------------------------------------------------------

--
-- Table structure for table `facultydetails`
--

CREATE TABLE `facultydetails` (
  `username` varchar(20) NOT NULL,
  `email` varchar(20) NOT NULL,
  `ph_no` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `facultydetails`
--

INSERT INTO `facultydetails` (`username`, `email`, `ph_no`) VALUES
('hemantsir', 'hemant@gmail.com', '7854963210'),
('kirtisir', 'kirti@gmail.com', '7410258960'),
('mehul', 'mehul@gmail.com', '9876543211');

-- --------------------------------------------------------

--
-- Table structure for table `logindata`
--

CREATE TABLE `logindata` (
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `role` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `logindata`
--

INSERT INTO `logindata` (`username`, `password`, `role`) VALUES
('admin', '123', 'admin'),
('ankur', 'ankur', 'student'),
('chintan', '123', 'student'),
('deep', 'deep', 'student'),
('deepnil', '123', 'student'),
('harsh', '123', 'student'),
('hemantsir', '123', 'faculty'),
('ketul', '123', 'student'),
('kirtisir', '123', 'faculty'),
('meet', '123', 'student'),
('mehul', '123', 'faculty'),
('om', '123', 'student'),
('rohan', '123', 'student'),
('vaibhav', '123', 'student');

-- --------------------------------------------------------

--
-- Table structure for table `studentdetails`
--

CREATE TABLE `studentdetails` (
  `username` varchar(50) NOT NULL,
  `batch` varchar(5) NOT NULL,
  `emailid` varchar(25) NOT NULL,
  `dob` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `studentdetails`
--

INSERT INTO `studentdetails` (`username`, `batch`, `emailid`, `dob`) VALUES
('ankur', 'a', 'ankur@gmail.com', '2000-02-01'),
('chintan', 'c', 'chintan@gmail.com', '2000-03-06'),
('deep', 'b', 'deep@gmail.com', '2001-01-01'),
('deepnil', 'c', 'deepnil@gmail.com', '2021-04-20'),
('harsh', 'a', 'harsh@gmail.com', '2000-05-15'),
('ketul', 'b', 'ketul@gmail.com', '2021-04-11'),
('meet', 'b', 'meetvariya00@gmail.com', '2001-07-23'),
('om', 'a', 'om@gmail.com', '2021-04-20'),
('rohan', 'a', 'rohan@gmail.com', '2000-10-20');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `adminlogin`
--
ALTER TABLE `adminlogin`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `coursedetails`
--
ALTER TABLE `coursedetails`
  ADD PRIMARY KEY (`courseid`);

--
-- Indexes for table `facultydetails`
--
ALTER TABLE `facultydetails`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `logindata`
--
ALTER TABLE `logindata`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `studentdetails`
--
ALTER TABLE `studentdetails`
  ADD PRIMARY KEY (`username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
