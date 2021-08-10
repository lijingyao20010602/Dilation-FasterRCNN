from detectron2.config import get_cfg
from detectron2.modeling.meta_arch import build_model
from detectron2.distiller_zoo import DistillKL, HintLoss, Attention, Similarity, Correlation, VIDLoss, RKDLoss

class Distill():
    def __init__(self, distill_cfg):
        self.opt = distill_cfg
        self.model_t = self.build_teacher_model()

    def build_teacher_model(self):
        '''构建教师模型'''
        teacher_cfg = get_cfg() 
        teacher_cfg.merge_from_file(self.opt.CFG_T)
        model_t = build_model(teacher_cfg)
        return model_t
        
    def compute_distill_loss(self, batched_inputs, logit_s): 
        '''计算蒸馏损失'''
        # 获取教师特征图
        logit_t = self.model_t.get_features(batched_inputs)  

        # ==========================蒸馏损失函数==========================      
        # kd 损失函数
        criterion_kd = HintLoss()

        # 对五层FPN的损失取平均
        loss_kd = 0
        for t,s in zip(logit_t.values(), logit_s.values()):
            loss_kd += criterion_kd(s, t)
        loss_kd = loss_kd/5 * self.opt.B

        distill_losses = {'loss_kd': loss_kd}

        return distill_losses
    


