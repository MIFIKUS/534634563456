import mysql.connector


HOST = '127.0.0.1'
USERNAME = 'root'
PASSWORD = 'root'


class AddInfo:
    def __init__(self):
        self._connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
        self._connection.autocommit = True
        self.cursor = self._connection.cursor()

    def add_info(self, data: dict):
        tournament_id = data['tournament_id']
        name = data['name']
        gtd = data['gtd']
        buy_in = data['buy_in']
        total_buy_in = data['total_buy_in']
        table_size = data['table_size']
        speed = data['speed']
        tournament_type = data['type']
        archive_name = data['tournament_id']
        files_in_archive = data['files_in_archive']
        hands = data['hands']
        create_data = data['create_date']
        modify_date = data['modify_date']

        query = "INSERT INTO tournaments (tournament_id, name, gtd, buy_in, total_buy_in, table_size, speed, "\
                "tournament_type, archive_name, files_in_archive, hands, create_date, modify_date)"\
                f"(VALUES ({tournament_id}, {name}, {gtd}, {buy_in}, {total_buy_in}, {table_size}, {speed}, {tournament_type},"\
                f"{archive_name}, {files_in_archive}, {hands}, {create_data}, {modify_date});"

        self.cursor.execute(query)
    