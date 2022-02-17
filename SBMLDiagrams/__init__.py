# try:
#   from . import _version
# except:
#     from SBMLDiagrams import _version

# __version__ = _version.__version__

try:
    from . import visualizeSBML
    from . import drawNetwork
    from . import processSBML
    from . import editSBML
    from . import exportSBML
    from . import styleSBML
    from . import autoLayoutSBML
    from. import visualizeInfo
except:
    from SBMLDiagrams import visualizeSBML
    from SBMLDiagrams import drawNetwork
    from SBMLDiagrams import processSBML
    from SBMLDiagrams import editSBML
    from SBMLDiagrams import exportSBML
    from SBMLDiagrams import styleSBML
    from SBMLDiagrams import autoLayoutSBML
    from SBMLDiagrams import visualizeInfo

from SBMLDiagrams._version import __version__

from SBMLDiagrams.processSBML import *
from SBMLDiagrams.visualizeSBML import *
