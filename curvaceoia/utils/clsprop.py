from collections.abc import Callable
from typing import Any, Generic, TypeVar


__all__ = []

MT = TypeVar('MT', bound=Any)
RT = TypeVar('RT')
class classproperty(Generic[MT, RT]):
	"""
	Class property attribute. 
	"""

	def __init__(self, fget: Callable[[type[MT]], RT], /) -> None:
		self.fget = classmethod(fget)

	def __get__(self, instance: MT | None, objtype: type[MT], /) -> RT:
		return self.fget.__get__(instance, objtype)()