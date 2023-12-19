import csv

# Read data from 'assignment data.csv'
input_file = 'assignment_data.csv'
output_file = 'filtered_properties.csv'

properties = []
with open(input_file, 'r', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        properties.append(row)

# Calculate price per square foot for each property
for prop in properties:
    try:
        price = float(prop.get('price', 0))
        sq_ft = float(prop.get('sq__ft', 1))
        prop['price_per_sqft'] = price / sq_ft if sq_ft != 0 else 0  # Avoid division by zero
    except (ValueError, ZeroDivisionError):
        prop['price_per_sqft'] = 0  # Handling division by zero or invalid values

# Extract price_per_sqft values for properties sold
price_per_sqft_list = [float(prop.get('price_per_sqft', 0)) for prop in properties]

# Calculate average price per square foot
total_price_per_sqft = sum(price_per_sqft_list)
average_price_per_sqft = total_price_per_sqft / len(price_per_sqft_list) if len(price_per_sqft_list) > 0 else 0

# Filter properties sold for less than the average price per square foot
filtered_properties = [prop for prop in properties if float(prop.get('price_per_sqft', 0)) < average_price_per_sqft]

# Write filtered properties to a new CSV file
fieldnames = properties[0].keys() if properties else []
if fieldnames:
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_properties)
    print(f"Filtered properties written to {output_file}")
else:
    print("No properties found.")

