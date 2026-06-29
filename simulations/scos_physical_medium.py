class SCOSPhysicalMedium:
    def __init__(self, physical_constant=3.9999):
        """
        Simulates a non-man-made physical medium, such as a chaotic crystal or
        optical loop, using a highly sensitive nonlinear chaotic map.

        The physical_constant represents the baseline environmental state
        parameter r.
        """
        self.r = physical_constant

    def interact(self, digital_seed: float, input_data: list, environmental_temp=293.15) -> float:
        """
        Simulates passing a tiny digital seed into the open external medium.
        The input data perturbs the natural physical states, mapping the entire
        sequence into a single dense macroscopic final state.
        """
        # Toy-scale perturbation used to make the fidelity failure visible in
        # double-precision simulation.
        thermal_noise = (environmental_temp - 293.15) * 1e-1
        state = digital_seed + thermal_noise

        for bit in input_data:
            # Natural chaotic state transformation: x_{n+1} = r * x_n * (1 - x_n)
            state = self.r * state * (1.0 - state)

            # The data interacts with the medium, creating a microscopic perturbation.
            state = (state + (bit * 0.0001)) % 1.0

        return state

    def reconstruct(self, digital_seed: float, target_state: float, data_length: int, tolerance=1e-7) -> list:
        """
        Reconstructs the original data by searching for the path through the
        physical medium that lands on the target state.
        """
        print("[SCOS] Reconstructing original file from physical state vector...")

        def pathfind(current_state, depth):
            if depth == data_length:
                return abs(current_state - target_state) < tolerance, []

            for choice in [0, 1]:
                next_state = self.r * current_state * (1.0 - current_state)
                next_state = (next_state + (choice * 0.0001)) % 1.0

                success, path = pathfind(next_state, depth + 1)
                if success:
                    return True, [choice] + path

            return False, []

        success, path = pathfind(digital_seed, 0)
        if success:
            return path

        raise ValueError("Data Corruption Error: State Fidelity altered! Readout failed.")


if __name__ == "__main__":
    medium = SCOSPhysicalMedium()

    original_file = [1, 0, 1, 1, 0, 0, 1, 0]
    print(f"Original File Content : {original_file} (Size: {len(original_file)} bits)")

    digital_seed = 0.5000000
    print(f"Compressed Digital Seed: {digital_seed} (Size: Constant 1 Float)")

    print("\n--- Encoding Phase ---")
    print("[SCOS] Passing seed through the external open medium...")

    physical_state_hash = medium.interact(digital_seed, original_file, environmental_temp=293.15)
    print(f"[SUCCESS] Unique Physical State Captured: {physical_state_hash:.10f}")
    print("The information is now distributed within the medium's atomic configuration.")

    print("\n--- Decoding Phase (Perfect Conditions) ---")
    recovered_file = medium.reconstruct(digital_seed, physical_state_hash, len(original_file))
    print(f"[SUCCESS] Recovered File : {recovered_file}")
    print(f"Verification Match      : {original_file == recovered_file}")

    print("\n--- Decoding Phase (Environmental Interruption / Noise) ---")
    try:
        print("[ALERT] Temperature fluctuation detected (+0.001 K)...")
        corrupted_state = medium.interact(digital_seed, original_file, environmental_temp=293.151)
        medium.reconstruct(digital_seed, corrupted_state, len(original_file))
    except ValueError as e:
        print(f"[FAILURE] {e}")
        print("Proof Confirmed: Universal scaling requires absolute State Fidelity containment.")
