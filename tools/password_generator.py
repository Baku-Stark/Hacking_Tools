import random
import string
from services import Colors

class PasswordGenerator:
    """
    HackTools -> Password Generator | Generates secure passwords at different levels of complexity.
    """

    @staticmethod
    def generate(level: str = 'medium', length: int = 12) -> str:
        """
        Generates password based on complexity level.
            :param level: 'simple', 'medium', ou 'strong'
            :param length: password size
            :return: password generated
        """
        if length < 4:
            print(Colors.RED + "[PasswordGenerator] Length too short! Use at least 4 characters." + Colors.END)
            return ""

        if level == 'simple':
            chars = string.ascii_lowercase
        elif level == 'medium':
            chars = string.ascii_letters + string.digits
        elif level == 'strong':
            chars = string.ascii_letters + string.digits + string.punctuation
        else:
            print(Colors.RED + "[PasswordGenerator] Invalid level! Use: simple, medium or strong." + Colors.END)
            return ""

        password = ''.join(random.choice(chars) for _ in range(length))
        print(Colors.GREEN + f"[PasswordGenerator] Password Generated ({level}): {password}" + Colors.END)
        return password