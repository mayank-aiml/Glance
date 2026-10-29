from .document_prompts import (
    chunk_prompt,
    map_prompt_template,
    final_prompt,
    final_prompt_template,
    get_document_combine_prompt,
)
from .youtube_prompts import (
    YT_MAP_PROMPT,
    YT_COMBINE_PROMPT,
    get_youtube_combine_prompt,
)
from .website_prompts import (
    WEB_MAP_PROMPT,
    WEB_COMBINE_PROMPT,
    get_website_combine_prompt,
)
from .text_prompts import (
    BASE_PROMPT,
    TEXT_PROMPT,
    TEXT_PROMPT_TEMPLATE,
    TEXT_MAP_PROMPT,
    TEXT_COMBINE_PROMPT,
    get_text_combine_prompt,
)

__all__ = [
    "chunk_prompt",
    "map_prompt_template",
    "final_prompt",
    "final_prompt_template",
    "get_document_combine_prompt",
    "YT_MAP_PROMPT",
    "YT_COMBINE_PROMPT",
    "get_youtube_combine_prompt",
    "WEB_MAP_PROMPT",
    "WEB_COMBINE_PROMPT",
    "get_website_combine_prompt",
    "BASE_PROMPT",
    "TEXT_PROMPT",
    "TEXT_PROMPT_TEMPLATE",
    "TEXT_MAP_PROMPT",
    "TEXT_COMBINE_PROMPT",
    "get_text_combine_prompt",
]
