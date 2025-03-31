-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 29, 2025 at 07:26 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `krojacki_salon`
--

-- --------------------------------------------------------

--
-- Table structure for table `istorija_kupovina`
--

CREATE TABLE `istorija_kupovina` (
  `istorija_kupovina_id` int(11) NOT NULL,
  `proizvod_id` int(11) NOT NULL,
  `korisnik_id` int(11) NOT NULL,
  `kolicina` int(11) NOT NULL,
  `ukupna_cena` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `istorija_kupovina`
--

INSERT INTO `istorija_kupovina` (`istorija_kupovina_id`, `proizvod_id`, `korisnik_id`, `kolicina`, `ukupna_cena`) VALUES
(39, 23, 24, 1, 5000),
(40, 25, 24, 1, 2000),
(41, 26, 24, 1, 1000),
(42, 23, 26, 1, 5000),
(43, 26, 23, 1, 1000),
(44, 26, 23, 1, 1000),
(45, 26, 23, 1, 1000);

-- --------------------------------------------------------

--
-- Table structure for table `komentari`
--

CREATE TABLE `komentari` (
  `komentar_id` int(11) NOT NULL,
  `tekst_komentara` varchar(500) NOT NULL,
  `proizvod_id` int(11) NOT NULL,
  `korisnik_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `komentari`
--

INSERT INTO `komentari` (`komentar_id`, `tekst_komentara`, `proizvod_id`, `korisnik_id`) VALUES
(32, 'odlicne patike', 23, 25),
(33, 'kvalitetna jakna', 24, 25);

-- --------------------------------------------------------

--
-- Table structure for table `korisnici`
--

CREATE TABLE `korisnici` (
  `id` int(11) NOT NULL,
  `username` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL,
  `email` varchar(200) NOT NULL,
  `godina_rodjenja` year(4) NOT NULL,
  `profilna_slika` varchar(500) NOT NULL DEFAULT '/src/assets/slike_korisnici/default-slika.png',
  `trenutno_stanje_novca` float NOT NULL DEFAULT 0,
  `vrsta_korisnika` enum('krojac','kupac','admin','') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `korisnici`
--

INSERT INTO `korisnici` (`id`, `username`, `password`, `email`, `godina_rodjenja`, `profilna_slika`, `trenutno_stanje_novca`, `vrsta_korisnika`) VALUES
(14, 'admin', 'admin123', 'admin@raf.rs', '2000', '', 0, 'admin'),
(23, 'mmikic', 'mika123', 'mika@raf.rs', '2003', '/src/assets/slike_korisnici/robot.jpg', 7000, 'krojac'),
(24, 'zika', 'zika123', 'zika@raf.rs', '2001', '/src/assets/slike_korisnici/default-slika.png', 2000, 'kupac'),
(25, 'pera', 'pera123', 'pera@raf.rs', '2008', '/src/assets/slike_korisnici/defaul2.jpg', 6000, 'krojac'),
(26, 'stefan', 'stefan123', 'stefan@gmail.com', '2004', '/src/assets/slike_korisnici/covek.jpg', 45000, 'kupac');

-- --------------------------------------------------------

--
-- Table structure for table `korpa`
--

CREATE TABLE `korpa` (
  `korpa_id` int(11) NOT NULL,
  `proizvod_id` int(11) NOT NULL,
  `korisnik_id` int(11) NOT NULL,
  `kolicina` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `korpa`
--

INSERT INTO `korpa` (`korpa_id`, `proizvod_id`, `korisnik_id`, `kolicina`) VALUES
(97, 25, 23, 1);

-- --------------------------------------------------------

--
-- Table structure for table `proizvodi`
--

CREATE TABLE `proizvodi` (
  `proizvod_id` int(11) NOT NULL,
  `korisnik_id` int(11) NOT NULL,
  `naziv_proizvoda` varchar(500) NOT NULL,
  `opis` varchar(500) NOT NULL,
  `materijal` varchar(500) NOT NULL,
  `mere` float NOT NULL,
  `cena` float NOT NULL,
  `kolicina` int(200) NOT NULL DEFAULT 0,
  `proizvod_slika` varchar(300) NOT NULL DEFAULT '/src/assets/slike_proizvodi/default_proizvod_slika.png'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `proizvodi`
--

INSERT INTO `proizvodi` (`proizvod_id`, `korisnik_id`, `naziv_proizvoda`, `opis`, `materijal`, `mere`, `cena`, `kolicina`, `proizvod_slika`) VALUES
(23, 23, 'patike', 'crvene puma patike', 'guma', 43, 5000, 4998, '/src/assets/slike_proizvodi/puma.jpg'),
(24, 23, 'jakna', 'topla, crna jakna', 'koza', 180, 10000, 10000, '/src/assets/slike_proizvodi/jakna.jpg'),
(25, 25, 'carape', 'bele nike carape', 'vuna', 38, 2000, 1999, '/src/assets/slike_proizvodi/carape.jpg'),
(26, 25, 'majica', 'crvena majica', 'pamuk', 150, 1000, 996, '/src/assets/slike_proizvodi/majica.jpg'),
(27, 25, 'duks', 'sareni duks rock fam', 'pamuk', 200, 6500, 6500, '/src/assets/slike_proizvodi/duks.jpg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `istorija_kupovina`
--
ALTER TABLE `istorija_kupovina`
  ADD PRIMARY KEY (`istorija_kupovina_id`),
  ADD KEY `korisnik_id` (`korisnik_id`),
  ADD KEY `proizvod_id` (`proizvod_id`);

--
-- Indexes for table `komentari`
--
ALTER TABLE `komentari`
  ADD PRIMARY KEY (`komentar_id`),
  ADD KEY `korisnik_id` (`korisnik_id`),
  ADD KEY `proizvod_id` (`proizvod_id`);

--
-- Indexes for table `korisnici`
--
ALTER TABLE `korisnici`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `korpa`
--
ALTER TABLE `korpa`
  ADD PRIMARY KEY (`korpa_id`),
  ADD KEY `korisnik_id` (`korisnik_id`),
  ADD KEY `proizvod_id` (`proizvod_id`);

--
-- Indexes for table `proizvodi`
--
ALTER TABLE `proizvodi`
  ADD PRIMARY KEY (`proizvod_id`),
  ADD KEY `korisnik_id` (`korisnik_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `istorija_kupovina`
--
ALTER TABLE `istorija_kupovina`
  MODIFY `istorija_kupovina_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `komentari`
--
ALTER TABLE `komentari`
  MODIFY `komentar_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `korisnici`
--
ALTER TABLE `korisnici`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `korpa`
--
ALTER TABLE `korpa`
  MODIFY `korpa_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=98;

--
-- AUTO_INCREMENT for table `proizvodi`
--
ALTER TABLE `proizvodi`
  MODIFY `proizvod_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `istorija_kupovina`
--
ALTER TABLE `istorija_kupovina`
  ADD CONSTRAINT `istorija_kupovina_ibfk_1` FOREIGN KEY (`korisnik_id`) REFERENCES `korisnici` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `istorija_kupovina_ibfk_2` FOREIGN KEY (`proizvod_id`) REFERENCES `proizvodi` (`proizvod_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `komentari`
--
ALTER TABLE `komentari`
  ADD CONSTRAINT `komentari_ibfk_1` FOREIGN KEY (`korisnik_id`) REFERENCES `korisnici` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `komentari_ibfk_2` FOREIGN KEY (`proizvod_id`) REFERENCES `proizvodi` (`proizvod_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `korpa`
--
ALTER TABLE `korpa`
  ADD CONSTRAINT `korpa_ibfk_1` FOREIGN KEY (`korisnik_id`) REFERENCES `korisnici` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `korpa_ibfk_2` FOREIGN KEY (`proizvod_id`) REFERENCES `proizvodi` (`proizvod_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `proizvodi`
--
ALTER TABLE `proizvodi`
  ADD CONSTRAINT `proizvodi_ibfk_1` FOREIGN KEY (`korisnik_id`) REFERENCES `korisnici` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
