import os
import re
from datetime import datetime
from pathlib import Path
from agentic_code.crew import AgenticCodeCrew

def extract_and_save_files(result_text, project_name):
    """
    Robust extraction engine to parse agent output and rebuild project structure.
    """
    # 1. Setup Base Path
    results_base = os.path.join("Results", project_name)
    os.makedirs(results_base, exist_ok=True)
    
    # 2. Extract content starting from the first valid marker
    start_index = result_text.find("--- FILE:")
    if start_index == -1:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join("Results", f"raw_output_{timestamp}.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(result_text)
        print(f"⚠️ No markers found. Saved raw text to: {filepath}")
        return

    clean_text = result_text[start_index:]

    # 3. Universal Regex: Captures filename and code content up to the next marker
    #
    pattern = r'--- FILE:\s*(.*?)\s*---\s*(.*?)(?=\s*--- FILE:|$)'
    matches = re.findall(pattern, clean_text, re.DOTALL)

    for rel_path, content in matches:
        # Normalize paths for Windows/Linux compatibility
        rel_path = rel_path.strip().replace('\\', '/')
        
        # 4. Content Cleaning (Removes markdown artifacts)
        clean_content = content.strip()
        if clean_content.startswith("```"):
            clean_content = re.sub(r'^```[a-zA-Z0-9]*\n', '', clean_content)
            clean_content = re.sub(r'```$', '', clean_content)

        # 5. Atomic Write to Disk
        full_path = os.path.join(results_base, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(clean_content.strip())
                f.flush()
                os.fsync(f.fileno()) # Force write to D: drive immediately
            print(f"✅ Created: {rel_path}")
        except Exception as e:
            print(f"❌ Error writing {rel_path}: {e}")

    # --- AUTO-STABILIZATION ---
    # Ensure src is a valid Python package
    src_dir = os.path.join(results_base, "src")
    if os.path.exists(src_dir):
        init_file = os.path.join(src_dir, "__init__.py")
        if not os.path.exists(init_file):
            Path(init_file).touch()
            print(f"🛠️ Package Fix: Created {init_file}")

    # Ensure data directory is present for CSV/Storage tasks
    os.makedirs(os.path.join(results_base, "data"), exist_ok=True)
    
    # Fallback requirements if agent fails to specify
    req_file = os.path.join(results_base, "requirements.txt")
    if not os.path.exists(req_file):
        with open(req_file, "w") as f:
            f.write("pandas\nstreamlit\nplotly\nmatplotlib\n")
        print("🛠️ Environment Fix: Added fallback requirements.txt")

def run():
    print("\n" + "="*40)
    print("🚀 UNIVERSAL AGENTIC ENGINE STANDBY")
    print("="*40)
    
    input_file = 'task_input.txt'
    if not os.path.exists(input_file):
        print(f"[!] Missing {input_file}. Create it to provide a task.")
        return
        
    with open(input_file, 'r', encoding="utf-8") as f:
        user_task = f.read().strip()

    if not user_task:
        print("[!] task_input.txt is empty.")
        return

    print(f"\n[Running Task]: {user_task}")
    
    try:
        # Trigger CrewAI
        crew_instance = AgenticCodeCrew().crew()
        result = crew_instance.kickoff(inputs={'topic': user_task})
        
        # Generate unique folder
        project_id = datetime.now().strftime("Project_%Y%m%d_%H%M%S")
        
        print("\n[📦] Unpacking code structure...")
        extract_and_save_files(str(result), project_id)
        print(f"\n🏁 Project Complete! Path: Results/{project_id}")
        
    except Exception as e:
        print(f"❌ Critical Failure in Crew Execution: {e}")

if __name__ == "__main__":
    run()