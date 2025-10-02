# -*- coding: utf-8 -*-

import unittest
import collections

from transforming_collections import KeyTransformingDict

LowercaseDictFirstKey = KeyTransformingDict.create('LowercaseDictFirstKey', str.lower)
LowercaseDictLastKey  = KeyTransformingDict.create('LowercaseDictFirstKey', str.lower, retain_first_key=False)

class LowercaseDictPreserveTest(unittest.TestCase):
	KEY_UNTRANSFORMED_1 = 'AbCαΒγАбВ'
	KEY_UNTRANSFORMED_1_2 = 'aBcΑβΓаБв'
	KEY_TRANSFORMED_1   = 'abcαβγабв'
	KEY_UNTRANSFORMED_2 = 'abcABC'
	KEY_TRANSFORMED_2   = 'abcabc'
	KEY_UNTRANSFORMED_3 = 'XYZxyz'
	KEY_TRANSFORMED_3   = 'xyzxyz'
	
	def test_fromkeys_preserve_first_key(self):
		source_keys = (self.KEY_UNTRANSFORMED_1, self.KEY_UNTRANSFORMED_1_2)
		
		d = LowercaseDictFirstKey.fromkeys(source_keys, 'fromkeys')
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "fromkeys should preserve the first key")
	
	def test_fromkeys_preserve_last_key(self):
		source_keys = (self.KEY_UNTRANSFORMED_1, self.KEY_UNTRANSFORMED_1_2)
		
		d = LowercaseDictLastKey.fromkeys(source_keys, 'fromkeys')
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "fromkeys should preserve the last key")
	
	def test_init_sibling_class_preserve_first_key(self):
		transformer = str.upper
		UppercaseDict = KeyTransformingDict.create('UppercaseDict', transformer)
		
		source_keys = (self.KEY_UNTRANSFORMED_1, self.KEY_UNTRANSFORMED_1_2)
		source_dict = UppercaseDict({key: 'value' for key in source_keys})
		
		d = LowercaseDictFirstKey(source_dict)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "init from sibling class should preserve the first key")
	
	
	def test_init_sibling_class_preserve_last_key(self):
		transformer = str.upper
		UppercaseDict = KeyTransformingDict.create('UppercaseDict', transformer, retain_first_key=False)
		
		source_keys = (self.KEY_UNTRANSFORMED_1, self.KEY_UNTRANSFORMED_1_2)
		source_dict = UppercaseDict({key: 'value' for key in source_keys})
		
		d = LowercaseDictLastKey(source_dict)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "init from sibling class should preserve the last key")
	
	def test_init_dict_preserve_first_key(self):
		source_keys = (self.KEY_UNTRANSFORMED_1, self.KEY_UNTRANSFORMED_1_2)
		source_dict = {key: 'value' for key in source_keys}
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d = LowercaseDictFirstKey(d2)
				keys = set(d)
				
				self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "init from dict should preserve the first key")
	
	def test_init_dict_preserve_last_key(self):
		source_keys = (self.KEY_UNTRANSFORMED_1, self.KEY_UNTRANSFORMED_1_2)
		source_dict = {key: 'value' for key in source_keys}
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d = LowercaseDictLastKey(d2)
				keys = set(d)
				
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "init from dict should preserve the last key")
	
	def test_init_list_preserve_first_key(self):
		source_keys = (self.KEY_UNTRANSFORMED_1, self.KEY_UNTRANSFORMED_1_2)
		source_list = [[key, 'value'] for key in source_keys]
		
		d = LowercaseDictFirstKey(source_list)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "init from list should preserve the first key")
	
	def test_init_list_preserve_last_key(self):
		source_keys = (self.KEY_UNTRANSFORMED_1, self.KEY_UNTRANSFORMED_1_2)
		source_list = [[key, 'value'] for key in source_keys]
		
		d = LowercaseDictLastKey(source_list)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "init from list should preserve the last key")
	
	def test_init_kwargs_preserve_first_key(self):
		source_keys = (self.KEY_UNTRANSFORMED_1, self.KEY_UNTRANSFORMED_1_2)
		source_kwargs = {key: 'value' for key in source_keys}
		
		d = LowercaseDictFirstKey(**source_kwargs)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "init from kwargs should preserve the first key")
	
	def test_init_kwargs_preserve_last_key(self):
		source_keys = (self.KEY_UNTRANSFORMED_1, self.KEY_UNTRANSFORMED_1_2)
		source_kwargs = {key: 'value' for key in source_keys}
		
		d = LowercaseDictLastKey(**source_kwargs)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "init from kwargs should preserve the last key")
	
	def test_init_dict_kwargs_preserve_dict_key(self):
		source_dict   = {self.KEY_UNTRANSFORMED_1: 'dict'}
		source_kwargs = {self.KEY_UNTRANSFORMED_1_2: 'kwargs'}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			LowercaseDictFirstKey(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d = LowercaseDictFirstKey(d2, **source_kwargs)
				keys = set(d)
				
				self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "init from dict and kwargs should preserve dict key")
	
	def test_init_dict_kwargs_preserve_kwargs_key(self):
		source_dict   = {self.KEY_UNTRANSFORMED_1: 'dict'}
		source_kwargs = {self.KEY_UNTRANSFORMED_1_2: 'kwargs'}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			LowercaseDictLastKey(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d = LowercaseDictLastKey(d2, **source_kwargs)
				keys = set(d)
				
				self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "init from dict and kwargs should preserve kwargs key")
	
	def test_init_list_kwargs_preserve_list_key(self):
		source_list   = [[self.KEY_UNTRANSFORMED_1, 'list']]
		source_kwargs = {self.KEY_UNTRANSFORMED_1_2: 'kwargs'}
		
		d = LowercaseDictFirstKey(source_list, **source_kwargs)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "init from list and kwargs should preserve list key")
	
	def test_init_list_kwargs_preserve_kwargs_key(self):
		source_list   = [[self.KEY_UNTRANSFORMED_1, 'list']]
		source_kwargs = {self.KEY_UNTRANSFORMED_1_2: 'kwargs'}
		
		d = LowercaseDictLastKey(source_list, **source_kwargs)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "init from list and kwargs should preserve kwargs key")
	
	def test_update_sibling_class_preserve_first_key(self):
		transformer = str.upper
		UppercaseDict = KeyTransformingDict.create('UppercaseDict', transformer)
		
		ld = LowercaseDictFirstKey({self.KEY_UNTRANSFORMED_1: 'untransformed'})
		ud = UppercaseDict({self.KEY_UNTRANSFORMED_1_2: 'untransformed2'})
		
		ld.update(ud)
		keys = set(ld)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "update with sibling class should preserve the first key")
	
	def test_update_sibling_class_preserve_last_key(self):
		transformer = str.upper
		UppercaseDict = KeyTransformingDict.create('UppercaseDict', transformer)
		
		ld = LowercaseDictLastKey({self.KEY_UNTRANSFORMED_1: 'untransformed'})
		ud = UppercaseDict({self.KEY_UNTRANSFORMED_1_2: 'untransformed2'})
		
		ld.update(ud)
		keys = set(ld)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "update with sibling class should preserve the last key")
	
	def test_update_dict_preserve_first_key(self):
		source_dict = {self.KEY_UNTRANSFORMED_1_2: 'dict'}
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			LowercaseDictFirstKey(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d = LowercaseDictFirstKey({self.KEY_UNTRANSFORMED_1: 'original'})
				
				d.update(d2)
				keys = set(d)
				
				self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "update with dict should preserve the first key")
	
	def test_update_dict_preserve_last_key(self):
		source_dict = {self.KEY_UNTRANSFORMED_1_2: 'dict'}
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			LowercaseDictLastKey(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d = LowercaseDictLastKey({self.KEY_UNTRANSFORMED_1: 'original'})
				
				d.update(d2)
				keys = set(d)
				
				self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "update with dict should preserve the last key")
	
	def test_update_list_preserve_first_key(self):
		source_list = [[self.KEY_UNTRANSFORMED_1_2, 'list']]
		d = LowercaseDictFirstKey({self.KEY_UNTRANSFORMED_1: 'original'})
		
		d.update(source_list)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "update with list should preserve the first key")
	
	def test_update_list_preserve_last_key(self):
		source_list = [[self.KEY_UNTRANSFORMED_1_2, 'list']]
		d = LowercaseDictLastKey({self.KEY_UNTRANSFORMED_1: 'original'})
		
		d.update(source_list)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "update with list should preserve the last key")
	
	def test_update_kwargs_preserve_first_key(self):
		source_kwargs = {self.KEY_UNTRANSFORMED_1_2: 'kwargs'}
		d = LowercaseDictFirstKey({self.KEY_UNTRANSFORMED_1: 'original'})
		
		d.update(**source_kwargs)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "update with kwargs should preserve the first key")
	
	def test_update_kwargs_preserve_last_key(self):
		source_kwargs = {self.KEY_UNTRANSFORMED_1_2: 'kwargs'}
		d = LowercaseDictLastKey({self.KEY_UNTRANSFORMED_1: 'original'})
		
		d.update(**source_kwargs)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "update with kwargs should preserve the last key")
	
	def test_update_dict_kwargs_preserve_dict_key(self):
		source_dict   = {self.KEY_UNTRANSFORMED_1: 'dict'}
		source_kwargs = {self.KEY_UNTRANSFORMED_1_2: 'kwargs'}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			LowercaseDictFirstKey(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d = LowercaseDictFirstKey()
				
				d.update(d2, **source_kwargs)
				keys = set(d)
				
				self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "update with dict and kwargs should preserve dict key")
	
	def test_update_dict_kwargs_preserve_kwargs_key(self):
		source_dict   = {self.KEY_UNTRANSFORMED_1: 'dict'}
		source_kwargs = {self.KEY_UNTRANSFORMED_1_2: 'kwargs'}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			LowercaseDictLastKey(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d = LowercaseDictLastKey()
				
				d.update(d2, **source_kwargs)
				keys = set(d)
				
				self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "update with dict and kwargs should preserve kwargs key")
	
	def test_update_list_kwargs_preserve_list_key(self):
		source_list   = [[self.KEY_UNTRANSFORMED_1, 'list']]
		source_kwargs = {self.KEY_UNTRANSFORMED_1_2: 'kwargs'}
		d = LowercaseDictFirstKey()
		
		d.update(source_list, **source_kwargs)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "update with list and kwargs should preserve list key")
	
	def test_update_list_kwargs_preserve_kwargs_key(self):
		source_list   = [[self.KEY_UNTRANSFORMED_1, 'list']]
		source_kwargs = {self.KEY_UNTRANSFORMED_1_2: 'kwargs'}
		d = LowercaseDictLastKey()
		
		d.update(source_list, **source_kwargs)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "update with list and kwargs should preserve kwargs key")
	
	def test_setitem_preserve_first_key(self):
		d = LowercaseDictFirstKey({self.KEY_UNTRANSFORMED_1: 1})
		
		d[self.KEY_UNTRANSFORMED_1_2] = 2
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "setting a different key, but same up to transformation, should preserve the first key")
	
	def test_setitem_preserve_last_key(self):
		d = LowercaseDictLastKey({self.KEY_UNTRANSFORMED_1: 1})
		
		d[self.KEY_UNTRANSFORMED_1_2] = 2
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "setting a different key, but same up to transformation, should preserve the last key")
	
	def test_setdefault_present_preserve_key_first(self):
		d = LowercaseDictFirstKey({self.KEY_UNTRANSFORMED_1: 1})
		
		d.setdefault(self.KEY_UNTRANSFORMED_1_2)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "setdefault with different key, but same up to transformation, should preserve the first key")
	
	def test_setdefault_present_preserve_key_last(self):
		d = LowercaseDictLastKey({self.KEY_UNTRANSFORMED_1: 1})
		
		d.setdefault(self.KEY_UNTRANSFORMED_1_2)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "setdefault with different key, but same up to transformation, should preserve the first key")
	
	def test_copy_method_preserve_key_first(self):
		d = LowercaseDictFirstKey({self.KEY_UNTRANSFORMED_1: 1})
		d_copy = d.copy()
		keys = set(d_copy)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "copy method should preserve original key")
	
	
	def test_copy_method_preserve_key_last(self):
		d = LowercaseDictLastKey({self.KEY_UNTRANSFORMED_1: 1})
		d_copy = d.copy()
		keys = set(d_copy)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "copy method should preserve original key")
	
	def test_copy_preserve_key_first(self):
		import copy
		
		d = LowercaseDictFirstKey({self.KEY_UNTRANSFORMED_1: 1})
		d_copy = copy.copy(d)
		keys = set(d_copy)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "copy should preserve original key")
	
	def test_copy_preserve_key_last(self):
		import copy
		
		d = LowercaseDictLastKey({self.KEY_UNTRANSFORMED_1: 1})
		d_copy = copy.copy(d)
		keys = set(d_copy)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "copy should preserve original key")
	
	def test_deepcopy_preserve_key_first(self):
		import copy
		
		d2 = LowercaseDictFirstKey({self.KEY_UNTRANSFORMED_1_2: 2})
		d = LowercaseDictFirstKey({self.KEY_UNTRANSFORMED_1: d2})
		d_copy = copy.deepcopy(d)
		d2_copy = d_copy[self.KEY_UNTRANSFORMED_1]
		
		keys = set(d_copy)
		keys2 = set(d2_copy)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "outer copy should preserve original key")
		self.assertEqual(keys2, {self.KEY_UNTRANSFORMED_1_2}, "inner copy should preserve original key")
	
	
	def test_deepcopy_preserve_key_last(self):
		import copy
		
		d2 = LowercaseDictLastKey({self.KEY_UNTRANSFORMED_1_2: 2})
		d = LowercaseDictLastKey({self.KEY_UNTRANSFORMED_1: d2})
		d_copy = copy.deepcopy(d)
		d2_copy = d_copy[self.KEY_UNTRANSFORMED_1]
		
		keys = set(d_copy)
		keys2 = set(d2_copy)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "outer copy should preserve original key")
		self.assertEqual(keys2, {self.KEY_UNTRANSFORMED_1_2}, "inner copy should preserve original key")
	
	def test_or_preserve_first_key(self):
		source_dict = {
			self.KEY_UNTRANSFORMED_1_2: 1,
		}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			LowercaseDictFirstKey(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d1 = LowercaseDictFirstKey({self.KEY_UNTRANSFORMED_1: 1})
				
				d3 = d1 | d2
				keys = set(d3)
				
				self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "or should preserve the first key")
	
	def test_or_preserve_last_key(self):
		source_dict = {
			self.KEY_UNTRANSFORMED_1_2: 1,
		}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			LowercaseDictLastKey(source_dict),
		)
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d1 = LowercaseDictLastKey({self.KEY_UNTRANSFORMED_1: 1})
				
				d3 = d1 | d2
				keys = set(d3)
				
				self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "or should preserve the last key")
	
	def test_ror_preserve_first_key(self):
		source_dict = {
			self.KEY_UNTRANSFORMED_1_2: 1,
		}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			LowercaseDictFirstKey(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d1 = LowercaseDictFirstKey({self.KEY_UNTRANSFORMED_1: 1})
				
				d3 = d2 | d1
				keys = set(d3)
				
				self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "ror should preserve the first key")	
	
	def test_ror_preserve_last_key(self):
		source_dict = {
			self.KEY_UNTRANSFORMED_1_2: 1,
		}
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			LowercaseDictLastKey(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d1 = LowercaseDictLastKey({self.KEY_UNTRANSFORMED_1: 1})
				
				d3 = d2 | d1
				keys = set(d3)
				
				self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "ror should preserve the last key")
	
	def test_ior_preserve_first_key(self):
		source_dict = {
			self.KEY_UNTRANSFORMED_1_2: 1,
		}
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			LowercaseDictFirstKey(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d1 = LowercaseDictFirstKey({self.KEY_UNTRANSFORMED_1: 1})
				
				d1 |= d2
				keys = set(d1)
				
				self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "ior should preserve the first key")
	
	def test_ior_preserve_last_key(self):
		source_dict = {
			self.KEY_UNTRANSFORMED_1_2: 1,
		}
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			LowercaseDictLastKey(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d1 = LowercaseDictLastKey({self.KEY_UNTRANSFORMED_1: 1})
				
				d1 |= d2
				keys = set(d1)
				
				self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "ior should preserve the last key")

if __name__ == '__main__':
	unittest.main()
