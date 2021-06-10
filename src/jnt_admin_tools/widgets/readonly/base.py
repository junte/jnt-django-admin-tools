import abc


class BaseReadOnlyWidget(abc.ABC):
    """Base readonly widget."""

    @abc.abstractmethod
    def render(self, field_value, field_name, **kwargs) -> str:
        """Render current widget."""
