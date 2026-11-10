import json
import os

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

API_KEY = (
    os.getenv("GEM") or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
)

# Edit this list when Google renames models
MODELS = ["gemini-3.6-flash", "gemini-flash-latest"]
DEFAULT_SYSTEM_PROMPT = "You are a helpful, concise assistant."


def _to_text(content):
    """Gemini can return a string or a list of parts; always give back text."""
    if isinstance(content, str):
        return content
    parts = []
    for p in content:
        if isinstance(p, str):
            parts.append(p)
        elif isinstance(p, dict) and p.get("type") == "text":
            parts.append(p.get("text", ""))
    return "".join(parts)


def index(request):
    return render(request, "chat/index.html", {
        "models": MODELS,
        "default_system_prompt": DEFAULT_SYSTEM_PROMPT,
        "history": request.session.get("history", []),
        "has_key": bool(API_KEY),
    })


@require_POST
def chat_api(request):
    if not API_KEY:
        return JsonResponse({"error": "API key not found in .env"}, status=500)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    user_msg = (data.get("message") or "").strip()
    if not user_msg:
        return JsonResponse({"error": "Empty message"}, status=400)

    model = data.get("model") or MODELS[0]
    system_prompt = data.get("system_prompt") or DEFAULT_SYSTEM_PROMPT

    history = request.session.get("history", [])
    messages = [SystemMessage(content=system_prompt)]
    for m in history:
        cls = HumanMessage if m["role"] == "user" else AIMessage
        messages.append(cls(content=m["content"]))
    messages.append(HumanMessage(content=user_msg))

    try:
        llm = ChatGoogleGenerativeAI(model=model, google_api_key=API_KEY)
        reply = _to_text(llm.invoke(messages).content)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=502)

    history.append({"role": "user", "content": user_msg})
    history.append({"role": "assistant", "content": reply})
    request.session["history"] = history
    return JsonResponse({"reply": reply})


@require_POST
def clear_api(request):
    request.session["history"] = []
    return JsonResponse({"ok": True})