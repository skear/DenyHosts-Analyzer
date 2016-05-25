import geoip2.database

# Path to hosts.deny file
inputfile = "/etc/hosts.deny"

# Path to GeoLite2 mmdb file
geoip_inputfile = "GeoLite2-Country.mmdb"

# Create the file handlers
file = open(inputfile, 'r')
reader = geoip2.database.Reader(geoip_inputfile)

# Declarations
count = 1
ip_not_found = 0
ip_seen = 0
country_count = dict()

# Main loop to process the file
for line in file:

    # Remove carriage returns
    line = line.rstrip()

    # Ignore comments in the file
    if not line.startswith("#"):

        # Ignore any blank lines
        if not line.strip():
            continue
        else:
            # Grab just the IP address
            line = line.split(" ")

            # If there is not a period then it must not be an IP address
            if not "." in line[1]:
                break
            ip = line[1]

            try:
                response = reader.country(ip)
            except:
                ip_not_found = ip_not_found + 1

            ip_seen += 1
            country_iso = response.country.iso_code
            country_name = response.country.name
            country_count[country_name] = country_count.get(country_name, 0)+1

    count += 1

# Sort the dictionary by most IP addresses
country_count_sorted = sorted(country_count.items(), key=lambda i: i[1], reverse=True)

for country, value in country_count_sorted:
    print country, value

# Send the output to the terminal
print
print "Processed", ip_seen, "IP addresses."
print "There were", ip_not_found, "IP addresses that were not found in the database."
print
