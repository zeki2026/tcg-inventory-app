from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import User, UserRole
from app.dependencies import get_current_user
import asyncio
from datetime import datetime

router = APIRouter()

from app.services.email_service import email_service
from app.schemas import EmailSchema
import os

def generate_pdf_report(user_email: str):
    # Simulate PDF generation
    report_content = f"Report for {user_email}\nGenerated at {datetime.utcnow()}"
    filename = f"report_{user_email}_{datetime.utcnow().timestamp()}.txt"
    with open(filename, "w") as f:
        f.write(report_content)
    
    # Send Email
    payload = EmailSchema(
        to_email=user_email,
        subject="Your TCG Portfolio Report",
        body="Please find attached your requested report.",
        attachment_path=filename
    )
    email_service.send_email(payload)
    
    # Cleanup
    if os.path.exists(filename):
        os.remove(filename)

@router.post("/summary")
async def generate_summary_report(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.PRO:
        return {"message": "Upgrade to PRO for detailed reports", "status": "restricted"}

    background_tasks.add_task(generate_pdf_report, current_user.email)
    return {"message": "Report generation started. You will receive an email shortly."}
