from .prompt import PROMPTS, GRAPH_FIELD_SEP

class PromptManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PromptManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):  # 防止多次初始化
            self.prompts = PROMPTS
            self.graph_field_sep = GRAPH_FIELD_SEP
            self.initialized = True

    def get_prompts(self):
        return self.prompts

    def get_graph_field_sep(self):
        return self.graph_field_sep

    def set_prompts(self, new_prompts):
        self.prompts = new_prompts
        return self

    def set_graph_field_sep(self, new_sep):
        self.graph_field_sep = new_sep
        return self