"""
SkCode text modifier tags test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags.textmodifiers import TextModifierBaseTagOptions
from skcode.tags import (RootTagOptions,
                         LowerCaseTextTagOptions,
                         UpperCaseTextTagOptions,
                         CapitalizeTextTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)


class TextModifierTagsTestCase(unittest.TestCase):
    """ Tests suite for text modifier tags module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('lowercase', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['lowercase'], LowerCaseTextTagOptions)
        self.assertIn('uppercase', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['uppercase'], UpperCaseTextTagOptions)
        self.assertIn('capitalize', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['capitalize'], CapitalizeTextTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = TextModifierBaseTagOptions('lowercase')
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertTrue(opts.inline)
        self.assertFalse(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)

    def test_render_html_lowercase(self):
        """ Test the ``render_html`` method. """
        opts = LowerCaseTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('lowercase', opts)
        self.assertEqual('<span class="text-lowercase">test</span>\n', opts.render_html(tree_node, 'test'))

    def test_render_html_uppercase(self):
        """ Test the ``render_html`` method. """
        opts = UpperCaseTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('uppercase', opts)
        self.assertEqual('<span class="text-uppercase">test</span>\n', opts.render_html(tree_node, 'test'))

    def test_render_html_capitalize(self):
        """ Test the ``render_html`` method. """
        opts = CapitalizeTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('capitalize', opts)
        self.assertEqual('<span class="text-capitalize">test</span>\n', opts.render_html(tree_node, 'test'))

    def test_render_text_lowercase(self):
        """ Test the ``render_text`` method. """
        opts = LowerCaseTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('lowercase', opts)
        self.assertEqual('test', opts.render_text(tree_node, 'teST'))

    def test_render_text_uppercase(self):
        """ Test the ``render_text`` method. """
        opts = UpperCaseTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('uppercase', opts)
        self.assertEqual('TEST', opts.render_text(tree_node, 'teST'))

    def test_render_text_capitalize(self):
        """ Test the ``render_text`` method. """
        opts = CapitalizeTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('capitalize', opts)
        self.assertEqual('Test', opts.render_text(tree_node, 'test'))

    def test_render_text_unknown_modifier(self):
        """ Test the ``render_text`` method. """
        opts = TextModifierBaseTagOptions('unknown')
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('unknown', opts)
        self.assertEqual('teST', opts.render_text(tree_node, 'teST'))
