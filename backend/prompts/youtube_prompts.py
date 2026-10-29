from langchain_classic.prompts import PromptTemplate

YOUTUBE_MAP_PROMPT = """
Summarize ONLY this transcript section for later merging. Keep main ideas, facts,
explanations, examples, arguments, technical concepts, names, numbers.
Cut filler and repetition. Don't invent or drop important information.

Transcript Section:
{text}

Summary:
"""

YT_MAP_PROMPT = PromptTemplate(
    input_variables=["text"],
    template=YOUTUBE_MAP_PROMPT
)

YOUTUBE_MAP_PROMPT_TEMPLATE = YT_MAP_PROMPT


YOUTUBE_COMBINE_PROMPT = """
Merge the video-section summaries below into one accurate summary with exactly these sections:

# Title
# Introduction
# Main Topics
# Detailed Summary (logical narrative, keep order where it matters)
# Important Insights
# Important Examples
# Important Facts (names, numbers, statistics, technical terms)
# Conclusion
# Key Takeaways (5-10 points)

Don't invent or repeat information. Don't mention chunks or "section summaries".
If summaries conflict, don't guess.

SUMMARIES:
{text}

FINAL SUMMARY:
"""

YT_COMBINE_PROMPT = PromptTemplate(
    input_variables=["text"],
    template=YOUTUBE_COMBINE_PROMPT
)

YOUTUBE_COMBINE_PROMPT_TEMPLATE = YT_COMBINE_PROMPT

YT_QUICK_COMBINE_PROMPT = PromptTemplate(
    input_variables=["text"],
    template="""Merge the video-section summaries below into a concise Quick Summary:

# Overview (2-3 sentences capturing the core message)
# Key Takeaways (5-7 high-impact bullet points)
# Standout Insight

SUMMARIES:
{text}

QUICK SUMMARY:
"""
)

YT_STUDY_COMBINE_PROMPT = PromptTemplate(
    input_variables=["text"],
    template="""Transform the video-section summaries below into structured Study Notes:

# Subject Overview
# Core Concepts & Definitions
# Topic-by-Topic Breakdown
# Key Examples & Data Points
# Review Questions & Answers (5 key revision questions with brief answers)

SUMMARIES:
{text}

STUDY NOTES:
"""
)

YT_EXECUTIVE_COMBINE_PROMPT = PromptTemplate(
    input_variables=["text"],
    template="""Synthesize the video-section summaries below into an Executive Brief for decision-makers:

# Executive Brief (Concise high-level summary)
# Strategic Insights & Major Findings
# Key Metrics, Data & Timeline
# Action Items & Practical Implications

SUMMARIES:
{text}

EXECUTIVE BRIEF:
"""
)

def get_youtube_combine_prompt(summary_type: str = "detailed") -> PromptTemplate:
    mapping = {
        "quick": YT_QUICK_COMBINE_PROMPT,
        "detailed": YT_COMBINE_PROMPT,
        "study_notes": YT_STUDY_COMBINE_PROMPT,
        "executive": YT_EXECUTIVE_COMBINE_PROMPT,
    }
    return mapping.get(summary_type, YT_COMBINE_PROMPT)
