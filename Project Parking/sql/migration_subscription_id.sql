-- ΕΚΤΕΛΕΣΗ ΜΟΝΟ ΜΕΤΑ ΑΠΟ BACKUP της υπάρχουσας βάσης.
-- Για παλιές εγκαταστάσεις: ενεργοποιεί το AUTO_INCREMENT της συνδρομής.
-- Η υπάρχουσα πρωτεύουσα κλείδα διατηρείται. Δεν διαγράφονται εγγραφές.
ALTER TABLE `subscription`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'KEY';
