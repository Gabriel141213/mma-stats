class ScrapingException(Exception):
    """Exception base para erros de scraping"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"ScrapingException: {self.message}"

class RequestException(ScrapingException):
    """Exception para erros de requisição"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"RequestException: {self.message}"

class ParsingException(ScrapingException):
    """Exception para erros de parsing"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"ParsingException: {self.message}"