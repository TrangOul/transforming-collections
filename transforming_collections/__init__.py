# -*- coding: utf-8 -*-

from .key_transforming_dict import KeyTransformingDict


class LowercaseDict(KeyTransformingDict):
	@staticmethod
	def transform_key(key):
		if isinstance(key, str):
			return key.lower()
		return key


class UnicaseDict(KeyTransformingDict):
	@staticmethod
	def transform_key(key):
		if isinstance(key, str):
			return key.casefold()
		return key


__all__ = [
	'LowercaseDict',
	'UnicaseDict',
	'KeyTransformingDict',
]
