#!/usr/bin/env python3
"""Test script to verify database and all scripts work correctly."""

import sys
import json
import subprocess
from pathlib import Path

def run_script(script_name, args):
    """Run a Python script and return the result."""
    script_dir = Path(__file__).parent
    cmd = ["python", str(script_dir / script_name)] + args
    try:
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_name}: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error for {script_name}: {e}")
        print(f"Output was: {result.stdout}")
        return None

def main():
    print("🧪 AIMEN System Test Suite\n")
    
    # Test 1: Initialize database
    print("1️⃣ Testing database initialization...")
    result = run_script("init_db.py", [])
    if result and result.get("success"):
        print(f"   ✅ Database initialized: {result.get('path')}")
    else:
        print("   ❌ Database initialization failed")
        return 1
    
    # Test 2: Create product
    print("\n2️⃣ Testing product creation...")
    result = run_script("product.py", [
        "create",
        "--name", "Test Product",
        "--description", "A test product for verification"
    ])
    if result and result.get("success"):
        product_id = result["data"]["id"]
        print(f"   ✅ Product created with ID: {product_id}")
    else:
        print("   ❌ Product creation failed")
        return 1
    
    # Test 3: List products
    print("\n3️⃣ Testing product listing...")
    result = run_script("product.py", ["list"])
    if result and result.get("success") and len(result["data"]) > 0:
        print(f"   ✅ Found {len(result['data'])} product(s)")
    else:
        print("   ❌ Product listing failed")
        return 1
    
    # Test 4: Create feature
    print("\n4️⃣ Testing feature creation...")
    result = run_script("feature.py", [
        "create",
        "--product-id", str(product_id),
        "--name", "Test Feature",
        "--branch", "001-test-feature",
        "--priority", "high"
    ])
    if result and result.get("success"):
        feature_id = result["data"]["id"]
        print(f"   ✅ Feature created with ID: {feature_id}")
    else:
        print("   ❌ Feature creation failed")
        return 1
    
    # Test 5: List features
    print("\n5️⃣ Testing feature listing...")
    result = run_script("feature.py", ["list", "--product-id", str(product_id)])
    if result and result.get("success") and len(result["data"]) > 0:
        print(f"   ✅ Found {len(result['data'])} feature(s)")
    else:
        print("   ❌ Feature listing failed")
        return 1
    
    # Test 6: Create task
    print("\n6️⃣ Testing task creation...")
    result = run_script("task.py", [
        "create",
        "--feature-id", str(feature_id),
        "--task-id", "T001",
        "--description", "Test task implementation",
        "--phase", "Setup",
        "--file", "test.py"
    ])
    if result and result.get("success"):
        task_id = result["data"]["id"]
        print(f"   ✅ Task created with ID: {task_id}")
    else:
        print("   ❌ Task creation failed")
        return 1
    
    # Test 7: Update task status
    print("\n7️⃣ Testing task status update...")
    result = run_script("task.py", [
        "update",
        "--id", str(task_id),
        "--status", "doing"
    ])
    if result and result.get("success"):
        print(f"   ✅ Task status updated to 'doing'")
    else:
        print("   ❌ Task status update failed")
        return 1
    
    # Test 8: Get current work
    print("\n8️⃣ Testing current work query...")
    result = run_script("status.py", ["current"])
    if result and result.get("success"):
        data = result["data"]
        print(f"   ✅ Current work: {len(data['features'])} feature(s), {len(data['tasks'])} task(s) in progress")
    else:
        print("   ❌ Current work query failed")
        return 1
    
    # Test 9: Get statistics
    print("\n9️⃣ Testing statistics query...")
    result = run_script("status.py", ["stats"])
    if result and result.get("success"):
        print(f"   ✅ Statistics generated")
    else:
        print("   ❌ Statistics query failed")
        return 1
    
    # Test 10: Get workflow status
    print("\n🔟 Testing workflow status query...")
    result = run_script("status.py", ["workflow", "--feature-id", str(feature_id)])
    if result and result.get("success"):
        stage = result["data"]["current_stage"]
        print(f"   ✅ Workflow stage: {stage}")
    else:
        print("   ❌ Workflow status query failed")
        return 1
    
    # Test 11: Advance workflow
    print("\n1️⃣1️⃣ Testing workflow advancement...")
    result = run_script("transition.py", [
        "advance",
        "--feature-id", str(feature_id),
        "--next-stage", "clarify"
    ])
    if result and result.get("success"):
        print(f"   ✅ Workflow advanced to 'clarify'")
    else:
        print("   ❌ Workflow advancement failed")
        return 1
    
    # Test 12: Complete feature
    print("\n1️⃣2️⃣ Testing feature completion...")
    result = run_script("transition.py", [
        "complete-feature",
        "--feature-id", str(feature_id)
    ])
    if result and result.get("success"):
        print(f"   ✅ Feature marked as completed")
    else:
        print("   ❌ Feature completion failed")
        return 1
    
    print("\n" + "="*50)
    print("🎉 All tests passed! AIMEN system is ready to use!")
    print("="*50)
    return 0

if __name__ == "__main__":
    sys.exit(main())
