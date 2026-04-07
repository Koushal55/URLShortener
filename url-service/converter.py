class Base62Converter:
    # The 62 characters used for encoding
    CHARSET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    @classmethod
    def encode(cls, num: int) -> str:
        """Converts a unique integer ID to a Base62 string."""
        if num == 0:
            return cls.CHARSET[0]
        
        arr = []
        base = len(cls.CHARSET)
        while num:
            num, rem = divmod(num, base)
            arr.append(cls.CHARSET[rem])
        
        arr.reverse()
        return ''.join(arr)

    @classmethod
    def decode(cls, string: str) -> int:
        """Converts a Base62 string back to the unique integer ID."""
        base = len(cls.CHARSET)
        strlen = len(string)
        num = 0
        
        idx = 0
        for char in string:
            power = (strlen - (idx + 1))
            num += cls.CHARSET.index(char) * (base ** power)
            idx += 1
        return num