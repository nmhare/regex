import pyap
test_address = """
1829 n mozart st  Louisville KY
    """
addresses = pyap.parse(test_address, country='US')
for address in addresses:
# shows found address
    print(address)
    # shows address parts
    print(address.as_dict())

