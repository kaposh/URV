"""Helper class wrapping the return object from pyodbc query."""


class Rows:
    """
    Wrap the pyodbc execute object and make all the operation easier.

    ...

    Attributes
    ----------
    list_of_rows : list of Row
        The output of execute method of pyodbc connection

    ...

    Methods
    -------
    row_count():
        Gets a number of rows
    get_row(row_number):
        Gets a list of items of the table row by index
    """

    def __init__(self, list_of_rows):
        """
        Transform the data from list_of_rows into the list of dictionaries.

        Parameters
        ----------
        list_of_rows : list of Row
            List of Row objects taken from fetchall() method.

        """
        self.rows_list = []
        for row in list_of_rows:
            columns = [column[0] for column in row.cursor_description]
            self.rows_list.append(dict(zip(columns, row)))

    def __iter__(self):
        """Use the rows_list __iter__ when iterating this object."""
        return self.rows_list.__iter__()

    def __getitem__(self, column_name):
        """
        Get a generator of existing reporting databases names.

        Parameters
        ----------
        column_name : str
            Name of column

        Returns
        -------
        generator
            Generator of items of the table column by name

        """
        return (row[column_name] for row in self.rows_list)

    def get_row(self, row_number):
        """
        Get a list of items of the table row by index.

        Parameters
        ----------
        row_number : int
            The index of row

        Returns
        -------
        list
            List of items of the table row by index

        """
        return self.rows_list[row_number]

    @property
    def row_count(self):
        """
        Get a number of rows from the query.

        Returns
        -------
        int
            Number of rows

        """
        return len(self.rows_list)
