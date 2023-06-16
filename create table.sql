CREATE DATABASE IF NOT EXISTS mydb; 
USE mydb; 

CREATE TABLE `Daily Trends in FII / FPI Derivative Trades` (
  `Reporting Date` DATE,
  `Derivative Products` VARCHAR(255),
  `Buy No. of Contracts` DECIMAL(18, 2),
  `Buy Amount in Crore` DECIMAL(18, 2),
  `Sell No. of Contracts` DECIMAL(18, 2),
  `Sell Amount in crore` DECIMAL(18, 2),
  `Open Interest at the end of the date No. of Contracts` DECIMAL(18, 2),
  `Open Interest at the end of the date Amount in Crore` DECIMAL(18, 2)
);

CREATE TABLE `Daily Trends in FII / FPI Investments` (
    `Reporting Date` DATE,
    `Debt/Equity` VARCHAR(255),
    `Investment Route` VARCHAR(255),
    `Gross Purchases` DECIMAL(18, 2),
    `Gross Sales` DECIMAL(18, 2),
    `Net Investment(Rs Crore)` DECIMAL(18, 2),
    `Net InvestmentUS($) million` DECIMAL(18, 2)
);

CREATE TABLE `Conversion value` (
	`Reporting Date` DATE,
    `Conversion(1 USD TO INR)*` FLOAT
);

