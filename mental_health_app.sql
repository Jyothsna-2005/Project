-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 14, 2026 at 10:48 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mental_health_app`
--

-- --------------------------------------------------------

--
-- Table structure for table `diary_entries`
--

CREATE TABLE `diary_entries` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `content` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `diary_entries`
--

INSERT INTO `diary_entries` (`id`, `user_id`, `title`, `content`, `created_at`) VALUES
(67, 1, 'hi', '<div style=\"text-align: left;\">helo</div>', '2026-04-15 02:21:55'),
(69, 1, 'helo', '<b>hiohb</b><div>iuyuk<b>jygh</b></div>', '2026-04-15 02:41:25'),
(70, 2, 'hi', 'helloo', '2026-04-15 22:22:05'),
(72, 1, 'hy', 'oug', '2026-04-16 03:19:58'),
(73, 16, 'Zenzest Project Plan', 'Day 1 -<div><ol><li>&nbsp;Install Python Flask</li><li>Download others packages</li><li>Create a project</li></ol></div>', '2026-04-22 13:18:47');

-- --------------------------------------------------------

--
-- Table structure for table `doctor_assigned`
--

CREATE TABLE `doctor_assigned` (
  `student_email` varchar(255) NOT NULL,
  `student_name` varchar(255) DEFAULT NULL,
  `doctor_name` varchar(255) DEFAULT NULL,
  `doctor_email` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `doctor_assigned`
--

INSERT INTO `doctor_assigned` (`student_email`, `student_name`, `doctor_name`, `doctor_email`) VALUES
('jake@gmail.com', 'Jake', 'Dr Remya', 'remya@gmail.com'),
('jyothsna@gmail.com', 'Jyothsna', 'Dr Remya', 'remya@gmail.com'),
('nandini@gmail.com', 'Nandini', 'Dr Remya', 'remya@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `game_scores`
--

CREATE TABLE `game_scores` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `game_name` varchar(50) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `time` varchar(20) DEFAULT NULL,
  `moves` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `game_scores`
--

INSERT INTO `game_scores` (`id`, `user_id`, `game_name`, `score`, `created_at`, `time`, `moves`) VALUES
(1, 1, 'TicTacToe', 5, '2026-04-14 12:08:01', NULL, NULL),
(2, 1, 'WordScramble', 7, '2026-04-14 12:15:01', NULL, NULL),
(5, 1, 'TicTacToe', 10, '2026-04-15 03:16:31', '00:06', 7),
(6, 1, 'WordScramble', 7, '2026-04-15 03:32:59', '121', 3),
(7, 1, 'Sudoku', 10, '2026-04-15 03:42:04', '173', NULL),
(8, 1, 'TicTacToe', 10, '2026-04-15 07:47:16', '00:06', 7),
(9, 1, 'TicTacToe', 10, '2026-04-15 08:10:26', '00:05', 7),
(11, 1, 'Memory Game', 13, '2026-04-15 09:19:36', '33s', 13),
(12, 2, 'TicTacToe', 10, '2026-04-15 22:23:02', '00:10', 7),
(13, 1, 'TicTacToe', 0, '2026-04-15 23:09:58', '00:03', 6),
(14, 1, 'WordScramble', 8, '2026-04-15 23:42:55', '224', 2),
(15, 1, 'Memory Game', 17, '2026-04-16 02:57:38', '42s', 17),
(16, 1, 'TicTacToe', 10, '2026-04-16 03:22:00', '00:06', 7),
(17, 1, 'TicTacToe', 5, '2026-04-16 03:22:30', '00:11', 9),
(18, 16, 'Memory Game', 18, '2026-04-22 13:20:27', '30s', 18),
(19, 16, 'WordScramble', 8, '2026-04-22 13:23:46', '188', 2),
(20, 16, 'TicTacToe', 10, '2026-04-22 13:24:14', '00:18', 7),
(21, 2, 'Memory Game', 14, '2026-04-24 08:28:48', '44s', 14),
(22, 2, 'WordScramble', 8, '2026-04-24 08:40:29', '688', 2),
(23, 2, 'TicTacToe', 5, '2026-04-24 08:40:49', '00:12', 9),
(24, 2, 'TicTacToe', 0, '2026-04-24 08:40:58', '00:07', 6),
(25, 2, 'TicTacToe', 5, '2026-04-24 08:41:23', '00:22', 9),
(26, 2, 'TicTacToe', 5, '2026-04-24 08:41:42', '00:17', 9),
(27, 2, 'TicTacToe', 5, '2026-04-24 08:41:57', '00:12', 9),
(28, 2, 'TicTacToe', 10, '2026-04-24 08:42:12', '00:13', 7),
(29, 2, 'TicTacToe', 0, '2026-04-24 08:42:29', '00:13', 8),
(30, 2, 'TicTacToe', 5, '2026-04-24 08:42:50', '00:17', 9),
(31, 2, 'TicTacToe', 5, '2026-04-24 08:43:04', '00:12', 9),
(32, 2, 'TicTacToe', 5, '2026-04-24 08:43:22', '00:16', 9),
(33, 2, 'TicTacToe', 5, '2026-04-24 08:43:38', '00:14', 9),
(34, 2, 'TicTacToe', 10, '2026-04-24 08:43:52', '00:12', 7);

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `sender_id` int(11) DEFAULT NULL,
  `receiver_id` int(11) DEFAULT NULL,
  `message` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `messages`
--

INSERT INTO `messages` (`id`, `sender_id`, `receiver_id`, `message`, `created_at`) VALUES
(29, 16, 6, 'Hello doctor', '2026-04-22 13:07:32'),
(30, 6, 16, 'Hi Jake', '2026-04-22 13:09:39'),
(31, 2, 6, 'hi', '2026-04-22 15:03:39'),
(32, 6, 2, 'hello there!', '2026-04-22 15:05:29'),
(33, 2, 6, 'my mental health is very poor because of my sister...she spend half of my salary in njyam njyam...ayooo what to what to do? my sister stomach kokapamb', '2026-04-24 08:51:17'),
(34, 6, 2, 'okay mwole. take care of your sister very well', '2026-04-24 08:51:57');

-- --------------------------------------------------------

--
-- Table structure for table `questionnaire_results`
--

CREATE TABLE `questionnaire_results` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `percentage` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `questionnaire_results`
--

INSERT INTO `questionnaire_results` (`id`, `user_id`, `score`, `percentage`, `created_at`) VALUES
(1, 1, 17, 57, '2026-04-14 13:00:06'),
(2, 1, 19, 63, '2026-04-15 07:57:52'),
(3, 1, 30, 100, '2026-04-15 08:02:34'),
(4, 1, 6, 20, '2026-04-15 09:29:54'),
(5, 2, 24, 80, '2026-04-15 22:21:00'),
(6, 2, 24, 80, '2026-04-15 22:24:08'),
(7, 1, 17, 57, '2026-04-15 23:09:24'),
(8, 1, 23, 77, '2026-04-16 02:40:28'),
(9, 1, 12, 40, '2026-04-16 02:47:32'),
(10, 1, 23, 77, '2026-04-16 03:10:16'),
(11, 11, 16, 53, '2026-04-22 10:36:11'),
(12, 16, 26, 87, '2026-04-22 13:17:00'),
(13, 2, 19, 63, '2026-04-24 08:26:53');

-- --------------------------------------------------------

--
-- Table structure for table `questions`
--

CREATE TABLE `questions` (
  `id` int(11) NOT NULL,
  `question` text NOT NULL,
  `option_a` varchar(255) DEFAULT NULL,
  `score_a` int(11) DEFAULT NULL,
  `option_b` varchar(255) DEFAULT NULL,
  `score_b` int(11) DEFAULT NULL,
  `option_c` varchar(255) DEFAULT NULL,
  `score_c` int(11) DEFAULT NULL,
  `option_d` varchar(255) DEFAULT NULL,
  `score_d` int(11) DEFAULT NULL,
  `createdAt` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `questions`
--

INSERT INTO `questions` (`id`, `question`, `option_a`, `score_a`, `option_b`, `score_b`, `option_c`, `score_c`, `option_d`, `score_d`, `createdAt`) VALUES
(1, 'How often do you feel stressed?', 'Never', 3, 'Sometimes', 2, 'Often', 1, 'Always', 0, '2026-04-22 10:29:45'),
(2, 'How well do you sleep?', 'Very well', 3, 'Okay', 2, 'Poorly', 1, 'Very poorly', 0, '2026-04-22 10:29:45'),
(3, 'How often do you feel happy?', 'Always', 3, 'Often', 2, 'Rarely', 1, 'Never', 0, '2026-04-22 10:29:45'),
(4, 'Do you feel motivated daily?', 'Very', 3, 'Somewhat', 2, 'Low', 1, 'None', 0, '2026-04-22 10:29:45'),
(5, 'How often do you feel anxious?', 'Never', 3, 'Sometimes', 2, 'Often', 1, 'Always', 0, '2026-04-22 10:29:45'),
(6, 'How well do you manage emotions?', 'Very well', 3, 'Okay', 2, 'Poorly', 1, 'Very poorly', 0, '2026-04-22 10:29:45'),
(7, 'Do you feel connected to others?', 'Very', 3, 'Somewhat', 2, 'Not much', 1, 'Not at all', 0, '2026-04-22 10:29:45'),
(8, 'How often do you feel tired?', 'Never', 3, 'Sometimes', 2, 'Often', 1, 'Always', 0, '2026-04-22 10:29:45'),
(9, 'How do you handle challenges?', 'Very well', 3, 'Okay', 2, 'Struggle', 1, 'Cannot handle', 0, '2026-04-22 10:29:45'),
(10, 'How satisfied are you with life?', 'Very', 3, 'Somewhat', 2, 'Not much', 1, 'Not at all', 0, '2026-04-22 10:29:45'),
(11, 'How often do you feel lonely?', 'Never', 3, 'Sometimes', 2, 'Often', 1, 'Always', 0, '2026-04-22 10:29:45'),
(12, 'Do you enjoy activities?', 'Always', 3, 'Often', 2, 'Rarely', 1, 'Never', 0, '2026-04-22 10:29:45'),
(13, 'How confident do you feel?', 'Very', 3, 'Moderate', 2, 'Low', 1, 'None', 0, '2026-04-22 10:29:45'),
(14, 'How often do you feel calm?', 'Always', 3, 'Often', 2, 'Rarely', 1, 'Never', 0, '2026-04-22 10:29:45'),
(15, 'Do you feel overwhelmed?', 'Never', 3, 'Sometimes', 2, 'Often', 1, 'Always', 0, '2026-04-22 10:29:45'),
(16, 'How is your concentration?', 'Excellent', 3, 'Good', 2, 'Poor', 1, 'Very poor', 0, '2026-04-22 10:29:45'),
(17, 'How often do you feel hopeless?', 'Never', 3, 'Sometimes', 2, 'Often', 1, 'Always', 0, '2026-04-22 10:29:45'),
(18, 'Do you feel energetic?', 'Always', 3, 'Often', 2, 'Rarely', 1, 'Never', 0, '2026-04-22 10:29:45'),
(19, 'How do you handle stress?', 'Very well', 3, 'Okay', 2, 'Poorly', 1, 'Very poorly', 0, '2026-04-22 10:29:45'),
(20, 'Do you feel emotionally stable?', 'Very', 3, 'Somewhat', 2, 'Not much', 1, 'Not at all', 0, '2026-04-22 10:29:45'),
(21, 'How often do you worry?', 'Never', 3, 'Sometimes', 2, 'Often', 1, 'Always', 0, '2026-04-22 10:29:45'),
(22, 'Do you feel positive about future?', 'Very', 3, 'Somewhat', 2, 'Not much', 1, 'Not at all', 0, '2026-04-22 10:29:45'),
(23, 'How often do you feel relaxed?', 'Always', 3, 'Often', 2, 'Rarely', 1, 'Never', 0, '2026-04-22 10:29:45'),
(24, 'Do you feel in control of your life?', 'Fully', 3, 'Somewhat', 2, 'Little', 1, 'Not at all', 0, '2026-04-22 10:29:45'),
(25, 'How often do you feel irritable?', 'Never', 3, 'Sometimes', 2, 'Often', 1, 'Always', 0, '2026-04-22 10:29:45');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `role` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `role`) VALUES
(2, 'Nandini', 'nandini@gmail.com', 'abcde', 'Student'),
(6, 'Dr Remya', 'remya1@gmail.com', 'remya123', 'Counsellor'),
(12, 'Jyothsna', 'jyothsna@gmail.com', '1', 'Student'),
(15, 'Admin', 'admin@gmail.com', 'admin123', 'Admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `diary_entries`
--
ALTER TABLE `diary_entries`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `doctor_assigned`
--
ALTER TABLE `doctor_assigned`
  ADD PRIMARY KEY (`student_email`);

--
-- Indexes for table `game_scores`
--
ALTER TABLE `game_scores`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `questionnaire_results`
--
ALTER TABLE `questionnaire_results`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `questions`
--
ALTER TABLE `questions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `diary_entries`
--
ALTER TABLE `diary_entries`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=74;

--
-- AUTO_INCREMENT for table `game_scores`
--
ALTER TABLE `game_scores`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `messages`
--
ALTER TABLE `messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `questionnaire_results`
--
ALTER TABLE `questionnaire_results`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `questions`
--
ALTER TABLE `questions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
