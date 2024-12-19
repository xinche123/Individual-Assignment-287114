from functions import *
import os

endChoice = 0
#Login Menu
while endChoice != 1:
    try:
        print("===== Stock Selection and Analyze Tool =====")
        print("What would you like to do?")
        print("1. Login\n"
              "2. Register\n"
              "3. Exit")
        menuChoice =int(input("Please select : "))
        if menuChoice == 1: # Login Choice
            while True:
                email = str(input("Please Enter Your Email: "))
                password = str(input("Please Enter Your Password: ")) 
                if "@" in email:
                    if authenticate_user(email,password):
                        os.system('cls')
                        print("==== Login Successful! ====")
                        endChoice = 1
                        break
                    else:
                        print("Invalid Email or Password, returning to Main Menu")
                        break
                else:
                    print("Please enter a valid email")
                    continue
        elif menuChoice == 2: # Register Choice
            while True:
                print("Please type 'exit' in email or password to return to main menu")
                email = str(input("Please enter an email to register: "))
                password = str(input("Please enter an password to register: "))
                if "@" in email:
                    os.system('cls')
                    register_result = register_user(email,password)
                    print(register_result)
                    break
                elif email.lower() or password.lower() == "exit":
                    break
                else:
                    print("Please enter a valid email")
                    continue
        elif menuChoice == 3: # Exit Choice
            print("Exiting......")
            quit()
        else:
            print("Please enter 1 to 3 only")
            continue

    except ValueError: # Check Valid Values or Not
        print("Please enter valid values only, Restarting...")
        continue

#Stock Menu, Activated when Login Successful
while True:
    analysisFile = "stock_analysis.csv"
    print("===== Stock Selection and Analyze Tool =====")
    print("What would you like to do?")
    print("1. Analyze\n"
          "2. Display Saved Data\n"
          "3. Exit")
    stockMenuChoice = int(input("Please select: "))
    os.system('cls')
    if stockMenuChoice == 1: # Analyze Choice
        while True:
            while True:
                ticker = input("Enter stock ticker (e.g., 1023.KL for CIMB, 1155.KL for Maybank): ").upper()
                if ".KL" not in ticker:
                    print("Invalid ticker! Please make sure the ticker contains '.KL'.")
                    continue

                if not ticker_exists(ticker):  # Verify if the ticker exists
                    print("Ticker does not exist or is invalid. Please try again.")
                    continue
                break

            while True:
                start_date = input("Enter start date (YYYY-MM-DD): ")
                if is_valid_date(start_date):
                    break
                print("Invalid date format! Please enter the date in 'YYYY-MM-DD' format.")

            while True:
                end_date = input("Enter end date (YYYY-MM-DD): ")
                if is_valid_date(end_date):
                    if start_date <= end_date:  # Ensure start_date is before or same as end_date
                        break
                    print("End date must be after or equal to the start date!")
                else:
                    print("Invalid date format! Please enter the date in 'YYYY-MM-DD' format.")

            data = get_closing_price(ticker, start_date, end_date)

            if not data.empty:
                print(data)  # Display the fetched data
                analysis_results = analyze_closing_price(data)  # Perform analysis

                # Prepare data to save
                saved_data = {
                    "Email": email,
                    "Ticker": ticker,
                    "Start Date": start_date,
                    "End Date": end_date,
                    "Interval": analysis_results['interval'],
                    "Average Price": round(analysis_results['average_price'], 2),
                    "Percentage Change": round(analysis_results['percentage_change'], 2),
                    "Highest Price": round(analysis_results['highest_price'], 2),
                    "Lowest Price": round(analysis_results['lowest_price'], 2),
                }

                # Save the data
                save_to_csv(saved_data, analysisFile)
                print("\nAnalysis results saved successfully!\n")

            else:
                print("No data to analyze.")

            exitChoice = input("Do you want to:\n1. Exit\n2. Go back to the main menu\n3. Analyze another stock\nEnter your choice (1-3): ")
            if exitChoice == "1":
                os.system('cls')
                print("Exiting...")
                quit()
            elif exitChoice == "2":
                os.system('cls')
                break
            elif exitChoice == "3":
                os.system('cls')
                continue
            else:
                print("Please enter 1, 2, or 3 only.")

    elif stockMenuChoice == 2:
        # Display saved data
        read_from_csv(analysisFile)

    elif stockMenuChoice == 3:
        os.system('cls')
        print("Exiting...")
        quit()

    else:
        print("Invalid choice! Please select 1, 2, or 3.")
    