from typing import Any, Literal
from pydantic import ConfigDict

from curvaceoia1.utils.clsprop import classproperty


__all__ = ['GlobalConfig', 'get_default_model_cfg']

class GlobalConfig:
	_scaled_arctap: bool = False
	_kr: bool = False

	@classmethod
	def enable_scaled_arctap(cls) -> None:
		cls._scaled_arctap = True
	
	@classmethod
	def uses_scaled_arctap(cls) -> bool:
		return cls._scaled_arctap


def get_default_model_cfg(
	extra: Literal['allow', 'ignore', 'forbid'] = 'forbid',
	ignored_types: Any = None
) -> ConfigDict:
	
	if ignored_types is None:
		ignored_types = ()

	return ConfigDict(
		extra=extra,
		validate_assignment=True,
		validate_default=True,
		ignored_types=ignored_types + (classproperty, ),
		allow_inf_nan=False,
	)