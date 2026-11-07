-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- Εξυπηρετητής: 127.0.0.1
-- Χρόνος δημιουργίας: 20 Φεβ 2022 στις 13:00:46
-- Έκδοση διακομιστή: 10.4.22-MariaDB
-- Έκδοση PHP: 8.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Βάση δεδομένων: `parking`
--

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `company`
--

CREATE TABLE `company` (
  `id` int(11) NOT NULL COMMENT 'KEY',
  `afm` text NOT NULL COMMENT 'Α.Φ.Μ.',
  `doy` text NOT NULL COMMENT 'ΔΟΥ',
  `address` text NOT NULL COMMENT 'Διεύθυνση',
  `city` text NOT NULL COMMENT 'Πόλη',
  `telephone` text NOT NULL COMMENT 'Τηλέφωνο',
  `title1` text NOT NULL COMMENT 'Τίτλος 1',
  `title2` text NOT NULL COMMENT 'Τίτλος 2',
  `comment` text NOT NULL COMMENT 'Σχόλια'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Άδειασμα δεδομένων του πίνακα `company`
--

INSERT INTO `company` (`id`, `afm`, `doy`, `address`, `city`, `telephone`, `title1`, `title2`, `comment`) VALUES
(1, '0000000000', 'Πόλη', 'Διεύθυνση αριθμός Τ.Κ.', 'Πόλη', '0000000000', 'Τίτλος 1', '', 'Αρχικοποίηση');

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `costs`
--

CREATE TABLE `costs` (
  `id` int(10) UNSIGNED NOT NULL COMMENT 'KEY',
  `timecost` time NOT NULL COMMENT 'Χρόνος κόστους σε λεπτά.',
  `moneycost` double NOT NULL COMMENT 'Κόστος €',
  `comments` text NOT NULL COMMENT 'Σχόλια'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Άδειασμα δεδομένων του πίνακα `costs`
--

INSERT INTO `costs` (`id`, `timecost`, `moneycost`, `comments`) VALUES
(0, '00:00:00', 0, 'Αρχικοποίηση - Τιμή χωρίς Φ.Π.Α.'),
(1, '00:20:00', 0, ' '),
(2, '02:00:00', 3.23, ''),
(3, '04:00:00', 0.81, ''),
(4, '01:00:00', 0.4, '');

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `costsub`
--

CREATE TABLE `costsub` (
  `id` int(10) UNSIGNED NOT NULL COMMENT 'KEY',
  `subdays` int(11) NOT NULL COMMENT 'Μέρες συνδρομής',
  `paysub` double NOT NULL COMMENT 'Κόστος συνδρομής',
  `comments` text NOT NULL COMMENT 'Σχόλια'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Άδειασμα δεδομένων του πίνακα `costsub`
--

INSERT INTO `costsub` (`id`, `subdays`, `paysub`, `comments`) VALUES
(0, 0, 0, 'Αρχικοποίηση - Τιμή χωρίς Φ.Π.Α. '),
(1, 7, 40.32, ''),
(2, 15, 68.55, ''),
(3, 30, 112.9, '');

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `door`
--

CREATE TABLE `door` (
  `id` int(11) NOT NULL COMMENT 'KEY',
  `stagein` int(11) NOT NULL COMMENT 'Κατάσταση πόρτας εισόδου',
  `stageout` int(11) NOT NULL COMMENT 'Κατάσταση πόρτας εξόδου',
  `comments` text NOT NULL COMMENT 'Κατάσταση πόρτας'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Άδειασμα δεδομένων του πίνακα `door`
--

INSERT INTO `door` (`id`, `stagein`, `stageout`, `comments`) VALUES
(1, 0, 0, 'Κατάσταση πόρτας εισόδου και εξόδου');

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `fpa`
--

CREATE TABLE `fpa` (
  `id` int(11) NOT NULL COMMENT 'KEY',
  `costfpa` int(11) NOT NULL COMMENT 'ΦΠΑ'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Άδειασμα δεδομένων του πίνακα `fpa`
--

INSERT INTO `fpa` (`id`, `costfpa`) VALUES
(1, 24);

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `inputcar`
--

CREATE TABLE `inputcar` (
  `inputnumber` int(10) UNSIGNED NOT NULL COMMENT 'Αριθμός εισόδου - KEY',
  `ticketnumber` int(11) NOT NULL COMMENT 'Αριθμός εισιτηρίου',
  `datein` date NOT NULL COMMENT 'Ημερομηνία εισόδου',
  `timein` time NOT NULL COMMENT 'Ώρα εισόδου',
  `placenumber` text NOT NULL COMMENT 'Αριθμός πινακίδας',
  `comments` text DEFAULT NULL COMMENT 'Παρατηρήσεις',
  `isout` int(11) NOT NULL COMMENT 'Αν είναι έξω -> 1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Άδειασμα δεδομένων του πίνακα `inputcar`
--

INSERT INTO `inputcar` (`inputnumber`, `ticketnumber`, `datein`, `timein`, `placenumber`, `comments`, `isout`) VALUES
(0, 0, '2022-01-01', '00:00:00', '0', ' Αρχικοποίηση', 1);

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `lockm`
--

CREATE TABLE `lockm` (
  `id` int(11) NOT NULL COMMENT 'KEY',
  `lockout` int(11) NOT NULL COMMENT 'Κλείδωμα Θέσεων\r\nLOCK 1 UNLOCK 0',
  `lockout2` int(11) NOT NULL COMMENT 'Κλείδωμα εταιρείας\r\nLOCK 1 UNLOCK 0',
  `coments` text NOT NULL COMMENT 'Σχόλια'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Άδειασμα δεδομένων του πίνακα `lockm`
--

INSERT INTO `lockm` (`id`, `lockout`, `lockout2`, `coments`) VALUES
(1, 0, 0, 'Κλείδωμα');

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `outputcar`
--

CREATE TABLE `outputcar` (
  `id` int(10) UNSIGNED NOT NULL COMMENT 'KEY',
  `ticketnumber` int(11) NOT NULL COMMENT 'Αριθμός εισιτηρίου ',
  `dateout` date NOT NULL COMMENT 'Ημερομηνία εξόδου ',
  `timeout` time NOT NULL COMMENT 'Ώρα εξόδου',
  `placenumber` text NOT NULL COMMENT 'Αριθμός πινακίδας',
  `pay` double NOT NULL COMMENT 'Πληρωτέο ποσό',
  `subscription` int(11) NOT NULL COMMENT 'Συνδρομή έχει -> 1',
  `comments` text NOT NULL COMMENT 'Παρατηρήσεις'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Άδειασμα δεδομένων του πίνακα `outputcar`
--

INSERT INTO `outputcar` (`id`, `ticketnumber`, `dateout`, `timeout`, `placenumber`, `pay`, `subscription`, `comments`) VALUES
(0, 0, '2022-01-01', '00:00:00', '0', 0, 0, 'Αρχικοποίηση');

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `places`
--

CREATE TABLE `places` (
  `id` int(11) NOT NULL COMMENT 'KEY',
  `remaneplaces` int(11) NOT NULL COMMENT 'Ελεύθερες θέσεις'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Άδειασμα δεδομένων του πίνακα `places`
--

INSERT INTO `places` (`id`, `remaneplaces`) VALUES
(1, 10);

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `subscription`
--

CREATE TABLE `subscription` (
  `id` int(10) UNSIGNED NOT NULL COMMENT 'KEY',
  `firstname` text NOT NULL COMMENT 'Όνομα',
  `lastname` text NOT NULL COMMENT 'Επίθετο',
  `phone` text NOT NULL COMMENT 'Τηλέφωνο',
  `placenumber` text NOT NULL COMMENT 'Αριθμός πινακίδας',
  `datestart` date NOT NULL COMMENT 'Ημερομηνία αρχής',
  `dateend` date NOT NULL COMMENT 'Ημερομηνία τέλους',
  `timestart` time NOT NULL COMMENT 'Ώρα αρχής',
  `timeend` time NOT NULL COMMENT 'Ώρα τέλους',
  `costsub` int(11) NOT NULL COMMENT 'Κόστος συνδρομής 7, 15, 30 μέρες κλπ.',
  `cost` double NOT NULL COMMENT 'Χρέωση σε €',
  `fpa` int(11) NOT NULL COMMENT 'Φ.Π.Α. %',
  `comments` text NOT NULL COMMENT 'Παρατηρήσεις'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Άδειασμα δεδομένων του πίνακα `subscription`
--

INSERT INTO `subscription` (`id`, `firstname`, `lastname`, `phone`, `placenumber`, `datestart`, `dateend`, `timestart`, `timeend`, `costsub`, `cost`, `fpa`, `comments`) VALUES
(0, '×××', '×××', '×××', '×××', '2022-01-01', '2022-01-01', '00:00:00', '00:00:00', 0, 0, 0, 'Αρχικοποίηση');

--
-- Ευρετήρια για άχρηστους πίνακες
--

--
-- Ευρετήρια για πίνακα `company`
--
ALTER TABLE `company`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- Ευρετήρια για πίνακα `costs`
--
ALTER TABLE `costs`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- Ευρετήρια για πίνακα `costsub`
--
ALTER TABLE `costsub`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- Ευρετήρια για πίνακα `door`
--
ALTER TABLE `door`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- Ευρετήρια για πίνακα `fpa`
--
ALTER TABLE `fpa`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- Ευρετήρια για πίνακα `inputcar`
--
ALTER TABLE `inputcar`
  ADD PRIMARY KEY (`inputnumber`) USING BTREE;

--
-- Ευρετήρια για πίνακα `lockm`
--
ALTER TABLE `lockm`
  ADD PRIMARY KEY (`id`);

--
-- Ευρετήρια για πίνακα `outputcar`
--
ALTER TABLE `outputcar`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- Ευρετήρια για πίνακα `places`
--
ALTER TABLE `places`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- Ευρετήρια για πίνακα `subscription`
--
ALTER TABLE `subscription`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- AUTO_INCREMENT για άχρηστους πίνακες
--

--
-- AUTO_INCREMENT για πίνακα `company`
--
ALTER TABLE `company`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'KEY', AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT για πίνακα `costs`
--
ALTER TABLE `costs`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'KEY', AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT για πίνακα `costsub`
--
ALTER TABLE `costsub`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'KEY', AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT για πίνακα `door`
--
ALTER TABLE `door`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'KEY', AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT για πίνακα `fpa`
--
ALTER TABLE `fpa`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'KEY', AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT για πίνακα `inputcar`
--
ALTER TABLE `inputcar`
  MODIFY `inputnumber` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Αριθμός εισόδου - KEY';

--
-- AUTO_INCREMENT για πίνακα `lockm`
--
ALTER TABLE `lockm`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'KEY', AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT για πίνακα `outputcar`
--
ALTER TABLE `outputcar`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'KEY';

--
-- AUTO_INCREMENT για πίνακα `places`
--
ALTER TABLE `places`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'KEY', AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT για πίνακα `subscription`
--
ALTER TABLE `subscription`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'KEY';
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
