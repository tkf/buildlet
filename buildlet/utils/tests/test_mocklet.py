from .. import _pickle as pickle

from .. import mocklet


def test_mocklet_can_be_pickled():
    m = mocklet.Mock()
    m(a=1, b=2)
    s = pickle.dumps(m)
    l = pickle.loads(s)
    l.assert_called_once_with(a=1, b=2)
