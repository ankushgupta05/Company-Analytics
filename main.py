from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load CSV data
csv_file_path = 'cleaned_dump.csv'

try:
    # Attempt to read the CSV file
    df = pd.read_csv(csv_file_path)
    index_name_list = df['index_name'].unique().tolist()
except Exception as e:
    # Handle the exception if CSV cannot be read
    print(f"Error reading CSV file: {e}")
    df = pd.DataFrame()  # Set df as an empty DataFrame if there's an error
    index_name_list = []

@app.route('/', methods=['GET', 'POST'])
def display_index():
    selected_index = None
    filtered_data = {}  # Initialize with an empty dictionary

    if request.method == 'POST':
        try:
            # Check if the clear button was pressed
            if request.form.get('clear'):
                selected_index = None  # Clear the selected index
            else:
                selected_index = request.form.get('index_name')  # Retrieve the selected value from the form


            # Filter data based on the selected index (if any)
            if selected_index and not df.empty:
                filtered_rows = df[df['index_name'] == selected_index]
                
                filtered_data = {
                    "index_date": filtered_rows['index_date'].tolist(),
                    "volume": filtered_rows['volume'].tolist(),
                    "open_index_value": filtered_rows['open_index_value'].tolist(),
                    "high_index_value": filtered_rows['high_index_value'].tolist(),
                    "low_index_value": filtered_rows['low_index_value'].tolist(),
                    "change_percent": filtered_rows['change_percent'].tolist(),
                    "closing_index_value": filtered_rows['closing_index_value'].tolist(),
                    "turnover_rs_cr": filtered_rows['turnover_rs_cr'].tolist(),
                    "pe_ratio": filtered_rows['pe_ratio'].tolist(),
                    "pb_ratio": filtered_rows['pb_ratio'].tolist(),
                    "div_yield": filtered_rows['div_yield'].tolist()
                }
            else:
                # If no index is selected, or df is empty, return an empty dictionary
                filtered_data = {}

        except KeyError as e:
            print(f"KeyError: Column not found in the CSV data - {e}")
            filtered_data = {"error": "Requested column not found in the CSV data."}
        except Exception as e:
            print(f"Error processing data: {e}")
            filtered_data = {"error": "An error occurred while processing the data."}

    return render_template(
        'index.html',
        index_name_list=index_name_list,
        selected_index=selected_index,
        filtered_data=filtered_data
    )

if __name__ == '__main__':
    app.run(debug=True)
