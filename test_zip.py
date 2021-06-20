import pgeocode

nomi = pgeocode.Nominatim('US')

zipcode = nomi.query_postal_code('44095')

print(zipcode)
