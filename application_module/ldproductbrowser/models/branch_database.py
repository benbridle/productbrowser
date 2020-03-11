from enum import Enum
from ldproductbrowser.models import _BaseDatabaseModel
from ldproductbrowser import globals as ldglobal


class Island(Enum):
    NORTH = 0
    SOUTH = 1


class Branch:
    def __init__(self, branch_id, name):
        self.name = name
        self.branch_id = branch_id
        self.abbreviation = ""
        self.latitude = None
        self.longitude = None
        self._island = None

    def __repr__(self):
        return f"<Branch {self.branch_id} '{self.name}'>"

    def __eq__(self, other):
        return self.branch_id == other.branch_id

    def __hash__(self):
        return self.branch_id

    @classmethod
    def from_cursor(cls, cursor):
        row = cursor.fetchone()
        return cls.from_row(row, cursor.description)

    @classmethod
    def from_row(cls, row, description):
        headers = [header[0] for header in description]  # pull column headers from cursor description
        branch_attr = dict(zip(headers, row))

        branch = cls(branch_attr["id"], branch_attr["name"])
        branch.set_coordinates(branch_attr["latitude"], branch_attr["longitude"])
        branch.abbreviation = branch_attr["abbreviation"]
        branch.island = Island(branch_attr["island_id"])
        return branch

    @property
    def island(self):
        return self._island

    @island.setter
    def island(self, new_island):
        if not isinstance(new_island, Island):
            raise TypeError("new_island must be a member of the Island enum")
        self._island = new_island

    def set_coordinates(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


class BranchDatabase(_BaseDatabaseModel):
    """
    Model for querying branch information at a high level.
    """

    def __init__(self, database_file_path):
        super().__init__(database_file_path)

    def get_branch(self, branch_id):
        c = self.execute("SELECT * FROM branches WHERE id=?", [branch_id])
        return Branch.from_cursor(c)

    def get_all_branches(self):
        c = self.execute("SELECT * FROM branches")
        branches = [Branch.from_row(row, c.description) for row in c.fetchall()]
        return branches

    def get_all_branch_ids(self):
        c = self.execute("SELECT id FROM branches")
        return [row[0] for row in c.fetchall()]

    def get_branch_from_name(self, name):
        results1 = self.execute("SELECT id FROM branches WHERE name=?", [name]).fetchone()
        results2 = self.execute("SELECT id FROM branches WHERE stockenq_name=?", [name]).fetchone()
        try:
            branch_id = (results1 or results2)[0]
        except TypeError:
            return None
        return self.get_branch(branch_id)

    def get_sorted_branches(self, island=None):
        if island and not isinstance(island, Island):
            raise TypeError("island must be a member of Island enum")
        query = "SELECT id FROM branches "
        if island:
            query += "WHERE island_id=? "
        query += "ORDER BY latitude DESC"
        parameters = []
        if island:
            parameters = [island.value]
        results = self.execute(query, parameters).fetchall()
        branches = [self.get_branch(result[0]) for result in results]
        return branches

    def get_all_branch_ids(self):
        results = self.execute("SELECT id FROM branches").fetchall()
        return [result[0] for result in results]
