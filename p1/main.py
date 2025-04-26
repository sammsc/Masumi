
import os
import uvicorn
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, ValidationError
from datetime import datetime, timezone
from typing import List, Optional
from crew_definition import ResearchCrew,SurveillanceCrew,CertificateCrew,InvestigateCrew
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import JSONResponse



# Load environment variables
load_dotenv()

# Retrieve OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI
app = FastAPI()

# ─────────────────────────────────────────────────────────────────────────────
# Temporary in-memory job store (DO NOT USE IN PRODUCTION)
# ─────────────────────────────────────────────────────────────────────────────
jobs = {}

# ─────────────────────────────────────────────────────────────────────────────
# Pydantic Models
# ─────────────────────────────────────────────────────────────────────────────

class KeyValuePair(BaseModel):
    key: str
    value: str

class StartJobRequest(BaseModel):
    # Per MIP-003, input_data should be defined under input_schema endpoint
    text: str

class ProvideInputRequest(BaseModel):
    job_id: str

class SurveilRequest(BaseModel):
    text: str



class CertificateRequest(BaseModel):
    text: str

class InvestigateRequest(BaseModel):
    text: str    

#___________________________________________________________________________


#__________________________________________________________________________
# core func

@app.post("/certificate")
async def certificate(request: CertificateRequest):
    """
    Endpoint to process transaction metadata.
    """
    if not OPENAI_API_KEY:
        return {"status": "error", "message": "Missing OpenAI API Key. Check your .env file."}

    job_id = str(uuid.uuid4())
    payment_id = str(uuid.uuid4())

    jobs[job_id] = {
        "status": "awaiting payment",  # Could also be 'awaiting payment', 'running', etc.
        "payment_id": payment_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "input_data": request.text,
        "certificate_result" : None
    }



    crew = CertificateCrew()  # Instantiate the certificate crew
    
    
    inputs = {"input_data": request.text}
    result = crew.crew.kickoff(inputs)

    # Store result as if we immediately completed it (placeholder)
    jobs[job_id]["status"] = "completed"
    jobs[job_id]["result"] = result
    #return result  # Return plain text, as required

    #nft certification
    cert_nft =        {
        "721": {
            "policy_id": {
            "asset_name": {
                "name": "Certification NFT",
                "image": "ipfs://<image_hash>",
                "description": "Certification of agentic code trustworthiness",
                "certification_result": "result",
                "certifier_id": "our_agenticDID_placeholder",
                "timestamp": "datetime.now(timezone.utc).isoformat(),"
            }
            }
        }
        }




    return {
        "job_id" : job_id,
        "result": result,  # Optional in MIP-003, included if available
        "payment_id": payment_id
        #"nft_job" : cert_nft
        }

@app.post("/surveil")
async def surveil(request: SurveilRequest):
    """
    Endpoint to process transaction metadata.
    """
    if not OPENAI_API_KEY:
        return {"status": "error", "message": "Missing OpenAI API Key. Check your .env file."}

    job_id = str(uuid.uuid4())
    payment_id = str(uuid.uuid4())

    jobs[job_id] = {
        "status": "awaiting payment",  # Could also be 'awaiting payment', 'running', etc.
        "payment_id": payment_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "input_data": request.text,
        "surveil_result" : None
    }



    crew = SurveillanceCrew()  # Instantiate the surveillance crew
    surveil_result = crew.surveil(request.text)
    #jobs["surveil_result"] = surveil_result
    inputs = {"input_data": request.text}
    result = crew.crew.kickoff(inputs)

    # Store result as if we immediately completed it (placeholder)
    jobs[job_id]["status"] = "completed"
    jobs[job_id]["result"] = result
    #return result  # Return plain text, as required

    return {
        "job_id" : job_id,
        "result": result,  # Optional in MIP-003, included if available
        "payment_id": payment_id
        }

    
#######################################?

@app.post("/investigate")
async def investigate(request: InvestigateRequest):
    """
    Endpoint to process transaction metadata.
    """
    if not OPENAI_API_KEY:
        return {"status": "error", "message": "Missing OpenAI API Key. Check your .env file."}

    job_id = str(uuid.uuid4())
    payment_id = str(uuid.uuid4())

    jobs[job_id] = {
        "status": "awaiting payment",  # Could also be 'awaiting payment', 'running', etc.
        "payment_id": payment_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "input_data": request.text,
        "investigate_result" : None
    }



    crew = InvestigateCrew()  # Instantiate the surveillance crew
   
    
    inputs = {"input_data": request.text}
    result = crew.crew.kickoff(inputs)

    # Store result as if we immediately completed it (placeholder)
    jobs[job_id]["status"] = "completed"
    jobs[job_id]["result"] = result
    #return result  # Return plain text, as required

    return {
        "job_id" : job_id,
        "result": result,  # Optional in MIP-003, included if available
        "payment_id": payment_id
        }



# ─────────────────────────────────────────────────────────────────────────────
# 1) Start Job (MIP-003: /start_job)
# ─────────────────────────────────────────────────────────────────────────────
@app.post("/start_job")
async def start_job(request_body: StartJobRequest):
    """
    Initiates a job with specific input data.
    Fulfills MIP-003 /start_job endpoint.
    """
    if not OPENAI_API_KEY:
        return {"status": "error", "message": "Missing OpenAI API Key. Check your .env file."}

    # Generate unique job & payment IDs
    job_id = str(uuid.uuid4())
    payment_id = str(uuid.uuid4())  # Placeholder, in production track real payment

    # For demonstration: set job status to 'awaiting payment'
    jobs[job_id] = {
        "status": "awaiting payment",  # Could also be 'awaiting payment', 'running', etc.
        "payment_id": payment_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "input_data": request_body.text,
        "result": None
    }

    # Here you invoke your crew
    crew = ResearchCrew()
    inputs = {"input_data": request_body.text}
    result = crew.crew.kickoff(inputs)

    # Store result as if we immediately completed it (placeholder)
    jobs[job_id]["status"] = "completed"
    jobs[job_id]["result"] = result

    return {
        "status": "success",
        "job_id": job_id,
        "payment_id": payment_id
    }

# ─────────────────────────────────────────────────────────────────────────────
# 2) Check Job Status (MIP-003: /status)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/status")
async def check_status(job_id: str = Query(..., description="Job ID to check status")):
    """
    Retrieves the current status of a specific job.
    Fulfills MIP-003 /status endpoint.
    """
    if job_id not in jobs:
        # Return 404 in a real system; here, just return a JSON error
        return {"error": "Job not found"}

    job = jobs[job_id]
    return {
        "job_id": job_id,
        "status": job["status"],
        "result": job["result"],  # Optional in MIP-003, included if available
        #"surveil_result": job.get("surveil_result"), 
    }  

# ─────────────────────────────────────────────────────────────────────────────
# 3) Provide Input (MIP-003: /provide_input)
# ─────────────────────────────────────────────────────────────────────────────
@app.post("/provide_input")
async def provide_input(request_body: ProvideInputRequest):
    """
    Allows users to send additional input if a job is in an 'awaiting input' status.
    Fulfills MIP-003 /provide_input endpoint.
    
    In this example we do not require any additional input, so it always returns success.
    """
    job_id = request_body.job_id

    if job_id not in jobs:
        return {"status": "error", "message": "Job not found"}

    job = jobs[job_id]

    return {"status": "success"}

# ─────────────────────────────────────────────────────────────────────────────
# 4) Check Server Availability (MIP-003: /availability)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/availability")
async def check_availability():
    """
    Checks if the server is operational.
    Fulfills MIP-003 /availability endpoint.
    """
    # Simple placeholder. In a real system, you might run
    # diagnostic checks or return server load info.
    return {
        "status": "available",
        "message": "The server is running smoothly."
    }

# ─────────────────────────────────────────────────────────────────────────────
# 5) Retrieve Input Schema (MIP-003: /input_schema)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/input_schema")
async def input_schema():
    """
    Returns the expected input schema for the /start_job and /surveil endpoints.
    """
    schema_example = {
        "start_job": [
            {"key": "text", "value": "string"}
        ],
        "surveil": [
            {"key": "text", "value": "string"}
        ]
    }
    return schema_example


# ─────────────────────────────────────────────────────────────────────────────
# Main logic if called as a script
# ─────────────────────────────────────────────────────────────────────────────
def main():
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY is missing. Please check your .env file.")
        return

    crew = ResearchCrew()
    inputs = {"text": "The impact of AI on the job market"}
    result = crew.crew.kickoff(inputs)

    print("\nCrew Output:\n", result)

if __name__ == "__main__":
    import sys

    # If 'api' argument is passed, start the FastAPI server
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        print("Starting FastAPI server...")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        main()
