#!/usr/bin/env python3

from db_table import db_table
import pandas as pd
import sys
import sqlite3

def import_agenda(file_path):
    # Define the schema for the agenda table
    agenda_schema = {
        'Date': "text",
        'Time_Start': "text",
        'Time_End': "text",
        'Session_Subsession': "text",
        'Session_Title': "text",
        'Speakers': "text",
        # Add other columns as needed
    }

    # Create the agenda table
    agenda_table = db_table("agenda", agenda_schema)

    # Manually construct the SQL statement for creating the "agenda" table
    create_table_sql = "CREATE TABLE IF NOT EXISTS agenda ({})".format(
        ', '.join(['"{}" {}'.format(col, data_type) for col, data_type in agenda_schema.items()])
    )

    # Connect to the SQLite database
    conn = sqlite3.connect('interview_test.db')  # Updated to 'interview_test.db'
    cursor = conn.cursor()

    # Execute the SQL statement to create the "agenda" table
    cursor.execute(create_table_sql)

    # Convert DataFrame to a list of dictionaries
    df = pd.read_excel(file_path, skiprows=14)
    print("Column names in DataFrame:", df.columns)

    agenda_data = df.where(pd.notna(df), '').to_dict(orient='records')
    # Remove extra double quotes around keys
    agenda_data = [{k.replace('""', ''): v for k, v in record.items()} for record in agenda_data]

    # for record in agenda_data:
    #     if isinstance(record, dict):
    #         print("Raw value for 'Session_Subsession':", record.get('*Session or Sub-session(Sub)', ''))
    #         Rest of your code
    for record in agenda_data:
        try:
            if isinstance(record, dict):  # Check if the record is a dictionary
                # Split speakers using semicolon and store in a list
                speakers = str(record.get('Speakers', '')).split(";") if 'Speakers' in record else []

                # Create a new dictionary to hold the modified record
                modified_record = {
                    'Date': record.get('*Date'),
                    'Time_Start': record.get('*Time Start'),  # Update to 'Time Start'
                    'Time_End': record.get('*Time End'),  # Update to 'Time End'
                    'Session_Subsession': record.get('*Session or \nSub-session(Sub)', ''),
                    'Session_Title': record.get('*Session Title'),
                    'Speakers': ';'.join(speakers),
                }
                # # Ensure the keys in the record match the correct column names
                # # Rename keys to match the column names in your SQLite schema
             
                
                # Prepare a list of columns for the SQL query
                columns_query = ', '.join(['"{}"'.format(column) for column in modified_record.keys()])

                # Use parameterized queries for values
                values_query = ', '.join(['?' for _ in modified_record.values()])

                # Construct the SQL insert query with parameterized values
                insert_query = 'INSERT INTO "{}" ({}) VALUES ({})'.format(agenda_table.name, columns_query, values_query)

                # Execute the SQL insert query with parameterized values
                cursor.execute(insert_query, tuple(modified_record.values()))

        except Exception as e:
            print("Error inserting record:", record)
            print("Error details:", e)

    # Commit changes to the database
    conn.commit()

    # Close the SQLite database connection
    conn.close()

    # Close the database connection
    agenda_table.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./import_agenda.py agenda.xls")
        sys.exit(1)

    file_path = sys.argv[1]
    import_agenda(file_path)
