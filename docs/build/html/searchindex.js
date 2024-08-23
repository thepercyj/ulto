Search.setIndex({"alltitles": {"Contents": [[1, "contents"]], "Core Modules": [[0, null]], "Getting Started": [[1, "getting-started"]], "Key Features": [[1, "key-features"]], "Module contents": [[0, "module-src.core"]], "Modules": [[0, "modules"], [1, null]], "Ulto - An Imperative Reversible Programming Language documentation": [[1, null]], "core package": [[0, null]], "interpreter module": [[2, null]], "lazyeval module": [[3, null]], "lexer module": [[4, null]], "logstack module": [[5, null]], "malloc module": [[6, null]], "parser module": [[7, null]], "semantic_analyser module": [[8, null]], "src package": [[1, "module-src"]]}, "docnames": ["core", "index", "interpreter", "lazyeval", "lexer", "logstack", "malloc", "parser", "semantic_analyser"], "envversion": {"sphinx": 62, "sphinx.domains.c": 3, "sphinx.domains.changeset": 1, "sphinx.domains.citation": 1, "sphinx.domains.cpp": 9, "sphinx.domains.index": 1, "sphinx.domains.javascript": 3, "sphinx.domains.math": 2, "sphinx.domains.python": 4, "sphinx.domains.rst": 2, "sphinx.domains.std": 2}, "filenames": ["core.rst", "index.rst", "interpreter.rst", "lazyeval.rst", "lexer.rst", "logstack.rst", "malloc.rst", "parser.rst", "semantic_analyser.rst"], "indexentries": {"module": [[1, "module-src", false]], "src": [[1, "module-src", false]]}, "objects": {"": [[1, 0, 0, "-", "src"]], "src": [[0, 0, 0, "-", "core"], [2, 0, 0, "-", "interpreter"], [4, 0, 0, "-", "lexer"], [7, 0, 0, "-", "parser"], [8, 0, 0, "-", "semantic_analyser"]], "src.core": [[3, 0, 0, "-", "lazyeval"], [5, 0, 0, "-", "logstack"], [6, 0, 0, "-", "malloc"]], "src.core.lazyeval": [[3, 1, 1, "", "LazyEval"]], "src.core.lazyeval.LazyEval": [[3, 2, 1, "", "engine"], [3, 3, 1, "", "evaluate"], [3, 2, 1, "", "evaluated"], [3, 2, 1, "", "expression"], [3, 2, 1, "", "value"]], "src.core.logstack": [[5, 1, 1, "", "LogStack"]], "src.core.logstack.LogStack": [[5, 3, 1, "", "get_memory_usage"], [5, 2, 1, "", "last_pruned"], [5, 2, 1, "", "log"], [5, 3, 1, "", "peek"], [5, 3, 1, "", "pop"], [5, 3, 1, "", "prune"], [5, 3, 1, "", "push"]], "src.core.malloc": [[6, 1, 1, "", "MemoryManager"]], "src.core.malloc.MemoryManager": [[6, 3, 1, "", "allocate"], [6, 2, 1, "", "allocated_memory"], [6, 3, 1, "", "deallocate"], [6, 3, 1, "", "get_allocated_memory"], [6, 3, 1, "", "get_remaining_memory"], [6, 2, 1, "", "limit"]], "src.interpreter": [[2, 4, 1, "", "BreakException"], [2, 1, 1, "", "Interpreter"]], "src.interpreter.Interpreter": [[2, 1, 1, "", "Interpreter"], [2, 3, 1, "", "apply_operator"], [2, 3, 1, "", "collect_profiling_data"], [2, 3, 1, "", "detect_eager_vars"], [2, 3, 1, "", "error"], [2, 3, 1, "", "evaluate_expression"], [2, 3, 1, "", "execute"], [2, 3, 1, "", "execute_assignment"], [2, 3, 1, "", "execute_for"], [2, 3, 1, "", "execute_function"], [2, 3, 1, "", "execute_if"], [2, 3, 1, "", "execute_minus_assign"], [2, 3, 1, "", "execute_node"], [2, 3, 1, "", "execute_over_assign"], [2, 3, 1, "", "execute_plus_assign"], [2, 3, 1, "", "execute_print"], [2, 3, 1, "", "execute_reverse"], [2, 3, 1, "", "execute_revtrace"], [2, 3, 1, "", "execute_times_assign"], [2, 3, 1, "", "execute_while"], [2, 3, 1, "", "get_memory_usage"], [2, 3, 1, "", "get_previous_value"], [2, 3, 1, "", "log_execution_details"], [2, 3, 1, "", "print_computation_cost"], [2, 3, 1, "", "profile_assignment"], [2, 3, 1, "", "profile_if"], [2, 3, 1, "", "profile_node"], [2, 3, 1, "", "profile_print"], [2, 3, 1, "", "profile_reverse"], [2, 3, 1, "", "profile_revtrace"], [2, 3, 1, "", "profile_while"], [2, 3, 1, "", "prune_logstack"], [2, 3, 1, "", "update_profiling_data"]], "src.interpreter.Interpreter.Interpreter": [[2, 2, 1, "", "assignments"], [2, 2, 1, "", "ast"], [2, 2, 1, "", "current_step"], [2, 2, 1, "", "detailed_history"], [2, 2, 1, "", "eager_vars"], [2, 2, 1, "", "evaluations"], [2, 2, 1, "", "history"], [2, 2, 1, "", "lib"], [2, 2, 1, "", "logstack"], [2, 2, 1, "", "memory_manager"], [2, 2, 1, "", "profile_batch_size"], [2, 2, 1, "", "profile_counter"], [2, 2, 1, "", "profiling_data"], [2, 2, 1, "", "reversals"], [2, 2, 1, "", "symbol_table"]], "src.lexer": [[4, 5, 1, "", "tokenize"]], "src.parser": [[7, 1, 1, "", "Parser"]], "src.parser.Parser": [[7, 3, 1, "", "advance"], [7, 3, 1, "", "consume"], [7, 3, 1, "", "consume_value"], [7, 2, 1, "", "current_token"], [7, 3, 1, "", "error"], [7, 3, 1, "", "parse"], [7, 3, 1, "", "parse_assignment"], [7, 3, 1, "", "parse_block"], [7, 3, 1, "", "parse_break"], [7, 3, 1, "", "parse_expression"], [7, 3, 1, "", "parse_for"], [7, 3, 1, "", "parse_if"], [7, 3, 1, "", "parse_primary_expression"], [7, 3, 1, "", "parse_print"], [7, 3, 1, "", "parse_reverse"], [7, 3, 1, "", "parse_revtrace"], [7, 3, 1, "", "parse_statement"], [7, 3, 1, "", "parse_while"], [7, 3, 1, "", "peek_next_token"], [7, 2, 1, "", "pos"], [7, 2, 1, "", "tokens"]], "src.semantic_analyser": [[8, 1, 1, "", "SemanticAnalyser"]], "src.semantic_analyser.SemanticAnalyser": [[8, 3, 1, "", "analyse"], [8, 3, 1, "", "analyse_node"], [8, 2, 1, "", "ast"], [8, 3, 1, "", "error"], [8, 3, 1, "", "evaluate_expression"], [8, 3, 1, "", "evaluate_operation"], [8, 3, 1, "", "inline_expression"], [8, 3, 1, "", "is_inside_loop"], [8, 3, 1, "", "process_assignment"], [8, 3, 1, "", "process_break"], [8, 3, 1, "", "process_for"], [8, 3, 1, "", "process_if"], [8, 3, 1, "", "process_len"], [8, 3, 1, "", "process_minus_assign"], [8, 3, 1, "", "process_over_assign"], [8, 3, 1, "", "process_plus_assign"], [8, 3, 1, "", "process_print"], [8, 3, 1, "", "process_reverse"], [8, 3, 1, "", "process_revtrace"], [8, 3, 1, "", "process_times_assign"], [8, 3, 1, "", "process_while"], [8, 2, 1, "", "symbol_table"]]}, "objnames": {"0": ["py", "module", "Python module"], "1": ["py", "class", "Python class"], "2": ["py", "attribute", "Python attribute"], "3": ["py", "method", "Python method"], "4": ["py", "exception", "Python exception"], "5": ["py", "function", "Python function"]}, "objtypes": {"0": "py:module", "1": "py:class", "2": "py:attribute", "3": "py:method", "4": "py:exception", "5": "py:function"}, "terms": {"": [1, 7, 8], "000": 5, "1": 5, "2": 5, "50": 5, "50000": 5, "A": [2, 3, 4, 5, 6, 7, 8], "For": 2, "If": [2, 5, 6], "In": 1, "It": [1, 2, 5, 6, 7, 8], "The": [2, 3, 4, 5, 6, 7, 8], "To": 1, "_": 2, "about": 1, "abstract": [2, 7, 8], "access": 3, "accord": 7, "action": 1, "actual": 3, "ad": 2, "addition": 2, "advanc": [1, 7], "ag": 5, "alloc": [2, 6], "allocated_memori": 6, "allow": [1, 5, 6], "along": 5, "also": [1, 2, 6], "amount": 6, "an": [2, 3, 5, 7, 8], "analys": 8, "analyse_nod": 8, "analysi": [1, 8], "analyz": [1, 7, 8], "ani": [2, 3, 5, 8], "appli": 2, "applic": 1, "apply_oper": 2, "approach": 1, "ar": [1, 3, 5, 8], "arg": [2, 4, 6, 7, 8], "arithmet": [2, 8], "assign": [2, 7, 8], "associ": 2, "ast": [2, 7, 8], "avail": [5, 6], "back": 5, "backtrack": [], "base": [1, 2, 3, 5, 6, 7, 8], "batch": 2, "been": 3, "befor": 8, "being": [5, 7], "between": 1, "block": 7, "bool": [3, 8], "both": [], "branch": 7, "break": [7, 8], "breakexcept": [1, 2], "byte": 6, "c": [1, 2], "cach": 3, "calcul": 5, "can": [1, 3], "cdll": 2, "certain": 3, "chang": [1, 5], "check": 8, "choos": 1, "class": [2, 3, 5, 6, 7, 8], "code": 4, "collect": 2, "collect_profiling_data": 2, "compil": 1, "complex": 1, "compon": 1, "compound": 2, "comput": [1, 2, 5], "condit": [2, 3, 7, 8], "consum": 7, "consume_valu": 7, "contain": 2, "context": 8, "control": [2, 8], "convert": 7, "core": [1, 3, 5, 6], "correct": [1, 8], "correspond": 5, "cost": 2, "counter": 2, "creat": 5, "ctype": 2, "current": [2, 5, 6, 7, 8], "current_step": 2, "current_token": 7, "data": [1, 2], "dealloc": 6, "debug": 1, "declar": 8, "default": 5, "defer": 3, "delai": 1, "design": [1, 5], "destruct": 1, "detail": [1, 2], "detailed_histori": 2, "detect": 2, "detect_eager_var": 2, "develop": 1, "dict": [2, 5, 8], "dictionari": [2, 5], "differ": 1, "divid": 2, "divis": 2, "doe": [5, 6], "dure": 8, "e": 2, "each": 1, "eager": [1, 2], "eager_var": 2, "easi": 1, "easier": 1, "effect": 1, "effici": 1, "empti": 5, "enabl": 1, "end": 2, "end_tim": 2, "energi": 1, "enforc": 8, "engin": 3, "enough": 5, "ensur": [1, 3, 6, 7, 8], "entri": 5, "environ": 1, "error": [1, 2, 7, 8], "especi": 1, "etc": 5, "evalu": [1, 2, 3, 8], "evaluate_express": [2, 8], "evaluate_oper": 8, "even": 1, "exce": 6, "except": [2, 7], "execut": 2, "execute_assign": 2, "execute_for": 2, "execute_funct": 2, "execute_if": 2, "execute_minus_assign": 2, "execute_nod": 2, "execute_over_assign": 2, "execute_plus_assign": 2, "execute_print": 2, "execute_revers": 2, "execute_revtrac": 2, "execute_times_assign": 2, "execute_whil": 2, "executionengin": 3, "exist": 5, "expect": [2, 7], "expens": 3, "explor": 1, "expr": [2, 8], "express": [2, 3, 7, 8], "extrem": 1, "fals": [3, 8], "familiar": 1, "far": 5, "ffi": 2, "file": [1, 2], "find": 1, "flag": 3, "flexibl": 1, "float": [2, 5], "flow": 2, "foreign": 2, "format": 2, "forward": 1, "found": 2, "from": [1, 2, 5], "function": [2, 8], "g": 2, "gener": 7, "get": 2, "get_allocated_memori": 6, "get_memory_usag": [2, 5], "get_previous_valu": 2, "get_remaining_memori": 6, "given": [1, 2, 4, 5, 6, 8], "grammar": 7, "ha": [3, 5], "handl": [1, 2], "hasn": 3, "have": 5, "help": 1, "high": 1, "histori": [2, 5], "how": [1, 5], "hybrid": 1, "hyrbid": 1, "i": [1, 2, 3, 5, 7, 8], "identifi": [2, 7], "immedi": 1, "includ": [1, 5, 8], "index": [2, 5], "indic": [3, 7], "inform": 1, "initi": 3, "inlin": 8, "inline_express": 8, "input": 7, "insid": 8, "instanc": 2, "instruct": 1, "int": [2, 5, 6, 7, 8], "interfac": 2, "interpret": 1, "irrevers": 1, "is_inside_loop": 8, "its": 3, "just": 1, "keep": [1, 2, 5], "kei": 5, "kept": 1, "keyerror": 2, "languag": [2, 7, 8], "last": 5, "last_prun": 5, "lazi": [1, 3], "lazili": 3, "lazyev": 0, "learn": 1, "left": [2, 8], "len": 8, "let": 1, "level": 1, "lexer": 1, "lexic": 7, "lib": 2, "librari": 2, "like": [1, 5], "limit": 6, "limit_mb": 6, "list": [2, 4, 5, 7, 8], "ll": 1, "load": 2, "log": [1, 2, 5], "log_execution_detail": 2, "logstack": [0, 1, 2], "long": 1, "look": 5, "loop": [2, 7, 8], "made": 5, "main": 1, "make": 1, "malloc": 0, "manag": [1, 2, 5, 6], "match": 7, "maximum": 5, "mb": 5, "megabyt": [2, 5], "memori": [1, 2, 5, 6], "memory_manag": 2, "memoryerror": 6, "memorymanag": [0, 2, 6], "messag": [2, 8], "met": 3, "method": [5, 6], "might": 3, "minu": 2, "mistak": [], "monitor": 1, "more": [1, 7], "most": [1, 5], "motiv": 1, "multipli": 2, "name": [2, 5], "need": [1, 3, 8], "new": [1, 5], "next": 7, "node": [2, 7, 8], "none": [2, 3, 5, 7], "now": 2, "number": [2, 7], "object": [2, 3, 5, 6, 7, 8], "offer": 1, "old": [1, 5], "old_valu": 5, "older": 5, "onc": 3, "onli": [3, 5], "onto": 5, "op": [2, 8], "oper": [1, 2, 5, 8], "operand": [2, 8], "optim": [1, 2], "optimis": 1, "option": 5, "otherwis": 8, "out": 5, "outcom": 1, "over": 5, "paramet": [2, 5], "parenthes": 7, "pars": 7, "parse_assign": 7, "parse_block": 7, "parse_break": 7, "parse_express": 7, "parse_for": 7, "parse_if": 7, "parse_primary_express": 7, "parse_print": 7, "parse_revers": 7, "parse_revtrac": 7, "parse_stat": 7, "parse_whil": 7, "parser": 1, "pass": 5, "peek": [5, 7], "peek_next_token": 7, "perform": [1, 2, 5, 8], "plu": 2, "po": 7, "pop": 5, "posit": [5, 7], "power": 1, "precompil": 1, "predefin": 6, "previou": [2, 5], "primari": 7, "print": [2, 7, 8], "print_computation_cost": 2, "process": [1, 7, 8], "process_assign": 8, "process_break": 8, "process_for": 8, "process_if": 8, "process_len": 8, "process_minus_assign": 8, "process_over_assign": 8, "process_plus_assign": 8, "process_print": 8, "process_revers": 8, "process_revtrac": 8, "process_times_assign": 8, "process_whil": 8, "profil": [1, 2], "profile_assign": 2, "profile_batch_s": 2, "profile_count": 2, "profile_if": 2, "profile_nod": 2, "profile_print": 2, "profile_revers": 2, "profile_revtrac": 2, "profile_whil": 2, "profiling_data": 2, "program": [2, 6, 7, 8], "provid": [1, 6], "prune": [1, 5], "prune_logstack": 2, "push": 5, "python": 1, "queri": 6, "rais": [2, 6, 7, 8], "rang": 5, "re": 1, "recent": 5, "remain": [1, 6], "remov": [1, 5], "repres": [2, 7], "requir": 3, "resourc": 1, "respons": [2, 7, 8], "result": [1, 2, 3, 8], "retain": 5, "retent": 5, "retention_tim": 5, "retriev": 2, "return": [2, 3, 4, 5, 6, 7, 8], "revers": [2, 7, 8], "revtrac": [2, 7, 8], "right": [2, 8], "rule": 8, "run": 1, "runtim": 1, "same": 1, "scenario": 3, "scientif": 1, "second": 5, "semant": [1, 8], "semantic_analys": 1, "semanticanalys": [1, 8], "sequenc": 1, "set": 2, "simpl": 8, "sinc": 5, "singl": [2, 7, 8], "situat": 1, "size": [2, 6], "sort": 2, "sorteddict": 2, "sourc": 4, "specif": 5, "specifi": [5, 6], "src": [2, 3, 4, 5, 6, 7, 8], "stack": [2, 5], "start": 2, "start_tim": 2, "state": [1, 2], "statement": [7, 8], "step": [1, 2], "store": [2, 5], "str": [2, 4, 5, 7, 8], "string": 7, "structur": [7, 8], "style": 1, "subsequ": 3, "subtract": 2, "support": [1, 5, 7], "symbol": [2, 8], "symbol_t": [2, 8], "syntax": [2, 7, 8], "t": 3, "tabl": [2, 8], "task": 1, "than": 5, "thi": [1, 3, 5, 8], "through": [1, 2], "time": [2, 5], "timestamp": 5, "token": [1, 4, 7], "token_typ": 7, "tool": 1, "total": [5, 6], "track": [1, 2, 5, 6, 8], "tradit": 1, "tree": [2, 7, 8], "true": 8, "tupl": [2, 5, 7, 8], "two": 2, "type": [2, 3, 5, 6, 7, 8], "typic": 1, "ulto": [2, 7, 8], "undo": [1, 5], "uniqu": [], "unix": 5, "unless": 3, "unlik": 1, "unnecessari": 1, "until": [1, 3], "updat": 2, "update_profiling_data": 2, "us": [1, 2, 3, 5, 8], "usag": [1, 2, 5], "valid": [7, 8], "valu": [2, 3, 5, 7, 8], "var_nam": [2, 5], "variabl": [1, 2, 5, 8], "variou": [7, 8], "via": 1, "view": 5, "wa": [1, 5], "wai": 1, "well": 1, "when": 1, "where": [1, 3, 5], "whether": [1, 3], "which": 1, "while": [1, 2, 7, 8], "who": 1, "whose": 5, "within": [6, 8], "without": [5, 7], "would": 8, "written": 1, "yet": 3, "you": [1, 5], "your": 1}, "titles": ["core package", "Ulto - An Imperative Reversible Programming Language documentation", "interpreter module", "lazyeval module", "lexer module", "logstack module", "malloc module", "parser module", "semantic_analyser module"], "titleterms": {"an": 1, "content": [0, 1], "core": 0, "document": 1, "featur": 1, "get": 1, "imper": 1, "interpret": 2, "kei": 1, "languag": 1, "lazyev": 3, "lexer": 4, "logstack": 5, "malloc": 6, "modul": [0, 1, 2, 3, 4, 5, 6, 7, 8], "packag": [0, 1], "parser": 7, "program": 1, "revers": 1, "semantic_analys": 8, "src": 1, "start": 1, "ulto": 1}})