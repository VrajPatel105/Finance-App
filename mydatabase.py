import json

class Database:
    

    def add_data(self, name, password, confirmpassword,rhs_value):
        try:
            # Read the existing database
            with open('database.json', 'r') as rf:
                try:
                    database = json.load(rf)
                except json.JSONDecodeError:
                    database = {}

            # Validation checks
            if int(rhs_value) in database:
                return 0
            elif password != confirmpassword:
                return 0
            else:
                # Add new data and save it
                database[int(rhs_value)] = [name, password]
                with open('database.json', 'w') as wf:
                    json.dump(database, wf, indent=4)  # Indent for readability
                return 1
        except Exception as e:
            print(f"Error in add_data: {e}")
            return 0

        

    def search(self, rhsvalue, password):
        with open('database.json', 'r') as rf:
            database = json.load(rf)
            # Convert all keys to integers
            database = {int(k): v for k, v in database.items()}
            # Now search with integer
            if int(rhsvalue) in database:
                if database[int(rhsvalue)][1] == password:
                    return 1
        return 0
            

    def add_rhs_val(self,email,rhs_value):
        try:
            # Read the existing database
            with open('rhs_database.json', 'r') as rf:
                try:
                    database = json.load(rf)
                except json.JSONDecodeError:
                    database = {}

            # Validation checks
            database[email] = [rhs_value]
            with open('rhs_database.json', 'w') as wf:
                json.dump(database, wf, indent=4)
            return rhs_value
                
        except Exception as e:
            print(f"Error in add_data: {e}")
            return 0
        


    def search_rhs_value(self,email):
        with open('rhs_database.json', 'r') as rf:
            database = json.load(rf)
            if email in database:
                return database[email][0]