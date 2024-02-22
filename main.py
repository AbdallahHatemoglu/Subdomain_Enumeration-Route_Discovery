import requests


# Function to generate subdomains by combining words from the wordlist with the target domain
def generate_subdomains(target_domain, wordlist):
    subdomains = [f"{word}.{target_domain}" for word in wordlist]
    subdomains.append(target_domain)  # Add the base domain as well
    return subdomains


# Function to perform route discovery and return the HTTP status code
def discover_route(route):
    try:
        response = requests.get(route)
        return response.status_code
    except requests.exceptions.RequestException:
        return None  # Request failed


# Function to discover routes for a list of routes and return a report
def discover_routes_and_report(target_domain, routes):
    route_report = []

    for route in routes:
        status_code = discover_route(route)

        # Check if the request was successful (status code not None)
        if status_code is not None:
            route_report.append(f"Route: {route} - Status Code: {status_code}")

    # Save the route report to a file
    route_report_file = "route_report.txt"
    with open(route_report_file, 'w') as file:
        file.write('\n'.join(route_report))

    print(f"Route discovery completed. Route report saved to {route_report_file}")


# Input: Target Domain and Wordlist File
target_domain = input("Enter the target domain (e.g., example.com): ")
wordlist_file = input("Enter the path to the wordlist file: ")

# Load wordlist from the file
with open(wordlist_file, 'r') as file:
    wordlist = [line.strip() for line in file]

# Define common route patterns (you can extend this list)
route_patterns = ["/login", "/admin", "/dashboard", "/api", "/contact"]

# Generate subdomains
subdomains = generate_subdomains(target_domain, wordlist)

routes = [f"http://{subdomain}{pattern}" for subdomain in subdomains for pattern in route_patterns]

# Perform route discovery for subdomains and create a subdomain report
subdomain_report = []

for subdomain in subdomains:
    route = f"http://{subdomain}"
    status_code = discover_route(route)
    if status_code is not None:
        subdomain_report.append(f"Subdomain: {subdomain} - Status Code: {status_code}")

# Save the subdomain report to a file
subdomain_report_file = "subdomain_report.txt"

with open(subdomain_report_file, 'w') as file:
    file.write('\n'.join(subdomain_report))
# Call the function to discover routes and create a report
discover_routes_and_report(target_domain, routes)