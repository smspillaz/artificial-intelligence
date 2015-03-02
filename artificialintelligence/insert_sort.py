# /tests/insert_sort.py
#
# Simple insert 
#
# See LICENCE.md for Copyright information
"""Loader module."""

class InsertSort(object):

    """Encapsulates the 'insert sort' algorithm."""

    def __init__(self, data):
        """Initialize."""

        super(InsertSort, self).__init__()
        self.data = data
        self.position = 1

    def iterate(self):
        """Do one sort iteration."""

        if self.position < len (self.data):
            j = self.position
            while j > 1:
                if self.data[j] < self.data[j - 1]:
                    tmp = self.data[j - 1]
                    self.data[j - 1] = self.data[j]
                    self.data[j] = tmp

                j -= 1

            self.position += 1
            return True

        return False


    def current_list(self):
        return self.data
