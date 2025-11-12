import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import db, create_document, get_documents

app = FastAPI(title="Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ContactPayload(BaseModel):
    name: str
    email: str
    subject: Optional[str] = None
    message: str


@app.get("/")
def read_root():
    return {"message": "Portfolio Backend Running"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = getattr(db, 'name', None) or "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response


# Projects Endpoints
@app.get("/api/projects")
def list_projects(category: Optional[str] = None):
    filt = {"category": category} if category else {}
    items = get_documents("project", filt) if db else []
    # Sort by year desc if present
    if items:
        try:
            items.sort(key=lambda x: x.get("year", 0), reverse=True)
        except Exception:
            pass
    # Map _id to string
    for it in items:
        if "_id" in it:
            it["id"] = str(it.pop("_id"))
    return {"projects": items}


@app.get("/api/projects/{slug}")
def get_project(slug: str):
    items = get_documents("project", {"slug": slug}, limit=1) if db else []
    if not items:
        raise HTTPException(status_code=404, detail="Project not found")
    it = items[0]
    if "_id" in it:
        it["id"] = str(it.pop("_id"))
    return it


@app.post("/api/contact")
def submit_contact(payload: ContactPayload):
    doc = payload.model_dump()
    _id = create_document("contactmessage", doc) if db else None
    return {"status": "ok", "id": _id}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
