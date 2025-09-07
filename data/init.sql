CREATE TABLE keyword
(
    id         INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
    word       VARCHAR(256) NOT NULL,
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_deleted BOOLEAN      NOT NULL DEFAULT FALSE,
    deleted_at DATETIME,

    UNIQUE KEY uk_keyword_001 (word)

) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;


CREATE TABLE scraped_product
(
    id                   INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name                 VARCHAR(256) NOT NULL,
    channel              VARCHAR(64)  NOT NULL,
    channel_product_id   VARCHAR(256) NOT NULL,
    is_tracking_required BOOLEAN      NOT NULL DEFAULT FALSE,
    keyword_id           INT          NULL,
    created_at           DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT frk_scraped_product_001 FOREIGN KEY (keyword_id) REFERENCES keyword (id) ON DELETE RESTRICT

) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX idx_scraped_product_001 ON scraped_product (channel);
CREATE INDEX idx_scraped_product_002 ON scraped_product (channel_product_id);
CREATE INDEX idx_scraped_product_003 ON scraped_product (name);


CREATE TABLE scraped_product_detail
(
    id                 INTEGER        NOT NULL AUTO_INCREMENT PRIMARY KEY,
    link               VARCHAR(1024),
    image_link         VARCHAR(1024),
    price              DECIMAL(10, 0) NOT NULL,
    mall_name          VARCHAR(128),
    product_type       VARCHAR(128),
    brand              VARCHAR(128),
    maker              VARCHAR(128),
    scraped_result     JSON,
    scraped_product_id INTEGER        NOT NULL,
    created_at         DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT frk_scraped_product_detail_001 FOREIGN KEY (scraped_product_id) REFERENCES scraped_product (id) ON DELETE RESTRICT

) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

INSERT INTO keyword (word)
VALUES ('잇츄'),
       ('플라고'),
       ('무무'),
       ('헤이테일'),
       ('냥쌤'),
       ('베터'),
       ('포우장'),
       ('닥터설'),
       ('고래패드');

ALTER TABLE scraped_product
    MODIFY keyword_id INT NULL;

CREATE TABLE sitemap_source
(
    id             INT           NOT NULL AUTO_INCREMENT PRIMARY KEY,
    channel        VARCHAR(64)   NOT NULL,
    sitemap_url    VARCHAR(1024) NOT NULL,
    file_path      VARCHAR(1024) NOT NULL,
    created_at     DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_synced_at DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

ALTER TABLE scraped_product
    ADD COLUMN sitemap_source_id INT NULL,
    ADD INDEX idx_scraped_product_004 (sitemap_source_id),
    ADD CONSTRAINT frk_scraped_product_002 FOREIGN KEY (sitemap_source_id) REFERENCES sitemap_source (id) ON DELETE RESTRICT;
