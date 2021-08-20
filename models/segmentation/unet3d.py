
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.modules.activation import ReLU
from torch.nn.modules.conv import ConvTranspose3d


def initial_convolution(in_channels, middle_channels, out_channels):
    conv = nn.Sequential(
        nn.Conv3d(in_channels, middle_channels, stride=1, kernel_size=3, padding=1),
        nn.ReLU(inplace=False),
       # nn.BatchNorm3d(),
        nn.Conv3d(middle_channels, out_channels, stride=1, kernel_size=3, padding=1),
        nn.ReLU(inplace=False),
        #nn.BatchNorm3d(),
    )
    return conv


def  downsample():
    return nn.MaxPool3d(kernel_size=2, stride=2)


def double_convolution(in_channels, out_channels):
    conv = nn.Sequential(
        nn.Conv3d(in_channels, out_channels, stride=1, kernel_size=3, padding=1),
        nn.ReLU(inplace=False),
       # nn.BatchNorm3d(),
        nn.Conv3d(in_channels, out_channels, stride=1, kernel_size=3, padding=1),
        nn.ReLU(inplace=False),
        #nn.BatchNorm3d(),
    )
    return conv


def upsample(in_channels, out_channels):
    return nn.ConvTranspose3d(in_channels, out_channels, kernel_size=2, stride=2)


def final_convolution(in_channels, out_channels):
    return nn.Conv3d(in_channels, out_channels, kernel_size=1)


def cat_block(block_1, block_2):
    return torch.cat(block_1, block_2)


class UNet3D (nn.Module):
    """UNet3D model PyTorch.

    Args:
        in_channels (int): input channels
        init_features (int): 
        out_classes (int):
    
    """
    def __init__(self, in_channels=2, init_features=32, out_classes=2):
        super().__init__()
        features = init_features

        # Encoders Layers
        self.init_conv = initial_convolution(in_channels, features, features * 2)
        self.conv_down_1 = double_convolution(features * 2, features * 4)
        self.conv_down_2 = double_convolution()
        

    def forward(self, image):
        # Encoder
        lol = 2
        # Decoder
        return None