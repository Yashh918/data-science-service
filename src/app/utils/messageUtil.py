import re
from datetime import datetime

class MessageUtil:
    def isBankSms(self, message):
        words_to_seach = ['bank', 'bank', 'credited', 'debited', 'spent', 'payment']
        pattern =  r'\b(' + '|'.join(map(re.escape, words_to_seach)) + r')\b'
        return bool(re.search(pattern, message, re.IGNORECASE))

    def extractExpense(self, message):
        transaction_type = self._extractTransactionType(message)
        return {
            "transaction_type": transaction_type,
            "currency": self._extractCurrency(message),
            "amount": self._extractAmount(message),
            "merchant": self._extractMerchant(message),
            "transaction_date": self._extractDate(message)
        }
    
    def _extractTransactionType(self, message):
        debit_words = ["debited", "spent", "txn", "transaction", "transfer", "transferred", "withdrawn", "withdrawal", "purchase", "used"]
        credit_words = ["credited", "received", "deposited", "refund", "refunded", "reversed", "cr"]

        debit_pattern = r'\b(' + '|'.join(map(re.escape, debit_words)) + r')\b'
        credit_pattern = r'\b(' + '|'.join(map(re.escape, credit_words)) + r')\b'

        has_debit = bool(re.search(debit_pattern, message, re.IGNORECASE))
        has_credit = bool(re.search(credit_pattern, message, re.IGNORECASE))

        if has_debit:
            return "DEBIT"
        elif has_credit:
            return "CREDIT"
        return None

    def _extractCurrency(self, message):
        pattern = r'\b(Rs\.?|INR|₹)\b'
        if re.search( pattern, message, re.IGNORECASE):
            return "INR"
        return None
    
    def _extractAmount(self, message):
        pattern = r'(?:Rs\.?|INR)\s*([\d,]+(?:\.\d{1,2})?)'
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            return match.group(1).replace(',', '')
        return None
    
    def _extractMerchant(self, message):
        pattern = r'([a-zA-Z\s\-]+?)\s+credited\b'
        matches = re.findall(pattern, message, re.IGNORECASE)
        if matches:
            return matches[-1].strip()
        
        fallback = r'(?:at|to|towards|from)\s+([A-Za-z0-9@./\-& ]+?)(?=\s*(?:on|via|ref|\.))'
        match = re.search(fallback, message, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        return None

    def _extractDate(self, message):
        patterns = [
            # 27-APR-26 | 27-APR-2026
            (
                r'\b(\d{1,2})[\-](JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)[\-](\d{2,4})\b',
                lambda m: self._parseDate(
                    f"{m.group(1)} {m.group(2)} {m.group(3)}",
                    "%d %b %y" if len(m.group(3)) == 2 else "%d %b %Y"
                )
            ),
            # 29 APR
            (
                r'\b(\d{1,2})\s(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\b',
                lambda m: self._parseDate(
                    f"{m.group(1)} {m.group(2)} {datetime.now().year}",
                    "%d %b %Y"
                )
            ),
            # 28/04/2026
            (
                r'\b(\d{1,2})[-/](\d{1,2})[-/](\d{2,4})\b',
                lambda m: self._parseDate(
                    f"{m.group(1)}/{m.group(2)}/{m.group(3)}",
                    "%d/%m/%Y"
                )
            )
        ]

        for pattern, parser in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                result = parser(match)
                if result:
                    return result
        
        return None

    def _parseDate(self, date_str, fmt):
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            return None

    def _confidence(self, extracted: dict) -> bool:
        t = extracted["transaction_type"]
        if(t == "DEBIT"):
            return extracted["amount"] is not None and extracted["merchant"] is not None
        elif(t == "CREDIT"):
            return extracted["amount"] is not None