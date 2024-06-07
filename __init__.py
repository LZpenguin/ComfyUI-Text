from .nodes import *

NODE_CLASS_MAPPINGS = {
    "Add_text_by_mask": AddTextByMask,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Add_text_by_mask": "Add Text By Mask",
}
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]