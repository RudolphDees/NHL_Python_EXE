import mysql.connector

# Connect to the database
conn = mysql.connector.connect(
    host="localhost",      # e.g., "localhost"
    user="root",  # e.g., "root"
    password="GoBolts#12358",
    database="test_databse" # Change to your actual database name
)

cursor = conn.cursor()

# Insert data
sql = "INSERT INTO test_table (test) VALUES (%s)"
values = ("Hello, MySQL!",)

cursor.execute(sql, values)
conn.commit()  # Save changes

print("Data inserted successfully!")

# Close connection
cursor.close()
conn.close()
