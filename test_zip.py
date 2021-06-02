import pgeocode

nomi = pgeocode.Nominatim('GB')

zipcode = nomi.query_postal_code('E1 7AX')

print(zipcode)
