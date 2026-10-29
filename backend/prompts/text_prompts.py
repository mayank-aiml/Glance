from langchain_classic.prompts import PromptTemplate

BASE_PROMPT = """
Summarize accurately and concisely. Keep the original meaning and any stated
uncertainty. Add nothing not in the source. Cut repetition and filler.
"""

TEXT_PROMPT = BASE_PROMPT + """
Output: 1. TL;DR (2-4 sentences) 2. Main Points 3. Important Details
4. Conclusion 5. Key Takeaways (5-10 points). Scale detail to input length.

TEXT:
{text}
"""

TEXT_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["text"],
    template=TEXT_PROMPT
)


TEXT_MAP_PROMPT = """
Summarize ONLY this text section for later merging. Keep main ideas, key facts,
arguments, names, dates, numbers. Cut filler and repetition. Add nothing not in the text.

Section:
{text}

Summary:
"""

TEXT_MAP_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["text"],
    template=TEXT_MAP_PROMPT
)


TEXT_COMBINE_PROMPT = """
Merge the text section summaries below into one cohesive, accurate summary with exactly these sections:

# Title
# TL;DR (2-4 sentences)
# Key Points (bullets)
# Detailed Summary
# Important Facts (names, dates, numbers, statistics, examples)
# Conclusion
# Key Takeaways (5-10 points)

Don't invent or repeat information. Don't mention chunks or section summaries.

SUMMARIES:
{text}

FINAL SUMMARY:
"""

TEXT_COMBINE_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["text"],
    template=TEXT_COMBINE_PROMPT
)

TEXT_QUICK_COMBINE_PROMPT = PromptTemplate(
    input_variables=["text"],
    template="""Merge the text section summaries below into a crisp Quick Summary:

# Overview (2-3 sentences)
# Key Takeaways (5-7 clear bullets)
# Core Highlight

SUMMARIES:
{text}

QUICK SUMMARY:
"""
)

TEXT_STUDY_COMBINE_PROMPT = PromptTemplate(
    input_variables=["text"],
    template="""Transform the text section summaries below into structured Study Notes:

# Topic & Objectives
# Key Concepts & Definitions
# Section Breakdown & In-Depth Insights
# Important Facts & Examples
# Review Questions & Answers (5 questions with answers)

SUMMARIES:
{text}

STUDY NOTES:
"""
)

TEXT_EXECUTIVE_COMBINE_PROMPT = PromptTemplate(
    input_variables=["text"],
    template="""Synthesize the text section summaries below into an Executive Brief:

# Executive Brief (Concise 2-3 sentence overview)
# Major Findings & Core Arguments
# Key Metrics, Dates & Figures
# Action Items & Practical Recommendations

SUMMARIES:
{text}

EXECUTIVE BRIEF:
"""
)

def get_text_combine_prompt(summary_type: str = "detailed") -> PromptTemplate:
    mapping = {
        "quick": TEXT_QUICK_COMBINE_PROMPT,
        "detailed": TEXT_COMBINE_PROMPT_TEMPLATE,
        "study_notes": TEXT_STUDY_COMBINE_PROMPT,
        "executive": TEXT_EXECUTIVE_COMBINE_PROMPT,
    }
    return mapping.get(summary_type, TEXT_COMBINE_PROMPT_TEMPLATE)
