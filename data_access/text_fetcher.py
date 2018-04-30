class Fetcher():
    """
    Parent class for Fetcher, classes that access data stored in files or databases
    """
    def __init__(self):
        pass

    def is_in(self, word, file):
        pass

class Text_Fetcher(Fetcher):
    location_table = {
        "lemma": "./data_access/data/lemma.txt",
        "stop": "./data_access/data/stop.txt"
    }
    
    def __init__(self):
        pass    

    def is_in(self, word, table):
        try:
            file_path = Text_Fetcher.location_table[table]
        except KeyError:
            raise KeyError("Table '{}' does not exist.".format(table))
        with open(Text_Fetcher.location_table[table]) as file:
            for l in file:
                if l.strip() == word:
                    return True
        return False


if __name__ == "__main__":
    import unittest
    class Text_Fetcher_Tests(unittest.TestCase):
        def test_is_in(self):
            tf = Text_Fetcher()
            self.assertTrue(tf.is_in("apple", "lemma"))
            self.assertTrue(tf.is_in("eat", "lemma"))          
            self.assertFalse(tf.is_in("123", "lemma"))
            self.assertFalse(tf.is_in("app", "lemma"))
            with self.assertRaises(KeyError):
                tf.is_in("que", "not")
    unittest.main()



