from detectron2.config import get_cfg
from detectron2.modeling.meta_arch import build_model
from detectron2.distiller_zoo import HintLoss, Attention, Similarity, NSTLoss, RKDLoss, PKT
from detectron2.checkpoint import DetectionCheckpointer
import torch

class Distill():
    def __init__(self, distill_cfg):
        self.opt = distill_cfg
        self.model_t = self.build_teacher_model()

    def build_teacher_model(self):
        '''构建教师模型'''
        # 模型创建
        teacher_cfg = get_cfg() 
        teacher_cfg.merge_from_file(self.opt.CFG_T)
        teacher_cfg['student_identity'] = False
        model_t = build_model(teacher_cfg)
        # 参数加载
        DetectionCheckpointer(model_t).resume_or_load(self.opt.PATH_T, resume=False)
        return model_t
        
    def compute_distill_loss(self, batched_inputs, logit_s): 
        '''计算蒸馏损失'''
        
        # 获取教师特征图
        with torch.no_grad():
            logit_t = self.model_t.get_features(batched_inputs)  

        # ==========================蒸馏损失函数==========================      
        # kd 损失函数
        if self.opt.DISTILL == 'hint':
            criterion_kd = HintLoss()
        elif self.opt.DISTILL == 'attention':
            criterion_kd = Attention()
        elif self.opt.DISTILL == 'nst':
            criterion_kd = NSTLoss()
        elif self.opt.DISTILL == 'similarity':
            criterion_kd = Similarity()
        elif self.opt.DISTILL == 'rkd':
            criterion_kd = RKDLoss()
        elif self.opt.DISTILL == 'pkt':
            criterion_kd = PKT()
        elif self.opt.DISTILL == 'kdsvd':
            criterion_kd = KDSVD()
        else:
            raise NotImplementedError(self.opt.DISTILL)

        # 对五层FPN的损失取平均
        loss_kd = 0
        for t,s in zip(logit_t.values(), logit_s.values()):
            loss_kd += criterion_kd(s, t.detach())
            
        loss_kd = loss_kd/5 * self.opt.B

        distill_losses = {'loss_kd': loss_kd}

        return distill_losses



