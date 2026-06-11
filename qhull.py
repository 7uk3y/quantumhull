import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt

def plot_hull(ax, points, hull, title, is_entangled=False):
    """Helper function to draw the Polytope (The Jewel)"""
    ax.set_title(title)
    
    # Plot the vertices (Particles and Walls)
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], color='red', s=60)
    
    # If Entangled, label Photons A and B (the last two points)
    if is_entangled:
        ax.text(points[-2, 0], points[-2, 1], points[-2, 2], ' Phot A', color='black', fontweight='bold')
        ax.text(points[-1, 0], points[-1, 1], points[-1, 2], ' Phot B', color='black', fontweight='bold')

    # Draw the facets (The 2D Sheets)
    for simplex in hull.simplices:
        triangle = points[simplex]
        ax.plot(triangle[:, 0], triangle[:, 1], triangle[:, 2], color='blue', alpha=0.5)
        ax.plot([triangle[-1, 0], triangle[0, 0]], 
                [triangle[-1, 1], triangle[0, 1]], 
                [triangle[-1, 2], triangle[0, 2]], color='blue', alpha=0.5)
    
    # Keep axes static to easily see geometry
    ax.set_xlim([0, 1.5])
    ax.set_ylim([0, 1.5])
    ax.set_zlim([0, 1.5])
    ax.set_xlabel('Momentum')
    ax.set_ylabel('Phase')
    ax.set_zlabel('Polarity')

def run_random_interaction(num_photons=5):
    """PHASE 1: Simulates N random photons interacting (No Entanglement)"""
    print(f"\n--- MODE: RANDOM INTERACTION ({num_photons} Photons) ---")
    
    # 1. Generate random particles in positive space
    particle_vectors = np.random.uniform(0.1, 1.0, (num_photons, 3))
    
    # 2. Define the Walls (Origin and Energy Limit)
    origin = np.array([[0, 0, 0]])
    energy_limit = np.array([[1.5, 1.5, 1.5]])
    
    # 3. Build Database and Shape
    vector_database = np.vstack((origin, particle_vectors, energy_limit))
    hull = ConvexHull(vector_database)
    
    print(f"Generated {num_photons} independent particles.")
    print(f"PROBABILITY AMPLITUDE (Volume): {hull.volume:.4f}")

    # 4. Visualize
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    plot_hull(ax, vector_database, hull, f"Random Interaction (Vol: {hull.volume:.3f})")
    plt.show()

def run_entanglement():
    """PHASE 2: Simulates 2 Entangled Photons collapsing instantly"""
    print("\n--- MODE: ENTANGLED PAIR (BBO Crystal) ---")

    # 1. Define Walls (Detectors) and the Pump Photon
    environment = np.array([[0.0, 0.0, 0.0], [1.2, 0.1, 0.1], [0.1, 1.2, 0.1]])
    pump_photon = np.array([1.0, 1.0, 1.0])

    # 2. Create Superposition State (Photon B is locked to Photon A)
    photon_A = np.random.uniform(0.2, 0.8, 3)
    photon_B = pump_photon - photon_A 

    print(f"Initial State (Superposition):")
    print(f"  Photon A: {photon_A.round(3)}")
    print(f"  Photon B: {photon_B.round(3)}")

    db_initial = np.vstack((environment, photon_A, photon_B))
    hull_initial = ConvexHull(db_initial)

    # 3. Alice Measures Photon A (Force Polarity/Z to 0.9)
    print("\n[!] Alice measures Photon A (Forces Polarity to 0.9)...")
    photon_A_measured = np.copy(photon_A)
    photon_A_measured[2] = 0.9 

    # 4. Spooky Action: Photon B instantly updates
    photon_B_measured = pump_photon - photon_A_measured

    print(f"Post-Measurement State (Collapsed):")
    print(f"  Photon A: {photon_A_measured.round(3)}")
    print(f"  Photon B: {photon_B_measured.round(3)}")

    db_measured = np.vstack((environment, photon_A_measured, photon_B_measured))
    hull_measured = ConvexHull(db_measured)

    print(f"\nPROBABILITY AMPLITUDE SHIFT:")
    print(f"  Initial Volume:  {hull_initial.volume:.4f}")
    print(f"  Measured Volume: {hull_measured.volume:.4f}")

    # 5. Visualize Before and After
    fig = plt.figure(figsize=(12, 5))
    ax1 = fig.add_subplot(121, projection='3d')
    plot_hull(ax1, db_initial, hull_initial, f"Superposition (Vol: {hull_initial.volume:.3f})", is_entangled=True)
    
    ax2 = fig.add_subplot(122, projection='3d')
    plot_hull(ax2, db_measured, hull_measured, f"Collapsed (Vol: {hull_measured.volume:.3f})", is_entangled=True)
    
    plt.tight_layout()
    plt.show()

# ==========================================
# THE TOGGLE SWITCH
# Change this variable to switch modes!
# Options: "random" or "entangled"
# ==========================================

SIMULATION_MODE = "entangled"

if __name__ == "__main__":
    if SIMULATION_MODE == "random":
        # You can change the number of photons here!
        run_random_interaction(num_photons=10)
    elif SIMULATION_MODE == "entangled":
        run_entanglement()
    else:
        print("Invalid mode. Please set SIMULATION_MODE to 'random' or 'entangled'.")
