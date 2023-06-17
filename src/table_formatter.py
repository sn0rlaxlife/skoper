from tabulate import tabulate

def format_table(data):
    """
    Formats the provided data into a rich table using the tabulate library.

    Args:
        data (list): A list of lists representing the tabular data.

    Returns:
        str: The formatted table as a string.
    """
    headers = data[0]  # Extract the headers from the first row
    rows = data[1:]  # Extract the data rows

    table = tabulate(rows, headers, tablefmt="fancy_grid")  # Generate the table using tabulate

    return table

# Example usage
data = [
    ["Name", "Age", "Country"],
    ["John Doe", 30, "USA"],
    ["Jane Smith", 28, "Canada"],
    ["Adam Johnson", 35, "Australia"]
]

formatted_table = format_table(data)
print(formatted_table)
