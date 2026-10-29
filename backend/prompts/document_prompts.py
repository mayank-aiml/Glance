from langchain_classic.prompts import PromptTemplate

# ============================================================
# MAP PROMPT
# Used to summarize each individual chunk
# ============================================================

chunk_prompt = """
Summarize this document section for later merging. Keep the main idea, key facts,
arguments, examples, and names, dates, numbers, technical terms.
Cut filler. Add nothing not in the text.

Section:
{text}

Summary:
"""

map_prompt_template = PromptTemplate(
    input_variables=["text"],
    template=chunk_prompt
)


final_prompt = """
Merge the summaries below into one self-contained summary with exactly these sections:

# Title
# Introduction
# Key Points (bullets)
# Detailed Summary (original logical flow)
# Important Facts (names, dates, numbers, statistics, examples, findings)
# Conclusion
# Key Takeaways (5-10 points)

Use only the input. No repetition. Don't mention chunks or "section summaries".
Don't fabricate where information is uncertain or incomplete.

Summaries:
{text}

Final Summary:
"""

final_prompt_template = PromptTemplate(
    input_variables=["text"],
    template=final_prompt
)

doc_quick_prompt = PromptTemplate(
    input_variables=["text"],
    template="""Merge the document summaries below into a concise Quick Summary:

# Executive Overview (2-3 sentences)
# Key Takeaways (5-7 clear bullets)
# Critical Finding

Summaries:
{text}

Quick Summary:
"""
)

doc_study_prompt = PromptTemplate(
    input_variables=["text"],
    template="""Transform the document summaries below into structured Study Notes:

# Document Topic & Objectives
# Key Terms & Formal Definitions
# Section Breakdown & In-Depth Concepts
# Critical Evidence, Data & Case Examples
# Self-Study / Comprehension Questions (5 questions with answers based strictly on text)

Summaries:
{text}

Study Notes:
"""
)

doc_executive_prompt = PromptTemplate(
    input_variables=["text"],
    template="""Synthesize the document summaries below into a high-level Executive Brief:

# Strategic Overview (Executive Summary)
# Major Findings & Core Arguments
# Crucial Metrics, Dates & Figures
# Action Items & Recommendations

Summaries:
{text}

Executive Brief:
"""
)

def get_document_combine_prompt(summary_type: str = "detailed") -> PromptTemplate:
    mapping = {
        "quick": doc_quick_prompt,
        "detailed": final_prompt_template,
        "study_notes": doc_study_prompt,
        "executive": doc_executive_prompt,
    }
    return mapping.get(summary_type, final_prompt_template)
