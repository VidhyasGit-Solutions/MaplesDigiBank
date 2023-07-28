from enum import Enum as PyEnum


class StatusEnum(PyEnum):
    IN_PROGRESS = "Inprogress"
    NOT_ASSIGNED = "NotAssigned"
    UNDER_REVIEW = "UnderReview"
    COMPLETED = "Completed"
    STARTED = "Started"
    NEW = "New"
    REJECTED = "Rejected"


class AccountTypeEnum(PyEnum):
    CHECKING_ACCOUNT = "CheckingAccount"
    SAVINGS_ACCOUNT = "SavingAccount"
