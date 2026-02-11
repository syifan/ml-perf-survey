"""Tool adapters for the unified ML performance modeling prototype."""
from prototype.adapters.base import ToolAdapter
from prototype.adapters.timeloop_adapter import TimeloopAdapter
from prototype.adapters.analytical_adapter import AnalyticalAdapter

_ADAPTERS = {
    "timeloop": TimeloopAdapter,
    "analytical": AnalyticalAdapter,
}


def get_adapter(name: str):
    """Get an adapter class by name."""
    return _ADAPTERS.get(name.lower())


def list_adapters():
    """Return all registered adapters."""
    return dict(_ADAPTERS)
