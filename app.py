import asyncio  # For handling API calls without freezing the app
import aiohttp  # For making asynchronous web requests
import io       # For reading text as if it were a file
import pandas as pd
import plotly.express as px
from flask import Flask, render_template, request

# --- Block 1: The Import Statements & Setup ---
app = Flask(_name_)

# --- Block 2: The Gemini AI Configuration ---
# This is the "brain" of our AI. 
# We are giving it a very specific, two-part job.
SYSTEM_PROMPT = """


PART 1: The Data
- Extract any structured data you find in the article.
- Format this data as a clean, simple CSV (Comma Separated Values).
- The first row MUST be the column headers.

PART 2: The Chart Suggestion
- After the CSV data, add a separator line: '---CHART---'
- On a new line, suggest the best chart type.
- On the next line, suggest the best column for the X-AXIS.
- On the next line, suggest the best column for the Y-AXIS.

EXAMPLE RESPONSE:
State,Literacy Rate,Internet Penetration
Kerala,94.0,63.0
Delhi,86.2,68.0
Mizoram,91.3,55.0
---CHART---
bar
State
Literacy Rate
"""

# The API URL and Key
API_URL = "https://generativelen.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key="
API_KEY = "" # Handled by the environment

# --- Block 3: The Asynchronous AI Call Function ---
# This function calls the Gemini API
async def call_gemini(article_text):
    payload = {
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"parts": [{"text": article_text}]}],
    }
    
    # We use aiohttp for an async request
    async with aiohttp.ClientSession() as session:
        # Exponential backoff for retries
        for i in range(3): # Max 3 retries
            try:
                async with session.post(API_URL + API_KEY, json=payload) as response:
                    response.raise_for_status() # Raise error for bad responses
                    result = await response.json()
                    
                    if result.get('candidates'):
                        return result['candidates'][0]['content']['parts'][0]['text']
                    else:
                        raise Exception("Invalid API response structure")

            except aiohttp.ClientError as e:
                if i == 2: # Last retry
                    return f"Error: API call failed after retries. {e}"
                await asyncio.sleep(2**i) # 1s, 2s
    return "Error: Could not contact AI service."


# --- Block 4: The Main Route (Handles everything) ---
@app.route('/', methods=['GET', 'POST'])
def index():
    # These variables will be sent to the HTML file
    graph_html = None
    extracted_data = None
    error_message = None

    if request.method == 'POST':
        try:
            article_text = request.form['article_content']
            
            # 1. Call the AI and get the response
            # We use asyncio.run() to execute our async function
            ai_response = asyncio.run(call_gemini(article_text))

            # 2. Split the AI response into its two parts
            if '---CHART---' not in ai_response:
                raise Exception("AI did not return a valid response. " + ai_response)

            parts = ai_response.split('---CHART---')
            csv_data = parts[0].strip()
            chart_info = parts[1].strip().split('\n')
            
            # 3. Parse the AI suggestions
            chart_type = chart_info[0].strip()
            x_col = chart_info[1].strip()
            y_col = chart_info[2].strip()
            
            # 4. Use PANDAS to read the CSV data
            # io.StringIO tricks pandas into reading our string as a file
            data_file = io.StringIO(csv_data)
            df = pd.read_csv(data_file)
            
            # Store the raw CSV to show the user
            extracted_data = csv_data

            # 5. Use PLOTLY to create the suggested graph
            fig = None
            if chart_type == 'bar':
                fig = px.bar(df, x=x_col, y=y_col, title=f"Bar Chart of {y_col} by {x_col}")
            elif chart_type == 'line':
                fig = px.line(df, x=x_col, y=y_col, title=f"Line Chart of {y_col} by {x_col}")
            elif chart_type == 'pie':
                # Pie charts use 'names' and 'values'
                fig = px.pie(df, names=x_col, values=y_col, title=f"Pie Chart of {y_col}")
            else:
                # Default to bar chart if suggestion is weird
                fig = px.bar(df, x=x_col, y=y_col, title=f"Chart of {y_col} by {x_col}")
            
            # 6. Convert the graph to HTML
            if fig:
                graph_html = fig.to_html(full_html=False)

        except Exception as e:
            # Handle any errors
            error_message = f"An error occurred: {e}"

    # 7. Render the page
    # If it was a GET request, it just shows the form.
    # If it was a POST, it now includes the graph, data, and/or an error.
    return render_template('index_ai.html', 
                           graph_html=graph_html, 
                           extracted_data=extracted_data, 
                           error_message=error_message)

# --- Block 5: The "Run" Command ---
if _name_ == '_main_':
    app.run(debug=True)