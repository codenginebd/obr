ALTER DATABASE book_rental_dev CHARACTER SET utf8 COLLATE utf8_unicode_ci;

//To change column to be able to store unicode value mysql database following commands should be run

//For author table

ALTER TABLE book_rental_dev.book_rental_author MODIFY COLUMN name_bn VARCHAR(255)
CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;

ALTER TABLE book_rental_dev.book_rental_author MODIFY COLUMN description_bn VARCHAR(255)
CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;

//For Publisher table
ALTER TABLE book_rental_dev.book_rental_bookpublisher MODIFY COLUMN name_bn VARCHAR(255)
CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;

ALTER TABLE book_rental_dev.book_rental_bookpublisher MODIFY COLUMN description_bn VARCHAR(255)
CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;