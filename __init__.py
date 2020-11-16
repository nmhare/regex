from collections import OrderedDict

from ..en import Provider as AddressProvider


class Provider(AddressProvider):
    city_prefixes = ('North', 'East', 'West', 'South', 'New', 'Lake', 'Port')

    city_suffixes = (
        'ville',
    )

    building_number_formats = ('#####', '####', '###')

    street_suffixes = (
        'Alley',
        'Avenue',
        'Branch',
        'Bridge',
        'Brook',
        'Brooks',
        'Burg',
        'Burgs',
        'Bypass',
        'Camp',
        'Canyon',
        'Cape',
        'Causeway',
        'Center',
        'Centers',
        'Circle',
        'Circles',
        'Cliff',
        'Cliffs',
        'Club',
        'Common',
        'Corner',
        'Corners',
        'Course',
        'Court',
        'Courts',
        'Cove',
        'Coves',
        'Creek',
        'Crescent',
        'Crest',
        'Crossing',
        'Crossroad',
        'Curve',
        'Dale',
        'Dam',
        'Divide',
        'Drive',
        'Drive',
        'Drives',
        'Estate',
        'Estates',
        'Expressway',
        'Extension',
        'Extensions',
        'Fall',
        'Falls',
        'Ferry',
        'Field',
        'Fields',
        'Flat',
        'Flats',
        'Ford',
        'Fords',
        'Forest',
        'Forge',
        'Forges',
        'Fork',
        'Forks',
        'Fort',
        'Freeway',
        'Garden',
        'Gardens',
        'Gateway',
        'Glen',
        'Glens',
        'Green',
        'Greens',
        'Grove',
        'Groves',
        'Harbor',
        'Harbors',
        'Haven',
        'Heights',
        'Highway',
        'Hill',
        'Hills',
        'Hollow',
        'Inlet',
        'Inlet',
        'Island',
        'Island',
        'Islands',
        'Islands',
        'Isle',
        'Isle',
        'Junction',
        'Junctions',
        'Key',
        'Keys',
        'Knoll',
        'Knolls',
        'Lake',
        'Lakes',
        'Land',
        'Landing',
        'Lane',
        'Light',
        'Loaf',
        'Lock',
        'Locks',
        'Locks',
        'Lodge',
        'Lodge',
        'Loop',
        'Mall',
        'Manor',
        'Manors',
        'Meadow',
        'Meadows',
        'Mews',
        'Mill',
        'Mills',
        'Mission',
        'Mission',
        'Motorway',
        'Mount',
        'Mountain',
        'Mountain',
        'Mountains',
        'Mountains',
        'Neck',
        'Orchard',
        'Overpass',
        'Park',
        'Parks',
        'Parkway',
        'Parkways',
        'Pass',
        'Passage',
        'Path',
        'Pike',
        'Pine',
        'Pines',
        'Place',
        'Plain',
        'Plains',
        'Plains',
        'Plaza',
        'Plaza',
        'Point',
        'Points',
        'Port',
        'Port',
        'Ports',
        'Ports',
        'Prairie',
        'Prairie',
        'Radial',
        'Ramp',
        'Ranch',
        'Rapid',
        'Rapids',
        'Rest',
        'Ridge',
        'Ridges',
        'River',
        'Road',
        'Road',
        'Roads',
        'Roads',
        'Route',
        'Row',
        'Rue',
        'Run',
        'Shoal',
        'Shoals',
        'Shore',
        'Shores',
        'Skyway',
        'Spring',
        'Springs',
        'Springs',
        'Spur',
        'Spurs',
        'Square',
        'Square',
        'Squares',
        'Squares',
        'Station',
        'Station',
        'Stravenue',
        'Stravenue',
        'Stream',
        'Stream',
        'Street',
        'Street',
        'Streets',
        'Summit',
        'Summit',
        'Terrace',
        'Throughway',
        'Trace',
        'Track',
        'Trafficway',
        'Trail',
        'Trail',
        'Tunnel',
        'Tunnel',
        'Turnpike',
        'Turnpike',
        'Underpass',
        'Union',
        'Unions',
        'Valley',
        'Valleys',
        'Via',
        'Viaduct',
        'View',
        'Village',
        'Village',
        'Villages',
        'Ville',
        'Vista',
        'Vista',
        'Walk',
        'Walks',
        'Wall',
        'Way',
        'Ways',
        'Well',
        'Wells')

    postcode_formats = ('#####', '#####-####')

    states = (
        'Kentucky'
    )
    states_abbr = (
        'KY',
    )

    states_postcode = {
        'KY': (40003, 42788),
    }

    territories_abbr = (
        'AS', 'FM', 'GU', 'MH', 'MP', 'PW', 'PR', 'VI',
    )

    states_and_territories_abbr = states_abbr + territories_abbr

    military_state_abbr = ('AE', 'AA', 'AP')

    military_ship_prefix = ('USS', 'USNS', 'USNV', 'USCGC')

    military_apo_format = ("PSC ####, Box ####")

    military_dpo_format = ("Unit #### Box ####")

    city_formats = (
        'Louisville',
    )

    street_name_formats = (
        '{{first_name}} {{street_suffix}}',
        '{{last_name}} {{street_suffix}}',
    )

    street_address_formats = (
        '{{building_number}} {{street_name}}',
    )

    address_formats = (
        "{{street_address}}\n{{city}}, {{state_abbr}} {{postcode}}",
    )

    address_formats = OrderedDict((
        ("{{street_address}}\n{{city}}, {{state_abbr}} {{postcode}}", 25),
    ))

    secondary_address_formats = ('Apt. ###', 'Suite ###')

    def city_prefix(self):
        return self.random_element(self.city_prefixes)

    def secondary_address(self):
        return self.numerify(
            self.random_element(
                self.secondary_address_formats))

    def state(self):
        return self.random_element(self.states)

    def state_abbr(self, include_territories=True):
        """
        :returns: A random state or territory abbreviation.

        :param include_territories: If True, territories will be included.
            If False, only states will be returned.
        """
        if include_territories:
            self.random_element(self.states_and_territories_abbr)
        return self.random_element(self.states_abbr)

    def postcode(self):
        return "%05d" % self.generator.random.randint(501, 99950)

    def zipcode_plus4(self):
        return "%s-%04d" % (self.zipcode(),
                            self.generator.random.randint(1, 9999))

    def postcode_in_state(self, state_abbr=None):
        """
        :returns: A random postcode within the provided state abbreviation

        :param state_abbr: A state abbreviation
        """
        if state_abbr is None:
            state_abbr = self.random_element(self.states_abbr)

        if state_abbr in self.states_abbr:
            postcode = "%d" % (self.generator.random.randint(
                            self.states_postcode[state_abbr][0],
                            self.states_postcode[state_abbr][1]))

            if len(postcode) == 4:
                postcode = "0%s" % postcode

            return postcode

        else:
            raise Exception('State Abbreviation not found in list')

    def military_ship(self):
        """
        :example 'USS'
        """
        return self.random_element(self.military_ship_prefix)

    def military_state(self):
        """
        :example 'APO'
        """
        return self.random_element(self.military_state_abbr)

    def military_apo(self):
        """
        :example 'PSC 5394 Box 3492
        """
        return self.numerify(self.military_apo_format)

    def military_dpo(self):
        """
        :example 'Unit 3333 Box 9342'
        """
        return self.numerify(self.military_dpo_format)

    # Aliases
    def zipcode(self):
        return self.postcode()

    def zipcode_in_state(self, state_abbr=None):
        return self.postcode_in_state(state_abbr)

    def postalcode(self):
        return self.postcode()

    def postalcode_in_state(self, state_abbr=None):
        return self.postcode_in_state(state_abbr)

    def postalcode_plus4(self):
        return self.zipcode_plus4()
