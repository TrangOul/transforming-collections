# -*- coding: utf-8 -*-

import unittest
import collections

from transforming_collections import KeyTransformingDict


class TestKeyTransformingDict(KeyTransformingDict):
	@staticmethod
	def transform_key(key):
		return str.lower(key)


class KeyTransformingDictBaseTestMixin:
	KEY_UNTRANSFORMED_1 = 'AbCαΒγАбВ'
	KEY_UNTRANSFORMED_1_2 = 'aBcΑβΓаБв'
	KEY_TRANSFORMED_1   = 'abcαβγабв'
	KEY_UNTRANSFORMED_2 = 'abcABC'
	KEY_TRANSFORMED_2   = 'abcabc'
	KEY_UNTRANSFORMED_3 = 'XYZxyz'
	KEY_TRANSFORMED_3   = 'xyzxyz'
	
	def test_subclassing(self):
		d = self.test_class()
		
		self.assertIsInstance(d,          collections.abc.MutableMapping)
		self.assertIsInstance(d.keys(),   collections.abc.KeysView)
		self.assertIsInstance(d.items(),  collections.abc.ItemsView)
		self.assertIsInstance(d.values(), collections.abc.ValuesView)
	
	def test_fromkeys_transform_key(self):
		source_keys = {self.KEY_UNTRANSFORMED_1}
		
		d = self.test_class.fromkeys(source_keys, 'fromkeys')
		
		self.assertEqual(len(d), 1, "fromkeys should create dict with one key")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
		self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
	
	def test_fromkeys_same_keys_up_to_transformation(self):
		source_keys = {self.KEY_UNTRANSFORMED_1, self.KEY_TRANSFORMED_1}
		
		d = self.test_class.fromkeys(source_keys, 'fromkeys')
			
		self.assertEqual(len(d), 1, "fromkeys should create dict with one key")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
		self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
	
	def test_fromkeys_multiple_keys(self):
		source_keys = {self.KEY_UNTRANSFORMED_1, self.KEY_UNTRANSFORMED_2}
		
		d = self.test_class.fromkeys(source_keys, 'fromkeys')
			
		self.assertEqual(len(d), 2, "fromkeys should create dict with both keys")
		self.assertIn(self.KEY_UNTRANSFORMED_1,   d, "untransformed key not found")
		self.assertIn(self.KEY_TRANSFORMED_1,     d,   "transformed key not found")
		self.assertIn(self.KEY_UNTRANSFORMED_2, d, "untransformed key not found")
		self.assertIn(self.KEY_TRANSFORMED_2,   d,   "transformed key not found")
	
	def test_fromkeys_preserve_first_key(self):
		source_keys = (self.KEY_UNTRANSFORMED_1, self.KEY_UNTRANSFORMED_1_2)
		
		d = self.test_class.fromkeys(source_keys, 'fromkeys')
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "fromkeys should preserve first key")
	
	def test_fromkeys_preserve_last_key(self):
		source_keys = (self.KEY_UNTRANSFORMED_1, self.KEY_UNTRANSFORMED_1_2)
		
		d = self.test_class.fromkeys(source_keys, 'fromkeys')
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "fromkeys should preserve last key")
	
	def test_init_sibling_class_transform_key(self):
		transformer = str.upper
		
		class UppercaseKeyDict(self.test_class.__bases__[0]):
			@staticmethod
			def transform_key(key):
				return transformer(key)
		
		source_dict = UppercaseKeyDict({self.KEY_UNTRANSFORMED_1: 'untransformed'})
		
		d = self.test_class(source_dict)
		keys = set(d)
		
		self.assertIn(self.KEY_TRANSFORMED_1, d, "transformed key not found in dict")
		self.assertIn(transformer(self.KEY_UNTRANSFORMED_1), d, "key transformed by other dict not found in dict")
		self.assertIn(self.KEY_UNTRANSFORMED_1, keys, "untransformed key not found in dict keys")
		self.assertNotIn(self.KEY_TRANSFORMED_1, keys, "transformed key found in dict keys")
		self.assertNotIn(transformer(self.KEY_UNTRANSFORMED_1), keys, "key transformed by other dict found in dict keys")
	
	def test_init_sibling_class_preserve_first_key(self):
		transformer = str.upper
		class UppercaseKeyDict(self.test_class.__bases__[0]):
			@staticmethod
			def transform_key(key):
				return transformer(key)
		source_keys = (self.KEY_UNTRANSFORMED_1, self.KEY_UNTRANSFORMED_1_2)
		source_dict = UppercaseKeyDict({key: 'value' for key in source_keys})
		
		d = self.test_class(source_dict)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "init from sibling class should preserve first key")
	
	
	def test_init_sibling_class_preserve_last_key(self):
		transformer = str.upper
		class UppercaseKeyDict(self.test_class.__bases__[0]):
			@staticmethod
			def transform_key(key):
				return transformer(key)
		source_keys = (self.KEY_UNTRANSFORMED_1, self.KEY_UNTRANSFORMED_1_2)
		source_dict = UppercaseKeyDict({key: 'value' for key in source_keys})
		
		d = self.test_class(source_dict)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "init from sibling class should preserve last key")
	
	def test_init_dict_transform_key(self):
		source_dict = {self.KEY_UNTRANSFORMED_1: 'untransformed'}
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d = self.test_class(d2)
				
				self.assertEqual(len(d), 1, "dict should have one key")
				self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
				self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
	
	def test_init_list_transform_key(self):
		source_list = [[self.KEY_UNTRANSFORMED_1, 'untransformed']]
		
		d = self.test_class(source_list)
		
		self.assertEqual(len(d), 1, "list should have one key")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
		self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
	
	def test_init_kwargs_transform_key(self):
		source_kwargs = {self.KEY_UNTRANSFORMED_1: 'untransformed'}
		
		d = self.test_class(**source_kwargs)
		
		self.assertEqual(len(d), 1, "dict should have one key")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
		self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
	
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
				d = self.test_class(d2)
				keys = set(d)
				
				self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "init from dict should preserve first key")
	
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
				d = self.test_class(d2)
				keys = set(d)
				
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "init from dict should preserve last key")
	
	def test_init_list_preserve_first_key(self):
		source_keys = (self.KEY_UNTRANSFORMED_1, self.KEY_UNTRANSFORMED_1_2)
		source_list = [[key, 'value'] for key in source_keys]
		
		d = self.test_class(source_list)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "init from list should preserve first key")
	
	def test_init_list_preserve_last_key(self):
		source_keys = (self.KEY_UNTRANSFORMED_1, self.KEY_UNTRANSFORMED_1_2)
		source_list = [[key, 'value'] for key in source_keys]
		
		d = self.test_class(source_list)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "init from list should preserve last key")
	
	def test_init_kwargs_preserve_first_key(self):
		source_keys = (self.KEY_UNTRANSFORMED_1, self.KEY_UNTRANSFORMED_1_2)
		source_kwargs = {key: 'value' for key in source_keys}
		
		d = self.test_class(**source_kwargs)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "init from kwargs should preserve first key")
	
	def test_init_kwargs_preserve_last_key(self):
		source_keys = (self.KEY_UNTRANSFORMED_1, self.KEY_UNTRANSFORMED_1_2)
		source_kwargs = {key: 'value' for key in source_keys}
		
		d = self.test_class(**source_kwargs)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "init from kwargs should preserve last key")
	
	def test_init_dict_overwrite_untransformed_by_transformed(self):
		source_dict = {self.KEY_UNTRANSFORMED_1: 'untransformed', self.KEY_TRANSFORMED_1: 'transformed'}
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				self.assertEqual(list(d2), [self.KEY_UNTRANSFORMED_1, self.KEY_TRANSFORMED_1], 'dict keys not in expected order')
				
				d = self.test_class(d2)
				
				self.assertEqual(len(d), 1, "dict should have one key")
				self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
				self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
				self.assertEqual(d[self.KEY_TRANSFORMED_1], 'transformed', "transformed key value not overwritten")
	
	def test_init_list_overwrite_untransformed_by_transformed(self):
		source_list = [[self.KEY_UNTRANSFORMED_1, 'untransformed'], [self.KEY_TRANSFORMED_1, 'transformed']]
		
		d = self.test_class(source_list)
		
		self.assertEqual(len(d), 1, "dict should have one key")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
		self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
		self.assertEqual(d[self.KEY_TRANSFORMED_1], 'transformed', "transformed key value not overwritten")
	
	def test_init_kwargs_overwrite_untransformed_by_transformed(self):
		source_kwargs = {self.KEY_UNTRANSFORMED_1: 'untransformed', self.KEY_TRANSFORMED_1: 'transformed'}
		self.assertEqual(len(source_kwargs), 2)
		self.assertEqual(list(source_kwargs), [self.KEY_UNTRANSFORMED_1, self.KEY_TRANSFORMED_1], 'kwargs keys not in expected order')
		
		d = self.test_class(**source_kwargs)
		
		self.assertEqual(len(d), 1, "dict should have one key")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
		self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
		self.assertEqual(d[self.KEY_TRANSFORMED_1], 'transformed', "transformed key value not overwritten")
	
	def test_init_dict_overwrite_transformed_by_untransformed(self):
		source_dict = {self.KEY_TRANSFORMED_1: 'transformed', self.KEY_UNTRANSFORMED_1: 'untransformed'}
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				self.assertEqual(list(d2), [self.KEY_TRANSFORMED_1, self.KEY_UNTRANSFORMED_1], 'dict keys not in expected order')
				
				d = self.test_class(d2)
				
				self.assertEqual(len(d), 1, "dict should have one key")
				self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
				self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
				self.assertEqual(d[self.KEY_TRANSFORMED_1], 'untransformed', "transformed key value not overwritten")
	
	def test_init_list_overwrite_transformed_by_untransformed(self):
		source_list = [[self.KEY_TRANSFORMED_1, 'transformed'], [self.KEY_UNTRANSFORMED_1, 'untransformed']]
		
		d = self.test_class(source_list)
		
		self.assertEqual(len(d), 1, "dict should have one key")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
		self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
		self.assertEqual(d[self.KEY_TRANSFORMED_1], 'untransformed', "transformed key value not overwritten")
	
	def test_init_kwargs_overwrite_transformed_by_untransformed(self):
		source_kwargs = {self.KEY_TRANSFORMED_1: 'transformed', self.KEY_UNTRANSFORMED_1: 'untransformed'}
		self.assertEqual(len(source_kwargs), 2)
		self.assertEqual(list(source_kwargs), [self.KEY_TRANSFORMED_1, self.KEY_UNTRANSFORMED_1], 'kwargs keys not in expected order')
		
		d = self.test_class(**source_kwargs)
		
		self.assertEqual(len(d), 1, "dict should have one key")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
		self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
		self.assertEqual(d[self.KEY_TRANSFORMED_1], 'untransformed', "transformed key value not overwritten")
	
	def test_init_dict_kwargs_add_both(self):
		source_dict   = {self.KEY_UNTRANSFORMED_1: 'dict'}
		source_kwargs = {self.KEY_UNTRANSFORMED_2: 'kwargs'}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			self.test_class(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d = self.test_class(d2, **source_kwargs)
				
				self.assertEqual(len(d), 2, "dict should have both keys")
				self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key from dict not found")
				self.assertIn(self.KEY_TRANSFORMED_1, d,   "transformed key from dict not found")
				self.assertIn(self.KEY_UNTRANSFORMED_2, d, "untransformed key from kwargs not found")
				self.assertIn(self.KEY_TRANSFORMED_2, d,   "transformed key from kwargs not found")
	
	def test_init_list_kwargs_add_both(self):
		source_list   = [[self.KEY_UNTRANSFORMED_1, 'dict']]
		source_kwargs = {self.KEY_UNTRANSFORMED_2: 'kwargs'}
		
		d = self.test_class(source_list, **source_kwargs)
		
		self.assertEqual(len(d), 2, "dict should have both keys")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key from list not found")
		self.assertIn(self.KEY_TRANSFORMED_1, d,   "transformed key from list not found")
		self.assertIn(self.KEY_UNTRANSFORMED_2, d, "untransformed key from kwargs not found")
		self.assertIn(self.KEY_TRANSFORMED_2, d,   "transformed key from kwargs not found")
	
	def test_init_dict_kwargs_overwrite_untransformed_by_transformed(self):
		source_dict   = {self.KEY_UNTRANSFORMED_1: 'dict'}
		source_kwargs = {self.KEY_TRANSFORMED_1: 'kwargs'}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			self.test_class(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d = self.test_class(d2, **source_kwargs)
				
				self.assertEqual(len(d), 1, "dict should have one key")
				self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
				self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
				self.assertEqual(d[self.KEY_TRANSFORMED_1], 'kwargs', "dict's untransformed key's value not overwritten by kwargs' transformed key's value")
	
	def test_init_list_kwargs_overwrite_untransformed_by_transformed(self):
		source_list   = [[self.KEY_UNTRANSFORMED_1, 'list']]
		source_kwargs = {self.KEY_TRANSFORMED_1: 'kwargs'}
		
		d = self.test_class(source_list, **source_kwargs)
		
		self.assertEqual(len(d), 1, "dict should have one key")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
		self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
		self.assertEqual(d[self.KEY_TRANSFORMED_1], 'kwargs', "list's untransformed key's value not overwritten by kwargs' transformed key's value")
	
	def test_init_dict_kwargs_overwrite_transformed_by_untransformed(self):
		source_dict   = {self.KEY_TRANSFORMED_1: 'dict'}
		source_kwargs = {self.KEY_UNTRANSFORMED_1: 'kwargs'}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			self.test_class(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d = self.test_class(d2, **source_kwargs)
				
				self.assertEqual(len(d), 1, "dict should have one key")
				self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
				self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
				self.assertEqual(d[self.KEY_TRANSFORMED_1], 'kwargs', "dict's transformed key's value not overwritten by kwargs' untransformed key's value")
	
	def test_init_list_kwargs_overwrite_transformed_by_untransformed(self):
		source_list   = [[self.KEY_TRANSFORMED_1, 'list']]
		source_kwargs = {self.KEY_UNTRANSFORMED_1: 'kwargs'}
		
		d = self.test_class(source_list, **source_kwargs)
		
		self.assertEqual(len(d), 1, "dict should have one key")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
		self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
		self.assertEqual(d[self.KEY_TRANSFORMED_1], 'kwargs', "list's transformed key value not overwritten by kwargs' untransformed key's value")
	
	def test_init_dict_kwargs_preserve_dict_key(self):
		source_dict   = {self.KEY_UNTRANSFORMED_1: 'dict'}
		source_kwargs = {self.KEY_UNTRANSFORMED_1_2: 'kwargs'}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			self.test_class(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d = self.test_class(d2, **source_kwargs)
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
			self.test_class(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d = self.test_class(d2, **source_kwargs)
				keys = set(d)
				
				self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "init from dict and kwargs should preserve kwargs key")
	
	def test_init_list_kwargs_preserve_list_key(self):
		source_list   = [[self.KEY_UNTRANSFORMED_1, 'list']]
		source_kwargs = {self.KEY_UNTRANSFORMED_1_2: 'kwargs'}
		
		d = self.test_class(source_list, **source_kwargs)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "init from list and kwargs should preserve list key")
	
	def test_init_list_kwargs_preserve_kwargs_key(self):
		source_list   = [[self.KEY_UNTRANSFORMED_1, 'list']]
		source_kwargs = {self.KEY_UNTRANSFORMED_1_2: 'kwargs'}
		
		d = self.test_class(source_list, **source_kwargs)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "init from list and kwargs should preserve kwargs key")
	
	def test_update_sibling_class_transform_key(self):
		transformer = str.upper
		
		class UppercaseKeyDict(self.test_class.__bases__[0]):
			@staticmethod
			def transform_key(key):
				return transformer(key)
		
		ld = self.test_class({self.KEY_UNTRANSFORMED_1: 'untransformed'})
		ud = UppercaseKeyDict({self.KEY_UNTRANSFORMED_1: 'untransformed2'})
		
		ld.update(ud)
		keys = set(ld)
		
		self.assertEqual(len(ld), 1, "dict should have one key")
		self.assertIn(self.KEY_TRANSFORMED_1, ld, "transformed key not found in dict")
		self.assertIn(transformer(self.KEY_UNTRANSFORMED_1), ld, "key transformed by other dict not found in dict")
		self.assertNotIn(self.KEY_TRANSFORMED_1, keys, "transformed key found in dict keys")
		self.assertNotIn(transformer(self.KEY_UNTRANSFORMED_1), keys, "key transformed by other dict found in dict keys")
	
	def test_update_sibling_class_preserve_first_key(self):
		transformer = str.upper
		
		class UppercaseKeyDict(self.test_class.__bases__[0]):
			@staticmethod
			def transform_key(key):
				return transformer(key)
		
		ld = self.test_class({self.KEY_UNTRANSFORMED_1: 'untransformed'})
		ud = UppercaseKeyDict({self.KEY_UNTRANSFORMED_1_2: 'untransformed2'})
		
		ld.update(ud)
		keys = set(ld)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "update with sibling class should preserve first key")
	
	def test_update_sibling_class_preserve_last_key(self):
		transformer = str.upper
		
		class UppercaseKeyDict(self.test_class.__bases__[0]):
			@staticmethod
			def transform_key(key):
				return transformer(key)
		
		ld = self.test_class({self.KEY_UNTRANSFORMED_1: 'untransformed'})
		ud = UppercaseKeyDict({self.KEY_UNTRANSFORMED_1_2: 'untransformed2'})
		
		ld.update(ud)
		keys = set(ld)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "update with sibling class should preserve last key")
	
	def test_update_dict_transform_key(self):
		source_dict = {self.KEY_UNTRANSFORMED_1: 'untransformed'}
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			self.test_class(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d = self.test_class()
				
				d.update(d2)
				
				self.assertEqual(len(d), 1, "dict should have one key")
				self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
				self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
	
	def test_update_list_transform_key(self):
		source_list = [[self.KEY_UNTRANSFORMED_1, 'untransformed']]
		d = self.test_class()
		
		d.update(source_list)
		
		self.assertEqual(len(d), 1, "dict should have one key")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
		self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
	
	def test_update_kwargs_transform_key(self):
		source_kwargs = {self.KEY_UNTRANSFORMED_1: 'untransformed'}
		d = self.test_class()
		
		d.update(**source_kwargs)
		
		self.assertEqual(len(d), 1, "dict should have one key")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
		self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
	
	def test_update_dict_overwrite_transformed_by_untransformed(self):
		source_dict = {self.KEY_UNTRANSFORMED_1: 'dict'}
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			self.test_class(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d = self.test_class({self.KEY_TRANSFORMED_1: 'original'})
				
				d.update(d2)
				
				self.assertEqual(len(d), 1, "dict should have one key")
				self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
				self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
				self.assertEqual(d[self.KEY_TRANSFORMED_1], 'dict', "original key's value not overwritten by dict's untransformed key's value")
	
	def test_update_list_overwrite_transformed_by_untransformed(self):
		d = self.test_class({self.KEY_TRANSFORMED_1: 'original'})
		source_list = [[self.KEY_UNTRANSFORMED_1, 'list']]
		
		d.update(source_list)
		
		self.assertEqual(len(d), 1, "dict should have one key")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
		self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
		self.assertEqual(d[self.KEY_TRANSFORMED_1], 'list', "original key's value not overwritten by list's untransformed key's value")
	
	def test_update_kwargs_overwrite_transformed_by_untransformed(self):
		d = self.test_class({self.KEY_TRANSFORMED_1: 'original'})
		source_kwargs = {self.KEY_UNTRANSFORMED_1: 'kwargs'}
		
		d.update(**source_kwargs)
		
		self.assertEqual(len(d), 1, "dict should have one key")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
		self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
		self.assertEqual(d[self.KEY_TRANSFORMED_1], 'kwargs', "original key's value not overwritten by kwargs' untransformed key's value")

	def test_update_dict_preserve_first_key(self):
		source_dict = {self.KEY_UNTRANSFORMED_1_2: 'dict'}
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			self.test_class(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d = self.test_class({self.KEY_UNTRANSFORMED_1: 'original'})
				
				d.update(d2)
				keys = set(d)
				
				self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "update with dict should preserve first key")
	
	def test_update_dict_preserve_last_key(self):
		source_dict = {self.KEY_UNTRANSFORMED_1_2: 'dict'}
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			self.test_class(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d = self.test_class({self.KEY_UNTRANSFORMED_1: 'original'})
				
				d.update(d2)
				keys = set(d)
				
				self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "update with dict should preserve last key")
	
	def test_update_list_preserve_first_key(self):
		source_list = [[self.KEY_UNTRANSFORMED_1_2, 'list']]
		d = self.test_class({self.KEY_UNTRANSFORMED_1: 'original'})
		
		d.update(source_list)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "update with list should preserve first key")
	
	def test_update_list_preserve_last_key(self):
		source_list = [[self.KEY_UNTRANSFORMED_1_2, 'list']]
		d = self.test_class({self.KEY_UNTRANSFORMED_1: 'original'})
		
		d.update(source_list)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "update with list should preserve last key")
	
	def test_update_kwargs_preserve_first_key(self):
		source_kwargs = {self.KEY_UNTRANSFORMED_1_2: 'kwargs'}
		d = self.test_class({self.KEY_UNTRANSFORMED_1: 'original'})
		
		d.update(**source_kwargs)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "update with kwargs should preserve first key")
	
	def test_update_kwargs_preserve_last_key(self):
		source_kwargs = {self.KEY_UNTRANSFORMED_1_2: 'kwargs'}
		d = self.test_class({self.KEY_UNTRANSFORMED_1: 'original'})
		
		d.update(**source_kwargs)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "update with kwargs should preserve last key")
	
	def test_update_dict_add(self):
		source_dict   = {self.KEY_UNTRANSFORMED_1: 'dict'}
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			self.test_class(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):	
				d = self.test_class({self.KEY_UNTRANSFORMED_3: 'original'})
				
				d.update(d2)
				
				self.assertEqual(len(d), 2, "dict should have both keys")
				self.assertIn(self.KEY_UNTRANSFORMED_3, d, "untransformed original key not found")
				self.assertIn(self.KEY_TRANSFORMED_3, d,   "transformed original key not found")
				self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key from dict not found")
				self.assertIn(self.KEY_TRANSFORMED_1, d,   "transformed key from dict not found")
	
	def test_update_list_add(self):
		source_list   = [[self.KEY_UNTRANSFORMED_1, 'dict']]
		d = self.test_class({self.KEY_UNTRANSFORMED_3: 'original'})
		
		d.update(source_list)
		
		self.assertEqual(len(d), 2, "dict should have both keys")
		self.assertIn(self.KEY_UNTRANSFORMED_3, d, "untransformed original key not found")
		self.assertIn(self.KEY_TRANSFORMED_3, d,   "transformed original key not found")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key from list not found")
		self.assertIn(self.KEY_TRANSFORMED_1, d,   "transformed key from list not found")
	
	def test_update_kwargs_add(self):
		source_kwargs   = {self.KEY_UNTRANSFORMED_2: 'kwargs'}
		d = self.test_class({self.KEY_UNTRANSFORMED_3: 'original'})
		
		d.update(**source_kwargs)
		
		self.assertEqual(len(d), 2, "dict should have both keys")
		self.assertIn(self.KEY_UNTRANSFORMED_3, d, "untransformed original key not found")
		self.assertIn(self.KEY_TRANSFORMED_3, d,   "transformed original key not found")
		self.assertIn(self.KEY_UNTRANSFORMED_2, d, "untransformed key from kwargs not found")
		self.assertIn(self.KEY_TRANSFORMED_2, d,   "transformed key from kwargs not found")
	
	def test_update_dict_kwargs_add_both(self):
		source_dict   = {self.KEY_UNTRANSFORMED_1: 'dict'}
		source_kwargs = {self.KEY_UNTRANSFORMED_2: 'kwargs'}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			self.test_class(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d = self.test_class({self.KEY_UNTRANSFORMED_3: 'original'})
				
				d.update(d2, **source_kwargs)
				
				self.assertEqual(len(d), 3, "dict should have all three keys")
				self.assertIn(self.KEY_UNTRANSFORMED_3, d, "untransformed original key not found")
				self.assertIn(self.KEY_TRANSFORMED_3, d,   "transformed original key not found")
				self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key from dict not found")
				self.assertIn(self.KEY_TRANSFORMED_1, d,   "transformed key from dict not found")
				self.assertIn(self.KEY_UNTRANSFORMED_2, d, "untransformed key from kwargs not found")
				self.assertIn(self.KEY_TRANSFORMED_2, d,   "transformed key from kwargs not found")
	
	def test_update_list_kwargs_add_both(self):
		source_list   = [[self.KEY_UNTRANSFORMED_1, 'dict']]
		source_kwargs = {self.KEY_UNTRANSFORMED_2: 'kwargs'}
		d = self.test_class({self.KEY_UNTRANSFORMED_3: 'original'})
		
		d.update(source_list, **source_kwargs)
		
		self.assertEqual(len(d), 3, "dict should have all three keys")
		self.assertIn(self.KEY_UNTRANSFORMED_3, d, "untransformed original key not found")
		self.assertIn(self.KEY_TRANSFORMED_3, d,   "transformed original key not found")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key from list not found")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d,   "transformed key from list not found")
		self.assertIn(self.KEY_UNTRANSFORMED_2, d, "untransformed key from kwargs not found")
		self.assertIn(self.KEY_TRANSFORMED_2, d,   "transformed key from kwargs not found")
	
	def test_update_dict_kwargs_overwrite_untransformed_by_transformed(self):
		source_dict   = {self.KEY_UNTRANSFORMED_1: 'dict'}
		source_kwargs = {self.KEY_TRANSFORMED_1: 'kwargs'}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			self.test_class(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d = self.test_class()
				
				d.update(d2, **source_kwargs)
				
				self.assertEqual(len(d), 1, "dict should have one key")
				self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
				self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
				self.assertEqual(d[self.KEY_TRANSFORMED_1], 'kwargs', "dict's untransformed key's value not overwritten by kwargs' transformed key's value")
	
	def test_update_list_kwargs_overwrite_untransformed_by_transformed(self):
		source_list   = [[self.KEY_UNTRANSFORMED_1, 'list']]
		source_kwargs = {self.KEY_TRANSFORMED_1: 'kwargs'}
		d = self.test_class()
		
		d.update(source_list, **source_kwargs)
		
		self.assertEqual(len(d), 1, "dict should have one key")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
		self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
		self.assertEqual(d[self.KEY_TRANSFORMED_1], 'kwargs', "list's untransformed key's value not overwritten by kwargs' transformed key's value")
	
	def test_update_dict_kwargs_overwrite_transformed_by_untransformed(self):
		source_dict   = {self.KEY_TRANSFORMED_1: 'dict'}
		source_kwargs = {self.KEY_UNTRANSFORMED_1: 'kwargs'}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			self.test_class(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d = self.test_class()
				
				d.update(d2, **source_kwargs)
				
				self.assertEqual(len(d), 1, "dict should have one key")
				self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
				self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
				self.assertEqual(d[self.KEY_TRANSFORMED_1], 'kwargs', "dict's transformed key's value not overwritten by kwargs' untransformed key's value")
	
	def test_update_list_kwargs_overwrite_transformed_by_untransformed(self):
		source_list   = [[self.KEY_TRANSFORMED_1, 'list']]
		source_kwargs = {self.KEY_UNTRANSFORMED_1: 'kwargs'}
		d = self.test_class()
		
		d.update(source_list, **source_kwargs)
		
		self.assertEqual(len(d), 1, "dict should have one key")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
		self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
		self.assertEqual(d[self.KEY_TRANSFORMED_1], 'kwargs', "list's transformed key value not overwritten by kwargs' untransformed key's value")
	
	def test_update_dict_kwargs_preserve_dict_key(self):
		source_dict   = {self.KEY_UNTRANSFORMED_1: 'dict'}
		source_kwargs = {self.KEY_UNTRANSFORMED_1_2: 'kwargs'}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			self.test_class(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d = self.test_class()
				
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
			self.test_class(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d = self.test_class()
				
				d.update(d2, **source_kwargs)
				keys = set(d)
				
				self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "update with dict and kwargs should preserve kwargs key")
	
	def test_update_list_kwargs_preserve_list_key(self):
		source_list   = [[self.KEY_UNTRANSFORMED_1, 'list']]
		source_kwargs = {self.KEY_UNTRANSFORMED_1_2: 'kwargs'}
		d = self.test_class()
		
		d.update(source_list, **source_kwargs)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1}, "update with list and kwargs should preserve list key")
	
	def test_update_list_kwargs_preserve_kwargs_key(self):
		source_list   = [[self.KEY_UNTRANSFORMED_1, 'list']]
		source_kwargs = {self.KEY_UNTRANSFORMED_1_2: 'kwargs'}
		d = self.test_class()
		
		d.update(source_list, **source_kwargs)
		keys = set(d)
		
		self.assertEqual(keys, {self.KEY_UNTRANSFORMED_1_2}, "update with list and kwargs should preserve kwargs key")
	
	def test_len_overwrite_transformed_key_by_untransformed(self):
		d = self.test_class({self.KEY_TRANSFORMED_1: 1})
		
		d[self.KEY_UNTRANSFORMED_1] = 2
		
		self.assertEqual(len(d), 1, "adding the same key (up to transformation) should not increase length")
	
	def test_in(self):
		d = self.test_class({self.KEY_TRANSFORMED_1: 1})
		
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
		self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
		self.assertNotIn(self.KEY_TRANSFORMED_2, d, "non-existing key found")
	
	def test_getitem_present(self):
		d = self.test_class({self.KEY_TRANSFORMED_1: 1})
		
		d[self.KEY_TRANSFORMED_1]
		d[self.KEY_UNTRANSFORMED_1]
	
	def test_getitem_missing(self):
		d = self.test_class({self.KEY_TRANSFORMED_1: 1})
		
		with self.assertRaises(KeyError, msg="KeyError not raised for non-existing key"):
			d[self.KEY_TRANSFORMED_2]
	
	def test_get_present(self):
		d = self.test_class({self.KEY_TRANSFORMED_1: 1})
		
		self.assertEqual(d.get(self.KEY_TRANSFORMED_1),   1,   "transformed key not found")
		self.assertEqual(d.get(self.KEY_UNTRANSFORMED_1), 1, "untransformed key not found")
	
	def test_get_missing_default(self):
		d = self.test_class()
		
		self.assertEqual(d.get(self.KEY_TRANSFORMED_1), None, "non-existing key should return None")
	
	def test_get_missing_provided(self):
		d = self.test_class()
		
		self.assertEqual(d.get(self.KEY_TRANSFORMED_1, 2), 2, "non-existing key should return specified default value")
	
	def test_setitem_empty_untransformed(self):
		d = self.test_class()
		
		d[self.KEY_UNTRANSFORMED_1] = 1
		
		self.assertEqual(len(d), 1, "adding a new key should increase length")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
		self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
	
	def test_setitem_empty_transformed(self):
		d = self.test_class()
		
		d[self.KEY_TRANSFORMED_1] = 1
		
		self.assertEqual(len(d), 1, "adding a new key should increase length")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
		self.assertIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not found")
	
	def test_setitem_overwrite_transformed_by_untransformed(self):
		d = self.test_class({self.KEY_TRANSFORMED_1: 1})
		
		d[self.KEY_UNTRANSFORMED_1] = 2
		
		self.assertEqual(len(d), 1, "adding the same key (up to transformation) should not increase length")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found")
		self.assertIn(self.KEY_TRANSFORMED_1,   d, "transformed key not found")
	
	def test_delitem_untransformed_key(self):
		d = self.test_class({self.KEY_TRANSFORMED_1: 1})
		
		del d[self.KEY_UNTRANSFORMED_1]
		
		self.assertNotIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not deleted")
		self.assertNotIn(self.KEY_TRANSFORMED_1,   d,      "original key not deleted")
		self.assertEqual(len(d), 0, "non-empty dict after deleting the only untransformed key")
		
		
		with self.assertRaises(KeyError, msg="KeyError not raised for deleting non-existing original key"):
			del d[self.KEY_TRANSFORMED_1]
	
	def test_pop_untransformed_key(self):
		d = self.test_class({self.KEY_TRANSFORMED_1: 1})
		
		d.pop(self.KEY_UNTRANSFORMED_1)
		
		self.assertEqual(len(d), 0, "non-empty dict after popping the only transformed key")
		self.assertNotIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not popped")
		self.assertNotIn(self.KEY_TRANSFORMED_1,   d,   "transformed key not popped")
		
		with self.assertRaises(KeyError, msg="KeyError not raised for popping non-existing untransformed key"):
			d.pop(self.KEY_UNTRANSFORMED_1)
	
	def test_popitem(self):
		d = self.test_class({self.KEY_TRANSFORMED_1: 1})
		
		key, value = d.popitem()
		self.assertEqual(len(d), 0, "non-empty dict after popping the only item")
		self.assertEqual(key, self.KEY_TRANSFORMED_1, "transformed key not popped")
		self.assertNotEqual(key, self.KEY_UNTRANSFORMED_1, "untransformed key popped - popitem should return transformed key only")
	
	def test_setdefault_missing_transform_key(self):
		d = self.test_class()
		
		d.setdefault(self.KEY_UNTRANSFORMED_1, 1)
		
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found after setdefault")
		self.assertIn(self.KEY_TRANSFORMED_1, d, "transformed key not found after setdefault")
	
	def test_setdefault_present_set_untransformed_key(self):
		d = self.test_class({self.KEY_TRANSFORMED_1: 1})
		
		value = d.setdefault(self.KEY_UNTRANSFORMED_1, 2)
		
		self.assertEqual(value, 1, "present value not returned for untransformed key")
		self.assertIn(self.KEY_TRANSFORMED_1, d, "transformed key not found after setdefault")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d, "untransformed key not found after setdefault")
	
	def test_iter(self):
		source_keys = {self.KEY_UNTRANSFORMED_1, self.KEY_UNTRANSFORMED_2}
		d = self.test_class({key: 'value' for key in source_keys})
		
		keys = set(d)
		
		self.assertEqual(len(keys), 2, "iterating should yield all keys")
		self.assertEqual(keys, source_keys, "transformed key not found in iteration")
		self.assertIn(self.KEY_UNTRANSFORMED_1,    keys, "untransformed key not found in iteration - iter should return original keys only")
		self.assertIn(self.KEY_UNTRANSFORMED_2,  keys, "untransformed key not found in iteration - iter should return original keys only")
		self.assertNotIn(self.KEY_TRANSFORMED_1,   keys,   "transformed key found in iteration - iter should return original keys only")
		self.assertNotIn(self.KEY_TRANSFORMED_2, keys,   "transformed key found in iteration - iter should return original keys only")
	
	def test_keys(self):
		source_keys = {self.KEY_UNTRANSFORMED_1, self.KEY_UNTRANSFORMED_2}
		d = self.test_class({key: 'value' for key in source_keys})
		
		keys = d.keys()
		
		self.assertEqual(len(keys), 2, "keys view should yield all keys")
		self.assertIn(self.KEY_TRANSFORMED_1,   keys, "transformed key not found in keys view")
		self.assertIn(self.KEY_TRANSFORMED_2, keys, "transformed key not found in keys view")
		# KeysView supports key normalization
		self.assertIn(self.KEY_UNTRANSFORMED_1,   keys, "untransformed key not found in keys view")
		self.assertIn(self.KEY_UNTRANSFORMED_2, keys, "untransformed key not found in keys view")
	
	def test_items(self):
		d = self.test_class({self.KEY_TRANSFORMED_1: 1, self.KEY_TRANSFORMED_2: 2})
		
		items = d.items()
		
		self.assertEqual(len(items), 2, "items view should yield all items")
		self.assertIn((self.KEY_TRANSFORMED_1,   1), items, "transformed key-value pair not found in items view")
		self.assertIn((self.KEY_TRANSFORMED_2, 2), items, "transformed key-value pair not found in items view")
		# ItemsView supports key normalization
		self.assertIn((self.KEY_UNTRANSFORMED_1,   1), items, "untransformed key-value pair not found in items view")
		self.assertIn((self.KEY_UNTRANSFORMED_2, 2), items, "untransformed key-value pair not found in items view")
		
	def test_values(self):
		d = self.test_class({self.KEY_TRANSFORMED_1: 1, self.KEY_TRANSFORMED_2: 2})
		
		values = d.values()
		
		self.assertEqual(len(values), 2, "values view should yield all values")
	
	def test_copy_method(self):
		d = self.test_class({self.KEY_TRANSFORMED_1: 1, self.KEY_TRANSFORMED_2: 2})
		d_copy = d.copy()
		
		self.assertIsInstance(d_copy, self.test_class, f"result should be an instance of self.test_class, not {type(d_copy).__name__}")
		self.assertEqual(d_copy, d, "copy should be equal to original")
		self.assertIsNot(d_copy, d, "copy should not be the same object as original")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d_copy, "untransformed key not found in copy")
		self.assertIn(self.KEY_UNTRANSFORMED_2, d_copy, "untransformed key not found in copy")
		self.assertIn(self.KEY_TRANSFORMED_1, d_copy, "transformed key not found in copy")
		self.assertIn(self.KEY_TRANSFORMED_2, d_copy, "transformed key not found in copy")
	
	def test_copy(self):
		import copy
		
		d = self.test_class({self.KEY_TRANSFORMED_1: 1, self.KEY_TRANSFORMED_2: 2})
		d_copy = copy.copy(d)
		
		self.assertIsInstance(d_copy, self.test_class, f"result should be an instance of self.test_class, not {type(d_copy).__name__}")
		self.assertEqual(d_copy, d, "copy should be equal to original")
		self.assertIsNot(d_copy, d, "copy should not be the same object as original")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d_copy, "untransformed key not found in copy")
		self.assertIn(self.KEY_UNTRANSFORMED_2, d_copy, "untransformed key not found in copy")
		self.assertIn(self.KEY_TRANSFORMED_1, d_copy, "transformed key not found in copy")
		self.assertIn(self.KEY_TRANSFORMED_2, d_copy, "transformed key not found in copy")
	
	def test_deepcopy(self):
		import copy
		
		d = self.test_class({self.KEY_TRANSFORMED_1: 1, self.KEY_TRANSFORMED_2: 2})
		d_copy = copy.deepcopy(d)
		
		self.assertIsInstance(d_copy, self.test_class, f"result should be an instance of self.test_class, not {type(d_copy).__name__}")
		self.assertEqual(d_copy, d, "copy should be equal to original")
		self.assertIsNot(d_copy, d, "copy should not be the same object as original")
		self.assertIn(self.KEY_UNTRANSFORMED_1, d_copy, "untransformed key not found in copy")
		self.assertIn(self.KEY_UNTRANSFORMED_2, d_copy, "untransformed key not found in copy")
		self.assertIn(self.KEY_TRANSFORMED_1, d_copy, "transformed key not found in copy")
		self.assertIn(self.KEY_TRANSFORMED_2, d_copy, "transformed key not found in copy")
	
	def test_or_add_both(self):
		source_dict = {
			self.KEY_UNTRANSFORMED_2: 3,
			self.KEY_TRANSFORMED_2: 4,
		}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			self.test_class(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d1 = self.test_class({self.KEY_TRANSFORMED_1: 1})
				
				d3 = d1 | d2
				
				self.assertIsInstance(d3, self.test_class, f"result should be an instance of self.test_class, not {type(d3).__name__}")
				self.assertEqual(len(d3), 2, "dict should have both keys")
				self.assertIn(self.KEY_TRANSFORMED_1, d3, "untransformed key from dict 1 not found")
				self.assertIn(self.KEY_UNTRANSFORMED_1, d3, "transformed key from dict 1 not found")
				self.assertIn(self.KEY_TRANSFORMED_2, d3, "untransformed key from dict 2 not found")
				self.assertIn(self.KEY_UNTRANSFORMED_2, d3, "transformed key from dict 2 not found")
	
	def test_ror_add_both(self):
		source_dict = {
			self.KEY_UNTRANSFORMED_2: 3,
			self.KEY_TRANSFORMED_2: 4,
		}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			self.test_class(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d1 = self.test_class({self.KEY_TRANSFORMED_1: 1})
				
				d3 = d2 | d1
				
				self.assertIsInstance(d3, self.test_class, f"result should be an instance of self.test_class, not {type(d3).__name__}")
				self.assertEqual(len(d3), 2, f"dict should have both keys: {d3.keys()}")
				self.assertIn(self.KEY_TRANSFORMED_1, d3, "untransformed key from dict 1 not found")
				self.assertIn(self.KEY_UNTRANSFORMED_1, d3, "transformed key from dict 1 not found")
				self.assertIn(self.KEY_TRANSFORMED_2, d3, "untransformed key from dict 2 not found")
				self.assertIn(self.KEY_UNTRANSFORMED_2, d3, "transformed key from dict 2 not found")
	
	def test_ior_add_both(self):
		source_dict = {
			self.KEY_UNTRANSFORMED_2: 3,
			self.KEY_TRANSFORMED_2: 4,
		}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			self.test_class(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d1 = self.test_class({self.KEY_TRANSFORMED_1: 1})
				
				d1 |= d2
				
				self.assertIsInstance(d1, self.test_class, f"result should be an instance of self.test_class, not {type(d1).__name__}")
				self.assertEqual(len(d1), 2, f"dict should have both keys: {d1.keys()}")
				self.assertIn(self.KEY_TRANSFORMED_1, d1, "untransformed key from dict 1 not found")
				self.assertIn(self.KEY_UNTRANSFORMED_1, d1, "transformed key from dict 1 not found")
				self.assertIn(self.KEY_TRANSFORMED_2, d1, "untransformed key from dict 2 not found")
				self.assertIn(self.KEY_UNTRANSFORMED_2, d1, "transformed key from dict 2 not found")
	
	def test_or_overwrite(self):
		source_dict = {
			self.KEY_UNTRANSFORMED_1 : 2
		}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			self.test_class(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d1 = self.test_class({self.KEY_TRANSFORMED_1: 1})
				
				d3 = d1 | d2
				
				self.assertIsInstance(d3, self.test_class, f"result should be an instance of self.test_class, not {type(d3).__name__}")
				self.assertEqual(len(d3), 1, "dict should have one key")
				self.assertIn(self.KEY_TRANSFORMED_1, d3, "untransformed key not found")
				self.assertIn(self.KEY_UNTRANSFORMED_1, d3, "transformed keynot found")
				self.assertEqual(d3[self.KEY_UNTRANSFORMED_1], 2, "value of untransformed key not overwritten")
				self.assertEqual(d3[self.KEY_TRANSFORMED_1], 2, "value of transformed key not overwritten")
	
	def test_ror_overwrite(self):
		source_dict = {
			self.KEY_UNTRANSFORMED_1 : 2
		}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			self.test_class(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d1 = self.test_class({self.KEY_TRANSFORMED_1: 1})
				
				d3 = d2 | d1
				
				self.assertIsInstance(d3, self.test_class, f"result should be an instance of self.test_class, not {type(d3).__name__}")
				self.assertEqual(len(d3), 1, "dict should have one key")
				self.assertIn(self.KEY_TRANSFORMED_1, d3, "untransformed key not found")
				self.assertIn(self.KEY_UNTRANSFORMED_1, d3, "transformed keynot found")
				self.assertEqual(d3[self.KEY_UNTRANSFORMED_1], 1, "value of untransformed key not overwritten")
				self.assertEqual(d3[self.KEY_TRANSFORMED_1], 1, "value of transformed key not overwritten")
	
	def test_ior_overwrite(self):
		source_dict = {
			self.KEY_UNTRANSFORMED_1 : 2
		}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			self.test_class(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d1 = self.test_class({self.KEY_TRANSFORMED_1: 1})
				
				d1 |= d2
				
				self.assertIsInstance(d1, self.test_class, f"result should be an instance of self.test_class, not {type(d1).__name__}")
				self.assertEqual(len(d1), 1, "dict should have one key")
				self.assertIn(self.KEY_TRANSFORMED_1, d1, "untransformed key not found")
				self.assertIn(self.KEY_UNTRANSFORMED_1, d1, "transformed keynot found")
				self.assertEqual(d1[self.KEY_UNTRANSFORMED_1], 2, "value of untransformed key not overwritten")
				self.assertEqual(d1[self.KEY_TRANSFORMED_1], 2, "value of transformed key not overwritten")
	
	def test_ior_same_instance(self):
		source_dict = {}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			self.test_class(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d1 = self.test_class()
				
				d1_before = d1
				d1 |= d2
				
				self.assertIs(d1, d1_before, "result should be the same object")
	
	def test_eq_transformed(self):
		source_dict = {
			self.KEY_TRANSFORMED_1: 1,
		}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
			self.test_class(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d1 = self.test_class({self.KEY_TRANSFORMED_1: 1})
				
				self.assertEqual(d1, d2, "dicts with same keys and values should be equal")
	
	def test_eq_untransformed_other_class(self):
		source_dict = {
			self.KEY_UNTRANSFORMED_1: 1,
		}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d1 = self.test_class({self.KEY_TRANSFORMED_1: 1})
				
				self.assertNotEqual(d1, d2, "dicts with same keys (up to transformation) and values should not be equal unless the keys are exactly equal")

'''
class TestKeyTransformingDictBase(unittest.TestCase, KeyTransformingDictBaseTestMixin):
	test_class = TestKeyTransformingDict


if __name__ == '__main__':
	unittest.main()
'''