import sqlite3

conn = sqlite3.connect('verbs.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users ( 
                [user_id] INTEGER PRIMARY KEY, 
                [username] TEXT NOT NULL, 
                [hash] TEXT NOT NULL)
            ''')

c.execute('''CREATE TABLE IF NOT EXISTS vocabulary (
                [verb_id] TEX NOT NULL,
                [user_id] TEXT NOT NULL,
                FOREIGN KEY([verb_id]) REFERENCES base([generated_id]),
                FOREIGN KEY([user_id]) REFERENCES users([user_id]))
            ''')

c.execute('''CREATE TABLE IF NOT EXISTS base (
                [generated_id] INTEGER PRIMARY KEY, 
                [verb] TEXT)
            ''')
            

# Tables for storing past tense verb forms in the first person.
c.execute('''CREATE TABLE IF NOT EXISTS past_1st_singular_neutral (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')
            
c.execute('''CREATE TABLE IF NOT EXISTS past_1st_plural_neutral (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')


# Tables for verb forms in the second person.
c.execute('''CREATE TABLE IF NOT EXISTS past_2nd_singular_masculine (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')
            
c.execute('''CREATE TABLE IF NOT EXISTS past_2nd_singular_feminine (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')
            
c.execute('''CREATE TABLE IF NOT EXISTS past_2nd_dual_neutral (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')
            
c.execute('''CREATE TABLE IF NOT EXISTS past_2nd_plural_masculine (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')
            
c.execute('''CREATE TABLE IF NOT EXISTS past_2nd_plural_feminine (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')

# Tables for verb forms in the third person.
c.execute('''CREATE TABLE IF NOT EXISTS past_3rd_singular_masculine (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')
            
c.execute('''CREATE TABLE IF NOT EXISTS past_3rd_singular_feminine (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')
            
c.execute('''CREATE TABLE IF NOT EXISTS past_3rd_dual_masculine (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')
            
c.execute('''CREATE TABLE IF NOT EXISTS past_3rd_dual_feminine (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')
            
c.execute('''CREATE TABLE IF NOT EXISTS past_3rd_plural_masculine (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')
            
c.execute('''CREATE TABLE IF NOT EXISTS past_3rd_plural_feminine (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')
            
# Tables for storing present tense verb forms in the first person.
c.execute('''CREATE TABLE IF NOT EXISTS present_1st_singular_neutral (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')
            
c.execute('''CREATE TABLE IF NOT EXISTS present_1st_plural_neutral (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')

# Tables for verb forms in the second person.            
c.execute('''CREATE TABLE IF NOT EXISTS present_2nd_singular_masculine (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')
            
c.execute('''CREATE TABLE IF NOT EXISTS present_2nd_singular_feminine (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')
            
c.execute('''CREATE TABLE IF NOT EXISTS present_2nd_dual_neutral (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')
            
c.execute('''CREATE TABLE IF NOT EXISTS present_2nd_plural_masculine (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')
            
c.execute('''CREATE TABLE IF NOT EXISTS present_2nd_plural_feminine (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')


# Tables for verb forms in the third person.
c.execute('''CREATE TABLE IF NOT EXISTS present_3rd_singular_masculine (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')
            
c.execute('''CREATE TABLE IF NOT EXISTS present_3rd_singular_feminine (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')
            
c.execute('''CREATE TABLE IF NOT EXISTS present_3rd_dual_masculine (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')
            
c.execute('''CREATE TABLE IF NOT EXISTS present_3rd_dual_feminine (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')
            
c.execute('''CREATE TABLE IF NOT EXISTS present_3rd_plural_masculine (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')
            
c.execute('''CREATE TABLE IF NOT EXISTS present_3rd_plural_feminine (
                [pronoun] TEXT,
                [verb] TEXT,
                [id] INTEGER NOT NULL,
                FOREIGN KEY([id]) REFERENCES base([generated_id]) ON DELETE CASCADE)
            ''')

conn.commit()
conn.close()
