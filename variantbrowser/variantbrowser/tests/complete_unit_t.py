import os
import unittest
import shutil
import sqlite3
from variantbrowser.dbutils import generate_db,  generate_user_db
from variantbrowser.importutils import importVcfXls
from variantbrowser.vb_app import get_config


class TestImport(unittest.TestCase):

    def test_sample_import(self):

        """
        Generate dbs.
        Copy and import a test sample.
        """

        if len(os.listdir("test_db")) != 0:
            shutil.rmtree("test_db")
            os.mkdir("test_db")

        generate_db('test_db/test_db.db')
        generate_user_db('test_db/test_db_user.db')

        self.assertTrue(os.path.isfile('test_db/test_db.db'))
        self.assertTrue(os.path.isfile('test_db/test_db_user.db'))
        
        if len(os.listdir("import")) != 0:
            shutil.rmtree("import")
            os.mkdir("import")
        
        shutil.copyfile("AOHC_PP-test_GX_0092_Result_300.zip", "import/AOHC_PP-test_GX_0092_Result_300.zip")
        shutil.copyfile("aohc_pp-test_variants.xlsx", "import/aohc_pp-test_variants.xlsx")

        importVcfXls("/illumina/analysis/dev/2024/sigvla/fullFres_dev_2024/fullFres/tests/import")

        #return None

        test_db = "test_db/test_db.db"
        comp_db = "comp.db"

        conn = sqlite3.connect(test_db)
        conn.execute("ATTACH ? AS db2", [comp_db])

        res1 = conn.execute("""SELECT * FROM main.variants
                            WHERE annotation_variant NOT IN
                                (SELECT annotation_variant FROM db2.variants)
                            """).fetchall()
        res2 = conn.execute("""SELECT * FROM db2.variants
                            WHERE annotation_variant NOT IN
                                (SELECT annotation_variant FROM main.variants)
                            """).fetchall()

        # They should both be empty if no difference.
        self.assertEqual(res1, [])
        self.assertEqual(res2, [])
    


# Cleanup that removes files from test/ import and test_db
        
if __name__ == '__main__':
    unittest.main()
