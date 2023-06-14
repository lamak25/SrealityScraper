import psycopg2

# REMINDER OF COMMANDS:

# For compose: https://hub.docker.com/_/postgres
# docker run --name some-postgres -e POSTGRES_PASSWORD=my_super_strong_password -d postgresi
# To get IP of the docker:
# docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_name_or_id>
# To get container name:
# docker ps
# To connect to the DBS:
# psql -h 127.0.0.1 -p 5432 -U postgres
# See all the tables inside:
# \dt
# DROP TABLE <table_name>;
# SELECT * FROM sreality_items;

class DBS_sreality:
    def __init__(self, database_name, username, password, host="localhost", port="5432"):
        self.database_name = database_name
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cursor = None

    def create_open_database(self):
        self.conn = psycopg2.connect(
            dbname=self.database_name,
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.conn.autocommit = True

        # Function to create a PostgreSQL database
        self.cursor = self.conn.cursor()

        # Function to create a table in the database
        if not self.table_exists():
            self.cursor.execute("CREATE TABLE sreality_items (id VARCHAR(11) PRIMARY KEY, offer_url VARCHAR(150), headline VARCHAR(100), img_url VARCHAR(150));")
        self.conn.commit()

    # Check if a table exists
    def table_exists(self):
        self.cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'sreality_items');")
        exists = self.cursor.fetchone()[0]
        return exists

    # Function to insert an item into the table
    def insert_item(self, id, offer_url, headline, img_url):
        self.cursor.execute("INSERT INTO sreality_items (id, offer_url, headline, img_url) \
                            VALUES (%s, %s, %s, %s) \
                            ON CONFLICT (id) DO UPDATE \
                            SET offer_url = EXCLUDED.offer_url, \
                            headline = EXCLUDED.headline, \
                            img_url = EXCLUDED.img_url", (id[:11], offer_url[:150], headline[:100], img_url[:150]))
        self.conn.commit()

    # Function to get all items from the table
    def get_all_items(self):
        self.cursor.execute("SELECT * FROM sreality_items")
        items = self.cursor.fetchall()
        return items

    # Function to get an item from the table based on ID
    def get_item(self, id):
        self.cursor.execute("SELECT * FROM sreality_items WHERE id = %s;", (id,))
        item = self.cursor.fetchone()
        return item

    def __del__(self):
        if self.conn is not None:
            self.conn.close()

# HOW TO USE:
# DB = DBS_sreality("postgres", "postgres", "my_super_strong_password", "172.17.0.2", "5432")
# DB.create_open_database()
#
# # Insert an item
# DB.insert_item("12345678901", "https://www.sreality.cz/detail/prodej/byt/2+kk/usti-nad-labem-severni-terasa-sramkova/2212459596", "Sample headlineee", "https://d18-a.sdn.cz/d_18/c_img_QM_Kb/dAFbUn.jpeg?fl=res,749,562,3|wrm,/watermark/sreality.png,10|shr,,20|jpg,90")
#
# # Get an item by ID
# item = DB.get_item("12345678901")
# print(item)
