class Journal:
    """This is Journal class with his functionality"""
    def __init__(self):
        self.entries = []
        self.count = 0

    def add_entry(self, text):
        self.entries.append(f"{self.count}: {text}")
        self.count += 1

    def remove_entry(self, pos):
        del self.entries[pos]

    def __str__(self):
        return "\n".join(self.entries)

    # this code will break SRP and makes god object
    # def save(self, filename):
    #     file = open(filename, "w")
    #     file.write(str(self))
    #     file.close()
    #
    # def load(self, filename):
    #     pass
    #
    # def load_from_web(self, uri):
    #     pass


class PersistenceManager:
    """This class is used for separation of responsibility (data persistence)"""

    @staticmethod
    def save_to_file(self, journal, file_path):
        file = open(file_path, "w")
        file.write(str(journal))
        file.close()


# usage example
if __name__ == '__main__':
    j = Journal()
    j.add_entry("I rode a bike.")
    j.add_entry("I ate a bug.")
    print(f"Journal entries:\n{j}\n")

    p = PersistenceManager()
    filepath = r'/tmp/journal.txt'  # or c:\temp\journal.txt
    p.save_to_file(j, filepath)

    # verify!
    with open(filepath) as fh:
        print(fh.read())
