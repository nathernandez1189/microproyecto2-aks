from torchvision.models import MobileNet_V3_Small_Weights, mobilenet_v3_small

# The weights are part of the container image, not downloaded when a Pod starts.
mobilenet_v3_small(weights=MobileNet_V3_Small_Weights.IMAGENET1K_V1)
print('MobileNetV3 Small weights cached successfully.')
