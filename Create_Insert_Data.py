import logging
import pandas
import sqlalchemy
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler('python.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

with open("config.json", 'r') as json_file:
  config = json.load(json_file)

def create_engine(dialect, username, password, server, port, database):
    connection = '%s://%s:%s@%s:%d/%s' % (dialect, username, password, server, port, database)
    logger.info(connection)
    engine = sqlalchemy.create_engine(connection)
    return engine

def main():
    try:
        object=config['tablelist'] 
        dialect = config['dialect']
        username = config['sql_username']
        password = config['sql_password']
        server = config['server']
        port = config['port']
        database = config['database']
        file_path = config['filepath']
        y=0
        
        while(len(object) > y):
            target_table = object[y]['Name']
            engine = create_engine(dialect, username, password, server, port, database)
            df = pandas.read_csv(file_path + target_table + ".csv")
            df.to_sql(target_table, engine, if_exists='replace', index=False)
            y=y+1
        
    except Exception as e:
        logger.error(e, exc_info=True)
        print(e)

if __name__ == '__main__':
    main()