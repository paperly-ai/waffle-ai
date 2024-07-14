from fastapi import APIRouter, HTTPException
from app.core.pinecone import init_pinecone
from app.services.document_processor import DocumentProcessor
from app.schemas import schema

router = APIRouter()

@router.post("/upsert_pdf")
async def upsert_pdf(request: schema.UpsertPDFRequest):
    processor=DocumentProcessor()
    vector = processor.embed_text(request.documet_url)
    vectors=vector[0]
    dimension=len(vectors)
    pinecone_index = init_pinecone(dimensions=dimension)
    pinecone_index.upsert([(f"{request.user_id}-{request.document_id}", vectors)])
    return {"message": "PDF vector upserted successfully"}
