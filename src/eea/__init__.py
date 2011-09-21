try:
    # Declare this a namespace package if pkg_resources is available.
    import pkg_resources
    pkg_resources.declare_namespace('eea')
except ImportError: #pylint: disable-msg = W0704

    pass
