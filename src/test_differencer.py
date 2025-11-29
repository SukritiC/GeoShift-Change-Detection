from src.differencer import compute_change, save_results
import rasterio
import os


def test_differencer():
    before_path = "data/before.tif"
    after_path = "data/after.tif"

    if not os.path.exists(before_path) or not os.path.exists(after_path):
        print("Mock data not found. Run src/generate_mock_data.py first.")
        return

    print("Running differencer on mock data...")
    diff, mask = compute_change(before_path, after_path)

    print(f"Difference map shape: {diff.shape}")
    print(f"Mask shape: {mask.shape}")
    print(f"Mask unique values: {set(mask.flatten())}")

    # Check if we detected change (should be some True values)
    if mask.any():
        print("SUCCESS: Change detected.")
    else:
        print("FAILURE: No change detected.")

    # Test saving
    os.makedirs("results", exist_ok=True)
    with rasterio.open(before_path) as src:
        profile = src.profile
        save_results(
            diff, mask, profile, "results/test_diff.tif", "results/test_mask.tif"
        )

    if os.path.exists("results/test_diff.tif") and os.path.exists(
        "results/test_mask.tif"
    ):
        print("SUCCESS: Results saved.")
    else:
        print("FAILURE: Results not saved.")


if __name__ == "__main__":
    test_differencer()
