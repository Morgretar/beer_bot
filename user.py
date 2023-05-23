class User:
    def __init__(self, telegram_id):
        self.telegram_id = telegram_id
        self.order = []
        self.quant = []
        self.address = ""
        self.comment = ""
        self.delivery_data = 0
