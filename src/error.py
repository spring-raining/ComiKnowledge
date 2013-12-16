# -*- coding: utf-8 -*-


class FormBlankError(Exception):
    def __init__(self, form):
        self.form = form

    def __str__(self):
        return self.form + " must not be blank"


class FormDuplicateError(Exception):
    def __init__(self, form):
        self.form = form

    def __str__(self):
        return self.form + " must be unique"


class FormInvalidError(Exception):
    def __init__(self, form):
        self.form = form

    def __str__(self):
        return "Invalid form: " + self.form


class ChecklistInvalidError(Exception):
    def __str__(self):
        return "Invalid checklist"


class ChecklistVersionError(Exception):
    def __str__(self):
        return 'This version cannot be read now'

class TooMuchCommentsError(Exception):
    def __str__(self):
        return "Comments are too much"

if __name__ == "__main__":
    # なにも書かないで
    pass
