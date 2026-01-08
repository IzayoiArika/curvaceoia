__all__ = [
	'enable_scaled_arctap',
	'uses_scaled_arctap',
	'accept_langcode_kr',
	'accepts_langcode_kr',
]


from typing import Any
from pydantic import ConfigDict

from curvaceoia.utils.clsprop import classproperty


__enable_scaled_arctap__: bool = False
def enable_scaled_arctap() -> None:
	global __enable_scaled_arctap__
	__enable_scaled_arctap__ = True

def uses_scaled_arctap() -> bool:
	global __enable_scaled_arctap__
	return __enable_scaled_arctap__

__reject_langcode_kr__: bool = True
def accept_langcode_kr() -> None:
	global __reject_langcode_kr__
	__reject_langcode_kr__ = False

def accepts_langcode_kr() -> bool:
	global __reject_langcode_kr__
	return __reject_langcode_kr__


def get_default_model_cfg(ignored_types: Any = None) -> ConfigDict:
	if ignored_types is None:
		ignored_types = ()

	return ConfigDict(
		extra='forbid',
		validate_assignment=True,
		validate_default=True,
		ignored_types=ignored_types + (classproperty, ),
		allow_inf_nan=False,
	)