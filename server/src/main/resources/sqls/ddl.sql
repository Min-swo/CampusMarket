CREATE TABLE `User`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL
);

CREATE TABLE `Cart`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `userId` BIGINT NOT NULL,
    `totalPrice` BIGINT NOT NULL
);

CREATE TABLE `CartItem`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `cartId` BIGINT NOT NULL,
    `itemId` BIGINT NOT NULL,
    `quantity` BIGINT NOT NULL
);

CREATE TABLE `Item`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `productId` BIGINT NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `stock` BIGINT NOT NULL,
    `unit` BIGINT NOT NULL,
    `unitPrice` BIGINT NOT NULL,
    `price` BIGINT NOT NULL,
    `saleRate` BIGINT NOT NULL,
    `itemType` ENUM('PARTNER', 'OTHERS') NOT NULL,
    `deliveryType` ENUM('FREE', 'CONDITIONAL') NOT NULL
);

CREATE TABLE `MembershipItem`(
     `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
     `membershipUnitPrice` BIGINT NOT NULL,
     `membershipPrice` BIGINT NOT NULL,
     `membershipSaleRate` BIGINT NOT NULL
);

CREATE TABLE `Product`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL
);

CREATE TABLE `Membership`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `type` ENUM('') NOT NULL,
    `price` BIGINT NOT NULL
);

CREATE TABLE `UserMembership`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `userId` BIGINT NOT NULL,
    `membershipId` BIGINT NOT NULL,
    `paymentDate` DATE NOT NULL
);

ALTER TABLE
    `UserMembership` ADD CONSTRAINT `usermembership_userid_foreign` FOREIGN KEY(`userId`) REFERENCES `User`(`id`);
ALTER TABLE
    `CartItem` ADD CONSTRAINT `cartitem_itemid_foreign` FOREIGN KEY(`itemId`) REFERENCES `Item`(`id`);
ALTER TABLE
    `Item` ADD CONSTRAINT `item_productid_foreign` FOREIGN KEY(`productId`) REFERENCES `Product`(`id`);
ALTER TABLE
    `UserMembership` ADD CONSTRAINT `usermembership_membershipid_foreign` FOREIGN KEY(`membershipId`) REFERENCES `Membership`(`id`);
ALTER TABLE
    `CartItem` ADD CONSTRAINT `cartitem_cartid_foreign` FOREIGN KEY(`cartId`) REFERENCES `Cart`(`id`);
ALTER TABLE
    `Cart` ADD CONSTRAINT `cart_userid_foreign` FOREIGN KEY(`userId`) REFERENCES `User`(`id`);
ALTER TABLE
    `Item` ADD CONSTRAINT `item_id_foreign` FOREIGN KEY(`id`) REFERENCES `MembershipItem`(`id`);