import chaonanlib as cn
from torchvision.models import resnet50

model=resnet50()
input_size=(1,3,224,224)

macs,params=cn.evaluate.Opcount.ComputeOps(input_size,model)
print(macs)
print(params)
