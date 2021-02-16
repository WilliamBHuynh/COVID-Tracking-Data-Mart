DROP TABLE if exists d_mobility;

CREATE TABLE d_mobility
(
  mobility_key              serial PRIMARY KEY,
  subregion                 VARCHAR(6) NOT NULL,
  province                  VARCHAR(7) NOT NULL,
  retail_and_recreation     VARCHAR(4) NOT NULL,
  grocery_and_pharmacy      VARCHAR(9) NOT NULL,
  parks                     INT NOT NULL,
  transit_stations          INT NOT NULL,
  workplaces                INT NOT NULL,
  residential               INT NOT NULL
);