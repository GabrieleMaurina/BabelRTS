from babelrts.components.languages.javascript import Javascript
from babelrts.components.languages.extension_pattern_action import ExtensionPatternAction

class Typescript(Javascript):

    def get_extensions_patterns_actions(self):
        javascript_extensions_patterns_actions = super().get_extensions_patterns_actions()
        extensions_patterns_actions = set()
        for javascript_extension_pattern_action in javascript_extensions_patterns_actions:
            extensions_patterns_actions.add(ExtensionPatternAction('ts', javascript_extension_pattern_action.pattern, javascript_extension_pattern_action.action))
        return tuple(extensions_patterns_actions)
