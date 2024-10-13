class Post:
    content: str
    filename: str

    def __init__(self, content: str, filename: str) -> None:
        self.content = content
        self.filename = filename

    def __str__(self) -> str:
        return f"""File Name: {self.filename}\n\nContent:\n\n{self.content}"""

    def __repr__(self):
        return f"Post(filename={self.filename}, content={self.content})"
