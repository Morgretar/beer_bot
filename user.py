class User:
    def __init__(self, telegram_id):
        self.telegram_id = telegram_id
        self.order = []
        self.quant = []
        self.info = {}
        self.address = ""
        self.comment = ""
        self.delivery_data = 0


    def __del__(self):
        print("Объект удалён")
