# NBA Match Predictor

A machine learning system that predicts NBA game outcomes using historical box score data and advanced feature engineering.

![Home Page](screenshots/home_page.png)

## Overview

This project uses a Ridge Classifier trained on NBA game data from 2016-2025 to predict upcoming game winners. The model achieves **66.02% backtesting accuracy** using walk-forward validation by season.

## Features

### Model Features
- **Rolling averages** (10-game window) for all box score statistics
- **Exponentially weighted moving averages** (EWM) - weights recent games more heavily
- **Rest days & back-to-backs** - fatigue indicators
- **Season win percentage** - cumulative team strength
- **Opponent win percentage** - strength of schedule
- **Head-to-head record** - historical matchup performance
- **Win/loss streaks** - momentum indicators

### Application Features
- Live prediction tracking with accuracy monitoring
- Streamlit dashboard with team filtering
- Rolling accuracy and cumulative performance charts
- Daily automated prediction updates

### Team-Specific Styling
Select any team to see predictions filtered and styled with team colors.

![Team Styling](screenshots/team.png)

## Tech Stack

- **Python 3.13**
- **scikit-learn** - Ridge Classifier, SelectKBest feature selection
- **pandas** - data manipulation
- **Streamlit** - web dashboard
- **Altair** - interactive charts
- **XGBoost** - alternative model (65.28% accuracy)

## Project Structure

```
nba-match-predictor/
├── app.py                  # Streamlit dashboard
├── predict.ipynb           # Model training & prediction generation
├── get_data_live.ipynb     # Data scraping & result tracking
├── nba_games.csv           # Historical game data (2016-2025)
├── data/
│   ├── predictions.csv         # Upcoming predictions
│   ├── prediction_history.csv  # Completed predictions with results
│   └── upcoming_games_2026.csv # Schedule for current season
├── images/                 # Team logos
└── utils/
    └── constants/          # Team colors & CSS styling
```

## Installation

```bash
git clone https://github.com/teaghanjohnson/nba-match-predictor.git
cd nba-match-predictor

pip install pandas scikit-learn streamlit altair xgboost

streamlit run app.py
```

## Usage

### Generate Predictions
1. Open `predict.ipynb` in Jupyter
2. Run all cells to train the model and generate predictions
3. Predictions are saved to `data/predictions.csv`

### Update Results
1. Open `get_data_live.ipynb`
2. Run the last cell to scrape latest scores and update prediction results
3. Completed predictions are archived to `data/prediction_history.csv`

### View Dashboard
```bash
streamlit run app.py
```

## Model Performance

| Model | Backtesting Accuracy |
|-------|---------------------|
| Ridge Classifier | 66.02% |
| XGBoost | 65.28% |

Live accuracy is tracked separately and may differ from backtesting.

![Model Performance](screenshots/model_performance.png)

## Methodology

### Walk-Forward Backtesting
The model uses walk-forward validation to prevent data leakage:
1. Train on seasons prior to test season
2. Apply SelectKBest (k=50) feature selection within training fold
3. Predict test season outcomes
4. Repeat for each season from 2018-2025

### Feature Selection
SelectKBest with f_classif scoring selects the top 50 features from 400+ candidates, including rolling stats, EWM stats, and engineered features.

## What I Tried (That Didn't Improve Accuracy)

- **Gradient Boosting**: 61.12% accuracy
- **Sample weighting** for recent seasons: No improvement
- **Filtering to last 4 seasons only**: Slight decrease

These experiments suggest ~66% is likely the ceiling for box-score-only features.

## Future Improvements

- Add player-level data (injuries, rest, minutes distribution)
- Incorporate betting line movement
- Add travel distance/timezone features
- Ensemble multiple models

## Connect

- [LinkedIn](https://www.linkedin.com/in/teaghan-johnson-510b95324)
- [GitHub](https://github.com/teaghanjohnson)

## License

MIT
