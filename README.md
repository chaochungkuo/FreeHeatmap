# FreeHeatmap

## Overview
FreeHeatmap is a tool for generating heatmaps from CSV files. It allows you to customize the colors, scales, and labels of the heatmap, and export it as a PNG image. The tool is built using the Dash web framework and Plotly library in Python.

## Features
- Generate heatmaps from a CSV file
- Customize colors, scales, and labels
- Export heatmaps as a PNG image

## Installation
To install the FreeHeatmap tool, clone the repository and install the dependencies:
```bash
git clone https://github.com/chaochungkuo/FreeHeatmap.git
cd FreeHeatmap
pip install -r requirements.txt
```

## Usage
To run the FreeHeatmap application, use the following command:
```bash
python src/app.py
```
This will start the Dash application, and you can access it in your web browser at `http://localhost:8051/freeheatmap/`.

## Configuration
You can customize the heatmap by editing the configuration options in the web interface. Options include:
- Color Scheme
- Scale
- Labels
- Clustering options
- Figure dimensions

## Examples
Here are some examples of how to use FreeHeatmap:
1. Upload a CSV file containing your data.
2. Configure the heatmap settings using the provided options.
3. Generate and view the heatmap in the web interface.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
