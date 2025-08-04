import tkinter as tk
from tkinter import ttk, messagebox

class CurrencyConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("Currency Converter")
        master.geometry("400x300") # Set a fixed window size
        master.resizable(False, False) # Make the window non-resizable

        # Define some colors for better aesthetics
        self.bg_color = "#16701B"
        self.button_color = "#4B4722" # Green
        self.button_text_color = "white"
        self.label_color = "#333333"

        master.configure(bg=self.bg_color)

        # --- Exchange Rates (Hardcoded for demonstration) ---
        # In a real application, you would fetch these from a reliable API.
        # Rates are relative to 1 GHS (Ghana Cedi).
        # Example: 1 USD = 10.5 GHS, so 1 GHS = 1/10.5 USD
        self.exchange_rates = {
            "GHS": 1.0,  # Ghana Cedi
            "USD": 10.5, # US Dollar (1 USD = 10.5 GHS) - Bank of Ghana mid-rate
            "EUR": 12.1166, # Euro (1 EUR = 12.1166 GHS) - Bank of Ghana mid-rate
            "GBP": 13.9062, # British Pound (1 GBP = 13.9062 GHS) - Bank of Ghana mid-rate
            # Add more currencies as needed
        }
        self.currencies = sorted(list(self.exchange_rates.keys()))

        # --- GUI Elements ---

        # Amount Label and Entry
        self.amount_label = tk.Label(master, text="Amount:", bg=self.bg_color, fg=self.label_color, font=('Arial', 10, 'bold'))
        self.amount_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.amount_entry = tk.Entry(master, width=20, font=('Arial', 10))
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # From Currency Dropdown
        self.from_currency_label = tk.Label(master, text="From:", bg=self.bg_color, fg=self.label_color, font=('Arial', 10, 'bold'))
        self.from_currency_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.from_currency_var = tk.StringVar(master)
        self.from_currency_var.set("USD") # Default value
        self.from_currency_menu = ttk.Combobox(master, textvariable=self.from_currency_var, values=self.currencies, state="readonly", width=17)
        self.from_currency_menu.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # To Currency Dropdown
        self.to_currency_label = tk.Label(master, text="To:", bg=self.bg_color, fg=self.label_color, font=('Arial', 10, 'bold'))
        self.to_currency_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.to_currency_var = tk.StringVar(master)
        self.to_currency_var.set("GHS") # Default value
        self.to_currency_menu = ttk.Combobox(master, textvariable=self.to_currency_var, values=self.currencies, state="readonly", width=17)
        self.to_currency_menu.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Convert Button
        self.convert_button = tk.Button(master, text="Convert", command=self.convert_currency,
                                        bg=self.button_color, fg=self.button_text_color,
                                        font=('Arial', 12, 'bold'), relief=tk.RAISED, bd=3)
        self.convert_button.grid(row=3, column=0, columnspan=2, pady=20)

        # Result Label
        self.result_label = tk.Label(master, text="Converted Amount: ", bg=self.bg_color, fg=self.label_color, font=('Arial', 12, 'bold'))
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)

        # Configure grid columns to expand
        master.grid_columnconfigure(1, weight=1)

    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            from_currency = self.from_currency_var.get()
            to_currency = self.to_currency_var.get()

            if from_currency not in self.exchange_rates or to_currency not in self.exchange_rates:
                messagebox.showerror("Error", "Selected currencies are not supported.")
                return

            # Step 1: Convert the amount from the source currency to a common base (GHS in this case)
            # If the source currency is GHS, amount_in_ghs is just the amount.
            # Otherwise, amount_in_ghs = amount * rate_of_source_currency_to_GHS
            amount_in_ghs = amount * self.exchange_rates[from_currency]

            # Step 2: Convert from the common base (GHS) to the target currency
            # If the target currency is GHS, converted_amount is amount_in_ghs.
            # Otherwise, converted_amount = amount_in_ghs / rate_of_target_currency_to_GHS
            converted_amount = amount_in_ghs / self.exchange_rates[to_currency]

            self.result_label.config(text=f"Converted Amount: {converted_amount:.2f} {to_currency}")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numeric amount.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def fetch_realtime_rates(self):
        """
        Placeholder function to demonstrate where you would fetch real-time rates.
        You would typically use a library like 'requests' to call a currency exchange API.
        Examples of APIs: Open Exchange Rates, Fixer.io, ExchangeRate-API, etc.

        Example using 'requests':"""
        import requests
        API_KEY = "YOUR_API_KEY"
        BASE_URL = "https://api.exchangerate-api.com/v4/latest/USD" # Or your chosen base currency

        try:
            response = requests.get(BASE_URL)
            response.raise_for_status() # Raise an exception for HTTP errors
            data = response.json()
            # Assuming data['rates'] contains currency codes mapped to their rates relative to BASE_URL
            # You would then process this data to update self.exchange_rates
            # For this app, you'd likely want rates relative to GHS.
            # If API provides rates relative to USD, then GHS_rate_vs_USD = data['rates']['GHS']
            # And then update self.exchange_rates accordingly:
            # self.exchange_rates = {currency: 1 / data['rates'][currency] * GHS_rate_vs_USD for currency in data['rates']}
            # Or fetch rates directly relative to GHS if the API supports it.

            messagebox.showinfo("Rates Updated", "Exchange rates have been updated successfully!")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Network Error", f"Could not fetch real-time rates: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while parsing rates: {e}")
        
        messagebox.showinfo("Real-time Rates", "This function would fetch real-time rates from an API. For this demo, rates are static.")


# --- Main execution block ---
if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    # You could add a button to trigger fetch_realtime_rates or call it on app start
    app.fetch_realtime_rates() # Uncomment to see the info message on startup
    root.mainloop()