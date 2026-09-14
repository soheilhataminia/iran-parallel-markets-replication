# The Behavior of Parallel Markets in Iran’s Inflationary Economy: Long-Run Relations and the Predictability of Price Changes

This repository contains the data and code used to reproduce the empirical analysis in the study.

## Repository Structure

- `data/` — monthly analysis dataset
- `stage_1_baseline_vecm/` — baseline nominal VECM
- `stage_2_rank_and_restriction_inference/` — rank and restriction inference
- `stage_3_cpi_adjusted_robustness/` — CPI-adjusted robustness
- `stage_4_xau_augmented_robustness/` — world-gold-price robustness
- `stage_5_cholesky_ordering_sensitivity/` — Cholesky-ordering sensitivity
- `stage_6_predictive_dynamics_and_forecasting/` — local projections, forecasting, and robustness analyses

## Data

The analysis uses 122 monthly observations from April 2016 to May 2026. Variable definitions and original data sources are documented in `data/README.md`.

## Software

Stages 1, 3, 4, and 5 use EViews.  
Stages 2 and 6 use Python.

Each stage contains its own README with the relevant files and execution details.
