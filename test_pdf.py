"""
Standalone script to test PDF generation without running the full application.
Run this from the project root: python test_pdf.py
"""

from datetime import datetime
import sys
import os

# Add backend to path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.pdf_generator import generate_course_report

def test_pdf_generation():
    """Test PDF generation with sample data."""
    
    print(">>> Testing PDF Generation...")
    print("-" * 50)
    
    # Sample user data
    user_data = {
        "email": "dheerajkumarsharmaa@gmail.com",
        "trainee_name": "Dheeraj Kumar Sharma",
        "role": "Trainee"
    }
    
    # Sample session data - Test Case 1: Mixed Progress
    session_data_1 = {
        "session_id": 1,
        "session_timestamp": datetime.now(),
        "chapter_data": [
            {"chapter": "Briefing Room", "score": 9, "status": "Completed"},
            {"chapter": "Arrival on Piper Alpha", "score": 8, "status": "Completed"},
            {"chapter": "Maintenance Area", "score": 7, "status": "Completed"},
            {"chapter": "Precursor to Disaster", "score": 6, "status": "Pending"},
            {"chapter": "Explosion Simulation", "score": 0, "status": "Not Completed"},
        ]
    }
    
    # Test Case 2: All Completed
    session_data_2 = {
        "session_id": 2,
        "session_timestamp": datetime.now(),
        "chapter_data": [
            {"chapter": "Briefing Room", "score": 10, "status": "Completed"},
            {"chapter": "Arrival on Piper Alpha", "score": 9, "status": "Completed"},
            {"chapter": "Maintenance Area", "score": 9, "status": "Completed"},
            {"chapter": "Precursor to Disaster", "score": 8, "status": "Completed"},
            {"chapter": "Explosion Simulation", "score": 8, "status": "Completed"},
            {"chapter": "Escape Aftermath", "score": 9, "status": "Completed"},
            {"chapter": "Debrief", "score": 10, "status": "Completed"}
        ]
    }
    
    # Test Case 3: Just Started
    session_data_3 = {
        "session_id": 3,
        "session_timestamp": datetime.now(),
        "chapter_data": [
            {"chapter": "Briefing Room", "score": 5, "status": "Pending"},
            {"chapter": "Arrival on Piper Alpha", "score": 0, "status": "Not Completed"},
            {"chapter": "Maintenance Area", "score": 0, "status": "Not Completed"},
        ]
    }
    
    # Generate PDFs
    test_cases = [
        ("Test_Report_Mixed_Progress.pdf", session_data_1, "Mixed progress (3 completed, 1 pending, 1 not completed)"),
        ("Test_Report_All_Completed.pdf", session_data_2, "All chapters completed with high scores"),
        ("Test_Report_Just_Started.pdf", session_data_3, "Just started training")
    ]
    
    for filename, session_data, description in test_cases:
        try:
            print(f"\n>>> Generating: {filename}")
            print(f"   Description: {description}")
            
            # Generate PDF
            pdf_buffer = generate_course_report(user_data, session_data)
            
            # Save to file
            with open(filename, "wb") as f:
                f.write(pdf_buffer.getvalue())
            
            # Get file size
            file_size = os.path.getsize(filename)
            
            print(f"   SUCCESS! File size: {file_size:,} bytes")
            print(f"   Saved to: {os.path.abspath(filename)}")
            
        except Exception as e:
            print(f"   ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print(">>> PDF Generation Test Complete!")
    print("=" * 50)
    print("\nGenerated files:")
    for filename, _, description in test_cases:
        if os.path.exists(filename):
            print(f"  [OK] {filename}")
    print("\nOpen these files to verify the PDFs are correct.")


if __name__ == "__main__":
    test_pdf_generation()

