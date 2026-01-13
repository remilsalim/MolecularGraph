# Molecular Side Effect Predictor™ 💊

A proprietary machine learning application designed to predict potential side effects of drug molecules based on their molecular formulas. Developed by [remilsalim](https://github.com/remilsalim).

## Overview

The **Molecular Side Effect Predictor™** leverages a Random Forest classifier trained on chemical data from PubChem to provide multi-label predictions of side effects. This tool is part of the **Molecular Graph™** product suite.

## Features

- **Molecular Formula Search**: Interactive autocomplete search for chemical formulas (e.g., `C6H12O6`, `H3N`).
- **Real-time Inference**: Powered by a Random Forest model with automatic feature extraction.
- **Engaging UI**: Modern Streamlit interface with dark mode support, proprietary branding, and funny chemistry facts during processing.
- **Reference Data**: Provides atomic details and database matching for searched compounds.

## Project Structure

- `app.py`: The main Streamlit application.
- `Molecular_Graph_Test1.ipynb`: Research notebook containing model training and data preparation logic.
- `my_pickles_extracted/`: Directory containing pre-trained models (`model.joblib`), encoders (`mlb.joblib`), and processed datasets.
- `drugs.pkl`, `side_effects.pkl`: Primary data sources.

## Installation & Usage

### Prerequisites

Ensure you have Python installed. It is recommended to use a virtual environment.

### Dependencies

Install the required packages:

```bash
pip install streamlit joblib pandas scikit-learn rdkit-pypi torch torch-geometric
```

### Running the App

Navigate to the project directory and run:

```bash
streamlit run app.py
```

## Ownership & Trademark

**Molecular Graph™** and **Molecular Side Effect Predictor™** are proprietary products.
© 2026 [remilsalim](https://github.com/remilsalim). All rights reserved.

---
*Stay Curious. Have all the solutions!* 🧪
