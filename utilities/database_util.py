import json

# Load the JSON data from a file
with open('Dataset/database.json', 'r') as file:
    data = json.load(file)

# Function to search for an item and check its availability
def check_availability(item_name):
    for item in data:
        if item["item"].lower() == item_name.lower():
            if item["available"]:
                return f"aisle no: {item}"
            else:
                return f"{item['item']} is currently unavailable."
    return f"{item_name} not found in the list."

# Example usage
item_name = input("Enter the item you want to search for: ")
print(check_availability(item_name))

