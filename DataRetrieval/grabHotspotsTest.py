import getpass
import unittest
from grabHotspots import code_churn

def test_code_churn():

    assert code_churn( 100, 100 ) == 0, "No code churn for no deletions"

    assert code_churn( 0, 0 ) == 0, "No code churn for nothing done"

    assert code_churn( 50, 100 ) == 50, "50 percent code churn if half was deleted"

    assert code_churn( 200, 0 ) == 100, "should just return 100 for pure deletions"

test_code_churn()

print "tests passed"

