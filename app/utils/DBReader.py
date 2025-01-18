import psycopg2


class DBReader:
    def lifeCheck(self):
        try:
            self.cursor.execute("Select 1;")
            return [True,"dbreader"]
        except(Exception) as e:
            return [e,"dbreader"]


    def __init__(self, userMS, hostDB, portDB, passwdDB, databDB):
        self.host = hostDB
        self.port = portDB
        self.database = databDB
        self.user = userMS
        self.password = passwdDB

        # Establish the database connection
        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )
        self.cursor = self.conn.cursor()

    def read_data(self, query, params=None):
        """
        Executes the given SQL query and returns the result.

        :param query: The SQL query to execute.
        :param params: Optional query parameters.
        :return: List of tuples containing the query result.
        """
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        """Closes the cursor and the connection."""
        self.cursor.close()
        self.conn.close()
