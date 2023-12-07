import torch
import torchvision
from torchvision.models.detection import  FasterRCNN_ResNet50_FPN_V2_Weights


class FasterRCNN(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.model = None
        self.preprocessor = None
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'


    def load(self, model_path):
        self.preprocessor = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT.transforms()

        self.model = torch.load(model_path, map_location=torch.device(self.device))
        self.model.eval()
        

    def forward(self, img):

        img = torchvision.transforms.Resize(416, antialias=None)(img)

        img = [self.preprocessor(img).to(self.device)]

        return self.model(img)