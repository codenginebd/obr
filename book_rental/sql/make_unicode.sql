ALTER DATABASE book_rental_dev CHARACTER SET utf8 COLLATE utf8_unicode_ci;

//To change column to be able to store unicode value mysql database following commands should be run

//For author table

ALTER TABLE book_rental_dev.book_rental_author MODIFY COLUMN name_2 VARCHAR(500)
CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;

ALTER TABLE book_rental_dev.book_rental_author MODIFY COLUMN description_2 text
CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;

//For Publisher table
ALTER TABLE book_rental_dev.book_rental_bookpublisher MODIFY COLUMN name_2 VARCHAR(500)
CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;

ALTER TABLE book_rental_dev.book_rental_bookpublisher MODIFY COLUMN description_2 text
CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;

//For Book table
ALTER TABLE book_rental_dev.book_rental_book MODIFY COLUMN title_2 VARCHAR(500)
CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;

ALTER TABLE book_rental_dev.book_rental_book MODIFY COLUMN subtitle_2 text
CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;

ALTER TABLE book_rental_dev.book_rental_book MODIFY COLUMN description_2 text
CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;

//Logger table
ALTER TABLE book_rental_dev.logger_errorlog MODIFY COLUMN url varchar(500)
CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;

ALTER TABLE book_rental_dev.logger_errorlog MODIFY COLUMN stacktrace text
CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;

//Product Category table
ALTER TABLE book_rental_dev.ecommerce_productcategory MODIFY COLUMN name_2 varchar(500)
CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;