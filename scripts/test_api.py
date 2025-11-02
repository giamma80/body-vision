#!/usr/bin/env python3
"""End-to-end test script for BodyVision API."""

import time

import httpx

BASE_URL = "http://localhost:8000"


def test_health_check() -> None:
    """Test health endpoint."""
    print("🏥 Testing health endpoint...")
    response = httpx.get(f"{BASE_URL}/health")
    assert response.status_code == 200, f"Health check failed: {response.text}"
    data = response.json()
    print(f"✅ Health check passed: {data}")
    print()


def test_create_prediction() -> str:
    """Test creating a prediction job."""
    print("📸 Creating prediction job...")

    payload = {
        "front_image_url": "https://example.com/images/front.jpg",
        "side_image_url": "https://example.com/images/side.jpg",
        "back_image_url": "https://example.com/images/back.jpg",
        "user_metadata": {
            "email": "test@example.com",
            "height_cm": 175.0,
            "weight_kg": 75.0,
            "age": 30,
            "gender": "male",
        },
    }

    response = httpx.post(f"{BASE_URL}/api/predict/", json=payload, timeout=10.0)
    assert response.status_code == 202, f"Prediction creation failed: {response.text}"

    data = response.json()
    job_id = data["job_id"]
    session_id = data["session_id"]

    print(f"✅ Job created successfully!")
    print(f"   Job ID: {job_id}")
    print(f"   Session ID: {session_id}")
    print(f"   Status: {data['status']}")
    print()

    return job_id


def test_get_status(job_id: str, wait_for_completion: bool = False) -> dict:
    """Test getting job status."""
    print(f"📊 Checking status for job {job_id}...")

    max_attempts = 15 if wait_for_completion else 1
    attempt = 0

    while attempt < max_attempts:
        response = httpx.get(f"{BASE_URL}/api/predict/{job_id}", timeout=10.0)
        assert response.status_code == 200, f"Status check failed: {response.text}"

        data = response.json()
        status = data["status"]

        print(f"   Status: {status}")

        if status == "completed":
            print("✅ Job completed!")
            print(f"   Processing time: {data['processing_time_seconds']:.2f}s")
            print(f"   Model used: {data['model_used']}")

            if data.get("measurements"):
                meas = data["measurements"]
                print("\n📊 Measurements:")
                print(f"   Body Fat: {meas['body_fat_percentage']:.1f}%")
                print(f"   Volume: {meas['body_volume_liters']:.2f}L")
                print(f"   Density: {meas['body_density_kg_per_liter']:.3f} kg/L")
                print(f"   Lean Mass: {meas['lean_mass_kg']:.1f}kg")
                print(f"   Fat Mass: {meas['fat_mass_kg']:.1f}kg")
                print(f"   Confidence: {meas['confidence_score']:.1%}")

            print()
            return data

        elif status == "failed":
            print(f"❌ Job failed: {data.get('error_message')}")
            print()
            return data

        elif wait_for_completion:
            print(f"   ⏳ Waiting... (attempt {attempt + 1}/{max_attempts})")
            time.sleep(2)
            attempt += 1
        else:
            return data

    if wait_for_completion and status != "completed":
        print(f"⚠️  Job did not complete within {max_attempts * 2}s")

    return data


def main() -> None:
    """Run end-to-end tests."""
    print("\n" + "=" * 60)
    print("BodyVision API End-to-End Test")
    print("=" * 60 + "\n")

    try:
        # 1. Health check
        test_health_check()

        # 2. Create prediction
        job_id = test_create_prediction()

        # 3. Check status immediately
        test_get_status(job_id, wait_for_completion=False)

        # 4. Wait for completion
        print("⏳ Waiting for job to complete (this may take 2-5 seconds)...\n")
        test_get_status(job_id, wait_for_completion=True)

        print("=" * 60)
        print("✅ All tests passed!")
        print("=" * 60 + "\n")

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}\n")
        exit(1)
    except httpx.ConnectError:
        print("\n❌ Could not connect to API server.")
        print("   Make sure the server is running: make dev\n")
        exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")
        exit(1)


if __name__ == "__main__":
    main()
