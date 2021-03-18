class ErrorResponse:

    messages = []
    data = None

    def add_message(self, message):
        self.messages.append(message)

    def has_error(self):
        return len(self.messages) > 0
