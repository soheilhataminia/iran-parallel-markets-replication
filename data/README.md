# Data

This directory contains the monthly analysis dataset used in the replication package.

## File

`data.xlsx`

## Coverage

April 2016 to May 2026.

## Variables and Sources

| Variable | Description | Source |
|---|---|---|
| USD | Free-market U.S. dollar exchange rate | Tehran Gold and Jewelry Union (TGJU) |
| GCOIN | Emami gold coin price | Tehran Gold and Jewelry Union (TGJU) |
| STOCK | Tehran Exchange Dividend and Price Index (TEDPIX) | Tehran Securities Exchange Technology Management Co. (TSETMC) |
| VEHICLE | Purchase-of-vehicles CPI sub-index | Statistical Center of Iran (SCI) |
| HOUSING | Average apartment transaction price per square meter in Tehran | Central Bank of Iran (CBI) and Ministry of Roads and Urban Development (MRUD) |
| CPI | Consumer Price Index | Statistical Center of Iran (SCI) |
| XAU | World gold price | World Gold Council (WGC) |

## Data Construction

USD, GCOIN, STOCK, and XAU are monthly averages constructed from the underlying daily observations.

VEHICLE, HOUSING, and CPI are used at their reported monthly frequency.

The replication files contain the preconstructed monthly series used in the empirical analysis. The original daily-to-monthly aggregation is not reproduced in the repository.

## Source References

- Tehran Gold and Jewelry Union (TGJU), historical market data for the free-market U.S. dollar exchange rate and Emami gold coin price.
- Tehran Securities Exchange Technology Management Co. (TSETMC), historical TEDPIX data.
- Statistical Center of Iran (SCI), Consumer Price Index and purchase-of-vehicles CPI sub-index.
- Central Bank of the Islamic Republic of Iran (CBI) and Ministry of Roads and Urban Development (MRUD), Tehran residential property transaction-price data.
- World Gold Council (WGC), historical world gold-price data.
