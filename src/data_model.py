class DataModel():
    def __init__(self, api_data):
        bases = api_data.bases
        # last data about bases different in values
        self.different_bases = bases
        # value from different loop
        self.previous_bases = bases

        self.previous_forum_records = {}

        for record in api_data.new_forum_records:
            self.previous_forum_records[record.title] = record

    def update(self, api_data):

        # calculating previous health about bases
        if self.previous_bases != api_data.bases:
            self.different_bases = self.previous_bases
        self.previous_bases = api_data.bases
        api_data.different_bases = self.different_bases

        def health_diff(a, b):
            if a < b:
                return 'Repairing'
            elif a > b:
                return 'Degrading'
            return 'Static'

        api_data.bases = {
            key: dict(
                value, **{
                    "diff":
                    health_diff(api_data.different_bases[key]['health'],
                                value['health'])
                })
            for key, value in api_data.bases.items()
        }

        self.api_data = api_data