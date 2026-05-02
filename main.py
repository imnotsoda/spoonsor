#fastAPI: webframework
#HTTPException: Python exceptions to terminate req & return structured HTTP error response to client
#CORSMiddleware: lets frontend call backend
#StaticFiles: lets fastAPI serve html files from static/ folder
#BaseModel: data validation for request bodies using pydantic (data validation library)
#Optional: allows some fields to be empty

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
from database import query, execute

app = FastAPI(title="Campus Fundraising Deals")

# allow frontend to call API built by FastAPI (since they r on diff ports)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # allow requests from any origin
    allow_methods=["*"], # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"], # allow all headers
)

# Serve static frontend files from the 'static' directory at /static URL path
app.mount("/static", StaticFiles(directory="static"), name="static")


# _______________________________________________________________
# PYDANTIC MODELS (for request body validation)
# this checks the required fields and types before sending to db

class DealCreate(BaseModel):
    org_id:           int
    restaurant_id:    int
    promo_code:       str
    donation_percent: float
    start_date:       str   # "YYYY-MM-DD"
    end_date:         str   # "YYYY-MM-DD"
    is_active:        bool  = True
    note:             Optional[str] = None
    instruction:      Optional[str] = None
    poster_url:       Optional[str] = None

class DealUpdate(BaseModel):
    org_id:           Optional[int]   = None
    restaurant_id:    Optional[int]   = None
    promo_code:       Optional[str]   = None
    donation_percent: Optional[float] = None
    start_date:       Optional[str]   = None
    end_date:         Optional[str]   = None
    is_active:        Optional[bool]  = None
    note:             Optional[str]   = None
    instruction:      Optional[str]   = None
    poster_url:       Optional[str]   = None


# _______________________________________________________________
# ORGANIZATIONS

@app.get("/organizations")
def get_organizations():
    """Return all orgs — used to populate dropdowns."""
    return query("SELECT * FROM Organizations ORDER BY name")


@app.post("/organizations")
def create_organization(name: str, description: str = None, contact_email: str = None):
    execute(
        "INSERT INTO Organizations (name, description, contact_email) VALUES (%s, %s, %s)",
        (name, description, contact_email)
    )
    return {"message": "Organization created"}


# _______________________________________________________________
# RESTAURANTS

@app.get("/restaurants")
def get_restaurants():
    """Return all restaurants — used to populate dropdowns."""
    return query("SELECT * FROM Restaurants ORDER BY name")


@app.post("/restaurants")
def create_restaurant(name: str, location: str = None, category: str = None, lat: float = None, lng: float = None):
    execute(
        "INSERT INTO Restaurants (name, location, category, lat, lng) VALUES (%s, %s, %s, %s, %s)",
        (name, location, category, lat, lng)
    )
    return {"message": "Restaurant created"}


# _______________________________________________________________
# DEALS - CRUD

@app.get("/deals")
def get_deals(
    org_id:        Optional[int]  = None,
    restaurant_id: Optional[int]  = None,
    category:      Optional[str]  = None,
    is_active:     Optional[bool] = None,
    start_after:   Optional[str]  = None,   # "YYYY-MM-DD"
    end_before:    Optional[str]  = None,   # "YYYY-MM-DD"
):
    """
    Return deals with optional filters.
    Used for both the admin table and the student report.
    All filters use parameterized queries — no SQL injection risk.
    """
    sql = """
        SELECT
            d.deal_id,
            d.promo_code,
            d.donation_percent,
            d.start_date,
            d.end_date,
            d.is_active,
            d.note,
            d.instruction,
            d.poster_url,
            o.name  AS org_name,
            o.org_id,
            r.name  AS restaurant_name,
            r.restaurant_id,
            r.location,
            r.category
        FROM Deals d
        JOIN Organizations o ON d.org_id = o.org_id
        JOIN Restaurants r ON d.restaurant_id = r.restaurant_id
        WHERE 1=1
    """
    params = []

    if org_id is not None:
        sql += " AND d.org_id = %s"
        params.append(org_id)

    if restaurant_id is not None:
        sql += " AND d.restaurant_id = %s"
        params.append(restaurant_id)

    if category is not None:
        sql += " AND r.category = %s"
        params.append(category)

    if is_active is not None:
        sql += " AND d.is_active = %s"
        params.append(is_active)

    if start_after is not None:
        sql += " AND d.start_date >= %s"
        params.append(start_after)

    if end_before is not None:
        sql += " AND d.end_date <= %s"
        params.append(end_before)

    sql += " ORDER BY d.start_date DESC"

    return query(sql, params if params else None)


@app.get("/deals/{deal_id}")
def get_deal(deal_id: int):
    result = query(
        "SELECT * FROM Deals WHERE deal_id = %s",
        (deal_id,),
        fetchall=False
    )
    if not result:
        raise HTTPException(status_code=404, detail="Deal not found")
    return result


@app.post("/deals")
def create_deal(deal: DealCreate):
    execute(
        """
        INSERT INTO Deals
            (org_id, restaurant_id, promo_code, donation_percent,
             start_date, end_date, is_active, note, instruction, poster_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            deal.org_id, deal.restaurant_id, deal.promo_code, deal.donation_percent,
            deal.start_date, deal.end_date, deal.is_active,
            deal.note, deal.instruction, deal.poster_url
        )
    )
    return {"message": "Deal created"}


@app.put("/deals/{deal_id}")
def update_deal(deal_id: int, deal: DealUpdate):
    # Build SET clause dynamically from only the fields provided
    fields = {k: v for k, v in deal.model_dump().items() if v is not None}
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    set_clause = ", ".join(f"{k} = %s" for k in fields)
    values = list(fields.values()) + [deal_id]

    execute(
        f"UPDATE Deals SET {set_clause} WHERE deal_id = %s",
        values
    )
    return {"message": "Deal updated"}


@app.delete("/deals/{deal_id}")
def delete_deal(deal_id: int):
    execute("DELETE FROM Deals WHERE deal_id = %s", (deal_id,))
    return {"message": "Deal deleted"}


# _______________________________________________________________
# REPORT STATS 

@app.get("/report/stats")
def get_report_stats(
    org_id:    Optional[int]  = None,
    is_active: Optional[bool] = None,
    category:  Optional[str]  = None,
):
    """
    Summary stats shown at the top of the student report:
    total deals, average donation %, number of orgs and restaurants involved.
    """
    sql = """
        SELECT
            COUNT(*) AS total_deals,
            ROUND(AVG(d.donation_percent), 2) AS avg_donation_percent,
            COUNT(DISTINCT d.org_id) AS orgs_involved,
            COUNT(DISTINCT d.restaurant_id) AS restaurants_involved
        FROM Deals d
        JOIN Restaurants r ON d.restaurant_id = r.restaurant_id
        WHERE 1=1
    """
    params = []

    if org_id is not None:
        sql += " AND d.org_id = %s"
        params.append(org_id)

    if is_active is not None:
        sql += " AND d.is_active = %s"
        params.append(is_active)

    if category is not None:
        sql += " AND r.category = %s"
        params.append(category)

    return query(sql, params if params else None, fetchall=False)