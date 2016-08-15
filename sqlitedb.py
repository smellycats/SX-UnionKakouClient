import sqlite3


class KakouDB(object):
    def __init__(self):
        self.conn = sqlite3.connect('/home/kakou.db')
        print "Opened database successfully";

    def __del__(self):
        self.conn.close()

    def add_idflag(self, start_id, end_id):
        self.conn.execute("INSERT INTO IDFLAG (START_ID,END_ID) \
              VALUES ({0}, {1})".format(start_id, end_id));
        r = self.conn.execute("SELECT last_insert_rowid()")
        self.conn.commit()
        return r.fetchone()[0]

    def set_idflag(self, _id, start_id):
        sql = "UPDATE IDFLAG SET start_id={0} WHERE id={1}".format(
            start_id, _id)
        self.conn.execute(sql)
        self.conn.commit()

    def get_idflag_by_id(self, _id):
        sql = "SELECT * FROM IDFLAG WHERE id={0}".format(_id)
        r = self.conn.execute(sql)
        return r.fetchone()

    def get_idflag(self, banned=0):
        sql = "SELECT * FROM IDFLAG WHERE banned={0}".format(banned)
        r = self.conn.execute(sql)
        return r.fetchone()

    def del_idflag(self, _id):
        sql = "UPDATE IDFLAG SET banned=1 WHERE id={0}".format(_id)
        self.conn.execute(sql)
        self.conn.commit()

if __name__ == "__main__":
    s = KakouDB()
    print s.add_idflag(2, 4)
    #s.set_idflag(1, 5)
    print s.get_idflag(0)
    #s.del_idflag(1)
