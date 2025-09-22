from fastapi import APIRouter, HTTPException
from app.api.dependencies import AppDepends
from app.utils.helpers import current_utc_time, new_uuid
from app.core.generator import generator
from app.models.api_models import GenerateRequest, GenerateResponse

router = APIRouter()


@router.post(path="/generate-section")
def generate_section(
    request: GenerateRequest, retriever=None, history_store=None
):
    """
    Generates a section of a grant application using context from the
    knowledge base.
    """
    app_depends = AppDepends()

    if retriever is None:
        retriever = app_depends.get_retriever()

    if history_store is None:
        history_store = app_depends.get_history_storage()

    results = retriever.search(request.text, company_id=request.company_id)
    if not results:
        raise HTTPException(
            status_code=404, detail="No documents found in knowledge base."
        )

    contexts = []
    for result in results:
        doc, score = result
        contexts.append(doc)

    generated_text = generator(request.text, contexts)

    response = GenerateResponse(
        company_id=request.company_id,
        section_type=request.section_type,
        generated_text=generated_text,
        sources=[doc.id for doc in contexts],
        request_id=new_uuid(),
        created_at=current_utc_time(),
    )

    history_store.add(
        company_id=request.company_id,
        section_type=request.section_type,
        request_id=response.request_id,
    )

    return response


@router.get(path="/history/{company_id}")
def get_history(company_id, history_store=None):
    """
    Returns the history of generated sections for a given company.
    """
    app_depends = AppDepends()

    if history_store is None:
        history_store = app_depends.get_history_storage()

    entries = history_store.list_for_company(company_id)
    if not entries:
        raise HTTPException(
            status_code=404, detail="No history found for this company."
        )
    return entries
