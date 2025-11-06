# Netflix vs Disney+: Award Analysis

This project analyzes **Netflix** and **Disney+** award performance across the **Oscars** and **Golden Globes**.  
It was developed as part of a **data visualization week** at the bootcamp and demonstrates skills in **data cleaning**, **analysis**, and **visual storytelling** with Python.

---

## Project Overview

The initial goal was to compare which platform has more awards in the **Best Feature category**.  
During analysis, it was discovered that **Disney+ has none** in this category — therefore, the **Best Animated Feature** was added to make the comparison fairer.  

For the **Golden Globe Awards**, several “Best Feature” categories were considered, including:
- Best Motion Picture – Drama  
- Best Motion Picture – Musical or Comedy  
- Best Television Series – Drama  
- Best Television Series – Musical or Comedy  
- Best Television Limited Series or Anthology Series  
- Best Motion Picture – Non-English Language  

---

## Files

| File | Description |
|------|--------------|
| `oscar_utils.py` | Functions for data cleaning and Oscar matching |
| `golden_globe_utils.py` | Functions for data cleaning and Golden Globe matching |
| `combined_analysis.py` | Main script combining both analyses and generating visualizations |
| `data/` | Raw CSV datasets (sourced from [Kaggle](https://www.kaggle.com/)) |
| `...charts/` | Output plots and visualizations |

---

## Tools & Libraries

- **Python 3**  
- **pandas** — data manipulation  
- **matplotlib** — visualization  

---

## How to Run

```bash
pip install pandas matplotlib
python combined_analysis.py
```
