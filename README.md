# AI-visualizer
AI-Powered Data Visualizer
A web application that automatically extracts structured data from unstructured text (like news articles) and generates interactive visualizations.
About The Project
This project was born from a practical need. Valuable data—such as economic figures, state-wise statistics, or policy impacts—is often "trapped" inside unstructured news articles and reports. For students, researchers, or anyone preparing for competitive exams (like the UPSC), manually extracting this data into a spreadsheet is tedious, time-consuming, and a barrier to quick analysis.
This tool automates the entire workflow.
You simply paste in the full text of an article. The application's backend sends the text to the Google Gemini AI, which has been instructed to:
Read and understand the text.
Extract any structured data it finds and format it as a clean CSV.
Suggest the most appropriate chart type (bar, line, pie) and the correct columns for the X and Y axes.
The Flask backend then uses Pandas to read this data, and Plotly to automatically generate the suggested interactive graph. The result is an instant, insightful visualization created directly from raw text.
Key Features
AI-Powered Data Extraction: Uses the Google Gemini AI to parse unstructured text and extract data into a clean CSV format.
Smart Chart Suggestion: The AI also analyzes the data to suggest the most appropriate chart type and axis configuration.
Automated Visualization: Instantly renders an interactive, web-based graph using Plotly.
Data Transparency: Displays the extracted raw CSV data so you can copy it, paste it into Excel, or verify its accuracy.
Simple Web Interface: A clean, single-page application built with Flask and styled with Tailwind CSS.
Tech Stack
Backend: Python, Flask
Data Processing: Pandas
Data Visualization: Plotly
AI & Asynchronous Requests: Google Gemini API & aiohttp
Frontend: HTML, Tailwind CSS, Jinja2
