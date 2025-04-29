import re
import dns.resolver
from services import Colors

class Email_Validator:
    """
    HackTools -> Email Validator | Tool to validate email format and domain MX record.
    """

    EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    @staticmethod
    def validate_format(email: str) -> bool:
        """
        Validate the basic format of an email address using regex.
        """
        return re.match(Email_Validator.EMAIL_REGEX, email) is not None

    @staticmethod
    def validate_mx(email: str) -> bool:
        """
        Check if the domain part of the email has MX records.
        """
        domain = email.split('@')[-1]

        try:
            answers = dns.resolver.resolve(domain, 'MX')
            return len(answers) > 0

        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout) as e:
            print(Colors.RED + f"[Error] MX lookup failed: {e}" + Colors.END)
            return False

    @staticmethod
    def validate_email(email: str):
        """
        Full validation: format + domain MX
        """
        if not Email_Validator.validate_format(email):
            print(Colors.RED + "❌ Invalid email format." + Colors.END)
            return

        print(Colors.GREEN + "✔️ Format looks valid." + Colors.END)

        if Email_Validator.validate_mx(email):
            print(Colors.GREEN + "✔️ Domain has MX records (receives emails)." + Colors.END)
        else:
            print(Colors.RED + "❌ Domain has no MX records." + Colors.END)