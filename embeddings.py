import sqlite3
import numpy as np


class EmbeddingDatabase:

    def __init__(self, db_dir):
        self.connection = sqlite3.connect(db_dir, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def save_embeddings_to_database(self, raw_embeddings_dir):
        id_embedding = 0

        self.cursor.execute('drop table if exists embeddings')
        self.cursor.execute('create table embeddings (palabra text, embedding_vector blob)')

        with open(raw_embeddings_dir, mode='r', encoding='utf8', errors='ignore') as file:
            file.readline()  # Para remover el encabezado
            for line in file:
                separator = line.index(' ')
                key = line[0:separator]
                values = np.fromstring(line[separator + 1:], dtype=float, sep=' ')

                params = (key, values)

                self.cursor.execute('insert into embeddings values (?, ?)', params)

                id_embedding += 1
                if id_embedding % 50000 == 0:
                    print('Van {0} embeddings'.format(id_embedding))

        self.cursor.execute('create index idx_palabra on embeddings(palabra)')

        self.connection.commit()

    def get(self, word):
        params = (word, )
        self.cursor.execute('select * from embeddings where palabra = ?', params)

        result = self.cursor.fetchone()[1]

        return np.frombuffer(result, dtype=np.float)

    def close_connection(self):
        self.connection.close()
