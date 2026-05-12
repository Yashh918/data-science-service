from utils.messageUtil import MessageUtil
from service.llmService import LLMService
from schema.expense import Expense

class MessageService:
    def __init__(self):
        self.messageUtil = MessageUtil()
        self.llmService = LLMService()

    def process_message(self, message):
        if not self.messageUtil.isBankSms(message):
            return None 

        # tier 1 regex
        extracted = self.messageUtil.extractExpense(message)
        if self.messageUtil._confidence(extracted):   
            return Expense(
                amount= extracted["amount"],
                merchant=extracted["merchant"],
                currency=extracted["currency"] or "INR",
                transaction_type=extracted["transaction_type"],
                transaction_date=extracted["transaction_date"],
            )

        # tier 2 llm fallback
        return self.llmService.runLLM(message) 
            