import pymysql


class DataBase:
    def __init__(self, host, user, password, db):
        self.con = pymysql.connect(host=host,
                              user=user,
                              password=password,
                              db=db,
                              )

    def get_type_drink(self):
        with self.con.cursor() as cur:
            type_of_drink = []
            cur.execute("select name from type_of_drink")
            result = cur.fetchall()
            for drink in result:
                for i in drink:
                   type_of_drink.append(str(i))
            cur.close()
            return type_of_drink

    def get_drink(self, type):
        cur = self.con.cursor()
        drinks = []
        cur.execute(f"select name from name_drink where id_type_of_drink = (select id from type_of_drink where name = '{type}')")
        result = cur.fetchall()
        for drink in result:
            for i in drink:
                drinks.append(str(i))
        cur.close()
        return drinks

    def get_consumables(self, type):
        cur = self.con.cursor()
        drinks = []
        cur.execute(f"select name from name_drink where id_type_of_drink = (select id from type_of_drink where name = '{type}')")
        result = cur.fetchall()
        for drink in result:
            for i in drink:
                drinks.append(str(i))
        cur.close()
        return drinks

    def get_all_drink(self):
        cur = self.con.cursor()
        drinks = []
        cur.execute(f"select name from name_drink")
        result = cur.fetchall()
        for drink in result:
            for i in drink:
                drinks.append(str(i))
        cur.close()
        return drinks

    def get_name_drink_and_quantity(self):
        cur = self.con.cursor()
        drinks = []
        cur.execute(f"select name, quantity from name_drink")
        result = cur.fetchall()
        for drink in result:
            for i in drink:
                drinks.append(str(i))
        cur.close()
        return drinks

    def get_address(self):
        cur = self.con.cursor()
        addresses = []
        cur.execute(f"select address from bars")
        result = cur.fetchall()
        for addresse in result:
            for i in addresse:
                addresses.append(str(i))
        cur.close()
        return addresses


    def insert_order(self, address, name, quantity):
        cur = self.con.cursor()
        bars = []
        drinks = []
        cur.execute(f"select id from bars where address = '{address}'")
        result = cur.fetchall()
        for bar in result:
            for i in bar:
                bars.append(i)
        cur.execute(f"select id from name_drink where name = '{name}'")
        result = cur.fetchall()
        for drink in result:
            for i in drink:
                drinks.append(i)
        cur.execute(f"insert into orders (id_bar, id_name_drink, quantity) values ({bars[0]}, {drinks[0]}, {quantity})")
        self.con.commit()
        cur.close()

    def insert_drink(self, name, quantity):
        cur = self.con.cursor()
        cur.execute(f"update name_drink set quantity = quantity + {quantity} where name = '{name}'")
        self.con.commit()
        cur.close()

    def minus_drink(self, name, quantity):
        cur = self.con.cursor()
        cur.execute(f"update name_drink set quantity = quantity - {quantity} where name = '{name}'")
        self.con.commit()
        cur.close()

    def get_orders(self):
        info = []
        cur = self.con.cursor()
        cur.execute("select * from orders")
        for result in cur.fetchall():
            info.append(result)
        cur.close()
        return info


    def db_close(self):
        self.con.close()


