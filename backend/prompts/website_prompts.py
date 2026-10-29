from langchain_classic.prompts import PromptTemplate

WEB_MAP_PROMPT = """
Summarize ONLY this webpage section for later merging. Keep main ideas, facts,
arguments, examples, statistics, dates, conclusions.
Ignore navigation, ads, cookie notices, footers, social widgets, unrelated links.
Cut repetition. Add nothing not in the content.

Webpage Section:
{text}

Summary:
"""

WEB_MAP_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["text"],
    template=WEB_MAP_PROMPT
)


WEB_COMBINE_PROMPT = """
Merge the webpage-section summaries below into one accurate summary with exactly these sections:

# Title
# Introduction
# Main Points
# Detailed Summary
# Important Facts (names, dates, numbers, statistics, examples, findings)
# Main Arguments
# Conclusion
# Key Takeaways (5-10 points)

Don't invent or repeat information. Don't mention chunks or section summaries.
Distinguish facts from opinions. Keep source uncertainty. Exclude page boilerplate.

SUMMARIES:
{text}

FINAL SUMMARY:
"""

WEB_COMBINE_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["text"],
    template=WEB_COMBINE_PROMPT
)

WEB_QUICK_COMBINE_PROMPT = PromptTemplate(
    input_variables=["text"],
    template="""Merge the webpage summaries below into a crisp Quick Summary:

# Overview (2-3 sentences)
# Key Takeaways (5-7 clear bullets)
# Bottom Line

SUMMARIES:
{text}

QUICK SUMMARY:
"""
)

WEB_STUDY_COMBINE_PROMPT = PromptTemplate(
    input_variables=["text"],
    template="""Transform the webpage summaries below into structured Study Notes:

# Topic & Context
# Fundamental Concepts & Definitions
# Comprehensive Breakdown of Points
# Case Evidence & Key Statistics
# Review Questions & Answers (5 questions with answers)

SUMMARIES:
{text}

STUDY NOTES:
"""
)

WEB_EXECUTIVE_COMBINE_PROMPT = PromptTemplate(
    input_variables=["text"],
    template="""Synthesize the webpage summaries below into an Executive Brief:

# Executive Brief (Overview of article/site)
# Strategic Insights & Business/Industry Impact
# Key Numbers, Dates & Quotes
# Recommendations / Key Actions

SUMMARIES:
{text}

EXECUTIVE BRIEF:
"""
)

def get_website_combine_prompt(summary_type: str = "detailed") -> PromptTemplate:
    mapping = {
        "quick": WEB_QUICK_COMBINE_PROMPT,
        "detailed": WEB_COMBINE_PROMPT_TEMPLATE,
        "study_notes": WEB_STUDY_COMBINE_PROMPT,
        "executive": WEB_EXECUTIVE_COMBINE_PROMPT,
    }
    return mapping.get(summary_type, WEB_COMBINE_PROMPT_TEMPLATE)
