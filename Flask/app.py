import pickle
from flask import Flask, request, render_template
app = Flask(__name__)

# Load the machine learning model
model = pickle.load(open(r"C:\Users\rajes\Downloads\SHARE PRICE ESTIMATION\SHARE PRICE ESTIMATION 1\share price estimation\lr (1).pkl", "rb"))

# List of possible companies for one-hot encoding
possible_companies = ["AMD","ASUS","INTEL","MSI","NVIDIA"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/inner-page")
def inner_page():
    return render_template('inner-page.html')

@app.route("/prediction")
def prediction():
    return render_template('prediction.html')

@app.route("/result", methods=['POST'])
def result():
    try:
        # Extract form data and convert to appropriate data types
        low = float(request.form["low"])
        high = float(request.form["high"])
        volume = float(request.form["volume"])
        open_value = float(request.form["open"])
        company = request.form["company"]  # Keep it as a string
        year = int(request.form["year"])
        month = request.form["month"]  # Keep it as a string
        day = int(request.form["day"])

        # Preprocess the "month" and "company" fields
        # For "month," you can map month names to numeric values
        month_to_numeric = {
            "January": 1,
            "February": 2,
            # Add more months as needed
        }
        month_numeric = month_to_numeric.get(month, 0)  # Default to 0 if month is not found

        # One-hot encode the 'company' feature
        company_one_hot = [1 if company == c else 0 for c in possible_companies]

        # Make predictions
        input_features = [open_value, high, low, volume, year, month_numeric, day] + company_one_hot[:2]  # Use the first two elements of one-hot encoding
        # Ensure that the input_features match the expected input dimension of your model

        # Make predictions
        xx = model.predict([input_features[:-1]])  # Remove the last element (extra feature)
        out = xx[0]
        prediction_result = "Forecasted closing price on {}/{}/{} is $ {}".format(day, month, year, out)

        return render_template("result.html", p=prediction_result)
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return render_template("error.html", error=error_message)

@app.route("/error")
def error():
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=False)
