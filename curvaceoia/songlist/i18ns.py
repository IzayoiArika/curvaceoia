from typing import Any, ClassVar, Generic, TypeVar

from curvaceoia.songlist.model import AdvancedModel
from curvaceoia.utils.cfg import accepts_langcode_kr


__all__ = [
	'GuardinaError',
	'I18nAny', 'I18nStr', 'I18nStrs', 'I18nStrEnRequired', 'I18nBool'
]

T = TypeVar('T')

class GuardinaError(KeyError):
	"""
	Specifically refers to the incorrect use of `kr` instead of `ko` as the language code for Korean.
	- Named `GuardinaError` because lowiro made this stupid mistake in the songlist for the song γuarδina.
	"""
	def __init__(self) -> None:
		pass
	
	def __str__(self) -> str:
		return '\'kr\' is not a valid language code; do you mean \'ko\'?'

class I18nAny(AdvancedModel, Generic[T]):

	en: T | None = None
	ja: T | None = None

	ko: T | None = None
	zh_Hans: T | None = None
	zh_Hant: T | None = None

	ko_dialog: T | None = None

	val_aliases: ClassVar[dict[str, str]] = {
		'kr': 'ko',
		'zh-Hans': 'zh_Hans',
		'zh-Hant': 'zh_Hant',
	}
	ser_rev_map: ClassVar[dict[str, str]] = {
		'zh_Hans': 'zh-Hans',
		'zh_Hant': 'zh-Hant',
	}

	@classmethod
	def before_validation(cls, data: Any) -> Any:
		data = super().before_validation(data)
		if not isinstance(data, dict):
			return data
		
		if 'kr' in data and not accepts_langcode_kr():
			raise GuardinaError
		
		return data

I18nStr = I18nAny[str]
I18nStrs = I18nAny[list[str]]
class I18nStrEnRequired(I18nStr):
	en: str # type: ignore
I18nBool = I18nAny[bool]