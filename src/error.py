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


if __name__ == "__main__":
    # なにも書かないで
    pass
