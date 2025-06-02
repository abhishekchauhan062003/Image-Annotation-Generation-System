# utils/visualizer.py

import matplotlib.pyplot as plt

def visualize_feature_maps(visualizations):
    for layer_name, activation in visualizations:
        num_filters = min(6, activation.shape[-1])
        fig, axes = plt.subplots(1, num_filters, figsize=(15, 5))
        fig.suptitle(layer_name)

        for i in range(num_filters):
            ax = axes[i]
            ax.imshow(activation[0, :, :, i], cmap='viridis')
            ax.axis('off')

        plt.tight_layout()
        plt.show()
