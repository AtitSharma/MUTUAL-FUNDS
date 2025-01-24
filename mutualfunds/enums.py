from django.db import models


class MutualFundsChoice(models.TextChoices):
    EQUITY = "EQUITY"
    DEBT = "DEBT"
    HYBRID = "HYBRID"