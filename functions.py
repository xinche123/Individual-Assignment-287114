import pandas as pd
import yfinance as yf
import os
import matplotlib.pyplot as plt
import datetime

user_path = "Login Credentials.csv"

# Create a new csv file if dont have any file
if not os.path.exists(user_path):
    pd.DataFrame(columns=["email", "password"]).to_csv(user_path, index=False)

# Function to register the user
def register_user(email:str,password:str) -> str:
    logins_df = pd.read_csv(user_path)
    if (logins_df["email"] == email).any():
        return "Email already exists in the system."
    new_user = pd.DataFrame({"email":[email],"password": [password]})
    new_user.to_csv(user_path, mode = "a", header = False, index = False)

    return "Registered Successfully!"


# Function to check if the inputted email or password exists.
def authenticate_user(email: str, password: str) -> bool:
        email = email.strip().lower()
        password = password.strip()
        
        logins_df = pd.read_csv(user_path)

        logins_df["email"] = logins_df["email"].astype(str).str.strip().str.lower()
        logins_df["password"] = logins_df["password"].astype(str).str.strip()
        
        # Look for exact match in both email and password columns
        match = logins_df[(logins_df["email"] == email) & (logins_df["password"] == password)]
        
        # Return true if found
        return not match.empty

#Fetch closing price
def get_closing_price(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    closing_prices = stock_data[['Close']]  # Extract only the 'Close' column
    return closing_prices

#Check dates
def is_valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

#Check ticker exists or not
def ticker_exists(ticker): 
    try:
        # Try downloading a small range of data for the ticker
        test_data = yf.Ticker(ticker).history(period="1d")
        return not test_data.empty
    except Exception:
        return False
    
def analyze_closing_price(data):
    if data.empty:
        print("Error: No data available for the selected ticker and dates.")
        return
    
    # Prompt the user to choose an interval
    print("Select an interval for analysis:")
    print("1. Daily (1 day)")
    print("2. Weekly (7 days)")
    print("3. Biweekly (2 weeks)")
    print("4. Monthly (1 month)")
    print("5. Half-yearly (6 months)")
    print("6. Yearly (1 year)")

    interval_choice = int(input("Enter your choice (1-6): "))
    
    # Map interval choices to pandas frequency codes
    interval_map = {
        1: '1D',
        2: '7D',
        3: '14D',
        4: '1M',
        5: '6M',
        6: '1YEAR'
    }

    if interval_choice not in interval_map:
        print("Error: Invalid interval choice. Please choose a valid option.")
        return

    interval = interval_map[interval_choice]

    # Resample data based on the selected interval
    try:
        resampled_data = data['Close'].resample(interval).mean()
        if len(resampled_data) < 2:
            print("Error: Selected date range is too small for the chosen interval.")
            return
    except Exception as e:
        print(f"Error during resampling: {e}")
        return

    # Calculate key metrics
    avg_price = resampled_data.mean()
    highest_price = resampled_data.max()
    lowest_price = resampled_data.min()

    # Convert metrics to scalars
    avg_price = avg_price.item() if hasattr(avg_price, "item") else avg_price
    highest_price = highest_price.item() if hasattr(highest_price, "item") else highest_price
    lowest_price = lowest_price.item() if hasattr(lowest_price, "item") else lowest_price

    # Calculate percentage change
    try:
        first_value = resampled_data.iloc[0].item() if hasattr(resampled_data.iloc[0], "item") else resampled_data.iloc[0]
        last_value = resampled_data.iloc[-1].item() if hasattr(resampled_data.iloc[-1], "item") else resampled_data.iloc[-1]
        percentage_change = ((last_value - first_value) / first_value) * 100
    except Exception as e:
        print(f"Error calculating percentage change: {e}")
        return

    # Display results
    print("\n===== Analysis Results =====")
    print(f"Interval: {interval}")
    print(f"Average Price: {avg_price:.2f}")
    print(f"Percentage Change: {percentage_change:.2f}%")
    print(f"Highest Price: {highest_price:.2f}")
    print(f"Lowest Price: {lowest_price:.2f}")
    print("============================")

    # Return results for saving
    return {
        "average_price": avg_price,
        "percentage_change": percentage_change,
        "highest_price": highest_price,
        "lowest_price": lowest_price,
        "interval":interval
    }

#Save to CSV function
def save_to_csv(data, filename):

    df = pd.DataFrame([data])  # Create a DataFrame from the dictionary
    try:
        # Append data if file exists, otherwise create a new one
        df.to_csv(filename, mode='a', index=False, header=not pd.io.common.file_exists(filename))
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def read_from_csv(filename):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(filename)
        if df.empty:
            print("No saved data found.")
        else:
            os.system('cls')
            print("\n========================= Saved Analysis Data ========================")
            print(df)
            print("========================================================================")
    except FileNotFoundError:
        print("No saved data file found. Please save some data first.")
    except Exception as e:
        print(f"Error reading from CSV: {e}")
