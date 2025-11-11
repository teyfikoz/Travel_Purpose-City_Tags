# TravelPurpose Examples

This directory contains example notebooks demonstrating how to use the TravelPurpose library.

## Notebooks

### 01_quickstart.ipynb
Introduction to the basic features:
- Loading the library
- Predicting travel purposes for cities
- Viewing raw tags from sources
- Searching for cities
- Understanding confidence scores
- Batch processing multiple cities

**Recommended for:** First-time users

### 02_advanced_usage.ipynb
Advanced features and customization:
- Custom tag source weighting
- Exploring the ontology structure
- Analyzing tag-to-category mappings
- Dataset analysis
- Running the data pipeline
- Building custom classifiers
- Comparative city analysis

**Recommended for:** Users who want to customize or extend the library

## Running the Notebooks

1. Install JupyterLab or Jupyter Notebook:
```bash
pip install jupyterlab
```

2. Launch Jupyter:
```bash
jupyter lab
```

3. Navigate to the examples directory and open a notebook

## Prerequisites

Make sure you have installed the travelpurpose package:

```bash
pip install travelpurpose
# or for development
pip install -e ".[dev]"
```

## Example Output

Expected output when running `predict_purpose("Istanbul")`:

```python
{
    'main': ['Culture_Heritage', 'Transit_Gateway', 'Leisure'],
    'sub': ['UNESCO_Site', 'Old_Town', 'Mega_Air_Hub', 'Gastronomy'],
    'confidence': 0.86
}
```

## Need Help?

- Check the [main README](../README.md)
- Open an [issue](https://github.com/teyfikoz/Travel_Purpose-City_Tags/issues)
- Read the [documentation](https://github.com/teyfikoz/Travel_Purpose-City_Tags)
