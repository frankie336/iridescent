"""
c++ Key Words
"""
cpp_7keywords = ['do','else-if','if','else','switch','for','while']



cpp_keywords = ['alignas', 'alignof', 'and', 'and_eq', 'asm', 'auto',
                'bitand', 'bitor', 'bool', 'break', 'case', 'catch', 'char', 'char16_t', 'char32_t',
                'class', 'compl', 'const', 'constexpr', 'const_cast', 'continue', 'decltype', 'default',
                'delete', 'do', 'double', 'dynamic_cast', 'else', 'enum', 'explicit', 'export',
                'extern', 'FALSE', 'float', 'for', 'friend', 'goto', 'if', 'inline', 'int', 'long',
                'mutable', 'namespace', 'new', 'noexcept', 'not', 'not_eq', 'nullptr', 'operator', 'or',
                'or_eq', 'private', 'protected', 'public', 'register', 'reinterpret_cast', 'return',
                'short', 'signed', 'sizeof', 'static', 'static_assert', 'static_cast', 'struct',
                'switch', 'template', 'this', 'thread_local', 'throw', 'TRUE', 'try', 'typedef', 'typeid',
                'typename', 'union', 'unsigned', 'using', 'virtual', 'void', 'volatile', 'wchar_t', 'while',
                'xor', 'xor_eq', 'override', 'final']




"""
Base DF
"""
base_df_dict = {'user': '', 'WordUnigramTF':0, 'numTernary': 0, 'numTokens': 0,
                 'numComments': 0, 'numLiteral': 0, 'numKeywords': 0,'numFunctions': 0,
                'numMacros': 0, 'numFunctions':0, 'numMacros':0, 'nestingDepth':0,
                'branchingFactor':0, 'avgParams': 0,'stdDevNumParams':0,'avgLineLength':0,
                'stdDevLineLength':0,'numTabs':0,'numSpaces':0,'numEmptyLines':0,
                'whiteSpaceRatio': 0, 'newLineBeforeOpenBrace':0,'tabsLeadLines':0


                }