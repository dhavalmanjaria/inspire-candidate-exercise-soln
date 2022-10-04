class ValidateWombatPostDTO:
    """We use DTOs for function return values so as to not use confusing tuples.

    Explicit is better than implicit
    """
    def __init__(self, is_error, message):
        self.is_error = is_error
        self.message = message