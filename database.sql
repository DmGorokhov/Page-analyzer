DROP TABLE IF EXISTS url_checks;
DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
  id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  name VARCHAR(255) UNIQUE NOT NULL,
  created_at timestamp NOT NULL
);

CREATE TABLE url_checks (
  id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  url_id bigint REFERENCES urls (id),
  status_code int,
  h1 VARCHAR(50),
  title VARCHAR(50),
  description VARCHAR(255),
  created_at timestamp NOT NULL
);