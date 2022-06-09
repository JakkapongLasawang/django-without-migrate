CREATE TABLE book_ (
  id serial4 NOT NULL,
  title VARCHAR(128) NOT NULL,
  number_of_pages INT NOT NULL,
  author VARCHAR(128) NOT NULL,
  quantity INT NOT NULL,
  published TIMESTAMP WITH TIME ZONE NOT NULL,
  CONSTRAINT book PRIMARY KEY (id)
);