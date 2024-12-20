import json

class Database:
    

    def add_data(self, name, email, password, confirmpassword):
        try:
            # Read the existing database
            with open('database.json', 'r') as rf:
                try:
                    database = json.load(rf)
                except json.JSONDecodeError:
                    database = {}

            # Validation checks
            if email in database:
                return 0
            elif password != confirmpassword:
                return 0
            else:
                # Add new data and save it
                database[email] = [name, password]
                with open('database.json', 'w') as wf:
                    json.dump(database, wf, indent=4)  # Indent for readability
                return 1
        except Exception as e:
            print(f"Error in add_data: {e}")
            return 0

        

    def search(self,email,password):

        with open('database.json', 'r') as rf:
            database = json.load(rf)
            if email in database:
                if database[email][1] == password:
                    return 1
                else:
                    return 0
            else:
                return 0