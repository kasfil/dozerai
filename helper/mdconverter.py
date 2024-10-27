from telegramify_markdown import customize, markdownify


def to_telemd(text: str) -> str:
    customize.markdown_symbol.head_level_1 = "📌"
    customize.markdown_symbol.head_level_2 = "🏷️"
    customize.markdown_symbol.task_completed = "✅"
    customize.markdown_symbol.task_uncompleted = "⬜"
    customize.markdown_symbol.link = "🔗"

    return markdownify(text)
