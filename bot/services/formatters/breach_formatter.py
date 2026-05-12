def format_breach_result(result):

    if not result["found"]:
        return "✅ Утечек не найдено."
    
    risk = result["risk"]
    risk_level = risk["level"].upper()

    message = (
        f"⚠️ Найдено утечек: {result['count']}\n"
        f"📊 Риск: {risk_level}\n\n"
    )
    
    reasons = risk.get("reasons", [])

    if reasons:
        message += "\n⚠️ Причины риска:\n"
        
        for reason in reasons:
            message += f"• {reason}\n"

    sources = result.get("sources", [])
    sources = sorted(
        sources,
        key=lambda x: x.get("date", ""),
        reverse=True
    )

    if sources:
        message += "\n📂 Источники:\n"

        for source in sources[:5]:
            name = source.get("name", "Unkown")
            date = source.get("date", "Uknown")

            if date.startswith("2025") or date.startswith("2026"):
                message += f"🚨 {name} ({date})\n"
            else:
                message += f"• {name} ({date})\n"

    fields = result.get("fields", [])

    if fields:
        message += "\n🔐 Скомпрометированные данные:\n"

        for field in fields[:5]:
            message += f"• {field}\n"

    return message