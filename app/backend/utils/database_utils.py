import psycopg2

from constants import (
    CREATE_STATIONS, 
    INSERT_DATA, 
    COL_TYPES, 
    GET_DATA, 
    GET_STATIONS_IDS, 
    GET_VARIABLES
)


class DatabaseUtils():

    def __init__(self):
        try:
            print('Connecting to Postgresql')
            self.conn = psycopg2.connect(host="localhost", database="weather_data")
            self.create_table()
            print('Connected!')
        except Exception as e:
            print('Error while trying to connect to Postgresql')
            raise e
        
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute(CREATE_STATIONS)
        cursor.close()
        self.conn.commit()

    def insert_data(self, data):
        insert_query = self.format_insert_query(data)
        cursor = self.conn.cursor()
        try:
            cursor.execute(insert_query)
        except psycopg2.IntegrityError:
            print('Error record already exists, discarding it')
        except (psycopg2.DataError, psycopg2.ProgrammingError):
            print('Error while inserting record, discarding it')
        
        cursor.close()
        self.conn.commit()

    def get_data(self, station_id, variable_name):
        return self.execute_get_query(GET_DATA.format(station_id, variable_name))

    def get_stations_ids(self):
        return self.execute_get_query(GET_STATIONS_IDS)
    
    def get_variables_names(self):
        return self.execute_get_query(GET_VARIABLES)

    def execute_get_query(self, query):
        cursor = self.conn.cursor()
        try:
            cursor.execute(query)
            values = cursor.fetchall()
        except Exception as e:
            print(e) 
            return None
        
        cursor.close()
        self.conn.commit()

        return values    

    @staticmethod
    def format_insert_query(data):
        insert_query = INSERT_DATA + '('
        for i in range(len(data)-1):
            try:
                if COL_TYPES[i] == 'INT':
                    insert_query += "%d, " % int(data[i])
                elif COL_TYPES[i] == 'STR':
                    insert_query += "'%s', " % data[i]
                else:
                    insert_query += "%f, " % float(data[i])
            except ValueError:
                return None
        
        insert_query += "'%s');" % data[-1]

        return insert_query