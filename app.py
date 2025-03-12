import sys
import mysql.connector
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QLabel, QTableWidget, QTableWidgetItem



class TeamSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Set up window
        self.setWindowTitle('Team Selector')
        self.setGeometry(100, 100, 600, 400)

        # Create a QVBoxLayout to hold the widgets
        layout = QVBoxLayout()

        # Create a label to display the selected team
        self.label = QLabel("Select a Team", self)
        layout.addWidget(self.label)

        # Create a ComboBox for the dropdown list
        self.combo_box = QComboBox(self)

        # Get the list of teams from the database and populate the ComboBox
        self.load_teams_from_database()

        # Connect the dropdown change event to a function
        self.combo_box.currentTextChanged.connect(self.on_combobox_changed)

        # Add the ComboBox to the layout
        layout.addWidget(self.combo_box)

        # Create a table to display the players
        self.table_widget = QTableWidget(self)
        layout.addWidget(self.table_widget)

        # Set the layout for the window
        self.setLayout(layout)

    def load_teams_from_database(self):
        try:
            conn = connect_to_mysql()
            cursor = conn.cursor()

            # Execute the query to get team names and team abbreviations
            cursor.execute("SELECT team_name, team_abbrev FROM teams")
            teams = cursor.fetchall()

            # Add team names to the combo box
            for team in teams:
                self.combo_box.addItem(team[0], team[1])  # team[0] is name, team[1] is abbreviation

            # Close the database connection
            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def on_combobox_changed(self, text):
        # Get the selected team abbreviation
        team_abr = self.combo_box.currentData()
        
        # Load players for the selected team
        self.load_players_for_team(team_abr)

    def load_players_for_team(self, team_abr):
        try:
            conn = connect_to_mysql()
            cursor = conn.cursor()

            # Execute the query to get players for the selected team
            cursor.execute("""
                SELECT first_name, last_name, sweater_number, position_code, shoots_catches
                FROM players
                WHERE team_abr = %s
            """, (team_abr,))

            players = cursor.fetchall()

            # Update the table with player data
            self.table_widget.setRowCount(len(players))
            self.table_widget.setColumnCount(5)
            self.table_widget.setHorizontalHeaderLabels(["First Name", "Last Name", "Number", "Position", "Shoots/Catches"])

            # Populate the table with player data
            for row, player in enumerate(players):
                for col, value in enumerate(player):
                    self.table_widget.setItem(row, col, QTableWidgetItem(str(value)))

            # Close the database connection
            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

def connect_to_mysql():
    conn = mysql.connector.connect(
        host="localhost",      # e.g., "localhost"
        user="root",  # e.g., "root"
        password="GoBolts#12358",
        database="nhl_data" # Change to your actual database name
    )
    return conn
# Set up the application
app = QApplication(sys.argv)

# Create the window
window = TeamSelector()
window.show()

# Run the application
sys.exit(app.exec())
