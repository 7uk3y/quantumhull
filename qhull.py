import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt

def calculate_interaction_amplitude(num_photons):
    """
    Simulates a multi-photon interaction by mapping them into a Vector DB (Property Space),
    building a geometric shape, and calculating its volume.
    """
    print(f"--- Simulating {num_photons}-Photon Interaction ---")
    
    # 1. CREATE THE VECTORS (The Particles)
    # Let's use 3 dimensions so we can visualize it: [Momentum, Phase, Polarity]
    # In reality, this would be 16D, 32D, etc.
    # We use np.random.uniform(0.1, 1.0) to keep them strictly in "Positive Space".
    
    particle_vectors = np.random.uniform(0.1, 1.0, (num_photons, 3))
    print(f"Generated {num_photons} Particle Vectors in Positive Space.")

    # 2. CREATE THE WALLS (The Constraints)
    # The universe has rules. 
    # Wall A: The 'Zero' point (Nothing can be less than 0).
    # Wall B: The 'Conservation of Energy' point (Max limit of the system).
    
    origin = np.array([[0, 0, 0]])
    energy_limit = np.array([[1.5, 1.5, 1.5]]) # The maximum bounds of our "fence"
    
    # Overlay the particles and the walls into one single database
    vector_database = np.vstack((origin, particle_vectors, energy_limit))

    # 3. BUILD THE SHAPE (The Polytope)
    # A Convex Hull acts like shrink-wrap. It wraps a multi-dimensional 
    # geometric shape tightly around all the outermost vectors.
    try:
        shape = ConvexHull(vector_database)
    except Exception as e:
        print("Vectors did not form a valid 3D shape:", e)
        return

    # 4. VOLUME = AMPLITUDE
    # We don't trace paths. We just ask the shape for its Volume.
    amplitude = shape.volume
    print(f"SUCCESS: Shape formed with {len(shape.simplices)} facets (2D sheets).")
    print(f"PROBABILITY AMPLITUDE (Volume): {amplitude:.4f}\n")

    # 5. VISUALIZE THE "JEWEL"
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(f"The 'Amplituhedron' for {num_photons} Photons")

    # Plot the points (Particles and Walls)
    ax.scatter(vector_database[:, 0], vector_database[:, 1], vector_database[:, 2], 
               color='red', s=50, label='Vectors (Particles/Walls)')

    # Draw the Facets (The 2D sheets connecting the positive space)
    for simplex in shape.simplices:
        # Get the vertices for each 2D sheet
        triangle = vector_database[simplex]
        # Draw the lines connecting them
        ax.plot(triangle[:, 0], triangle[:, 1], triangle[:, 2], color='blue', alpha=0.5)
        # Close the triangle loop
        ax.plot([triangle[-1, 0], triangle[0, 0]], 
                [triangle[-1, 1], triangle[0, 1]], 
                [triangle[-1, 2], triangle[0, 2]], color='blue', alpha=0.5)

    ax.set_xlabel('Dimension 1: Momentum')
    ax.set_ylabel('Dimension 2: Phase')
    ax.set_zlabel('Dimension 3: Polarity')
    plt.legend()
    plt.show()

# Run the simulation for 5 entangled/interacting photons
calculate_interaction_amplitude(num_photons=5)
