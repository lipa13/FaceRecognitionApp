"""
@author: JiXuan Xu, Jun Wang
@date: 20201019
@contact: jun21wangustc@gmail.com 
"""
import logging.config
#logging.config.fileConfig("config/logging.conf")
logger = logging.getLogger('sdk')

import torch

#from core.model_loader.BaseModelLoader import BaseModelLoader

#from ..BaseModelLoader import BaseModelLoader

from face_sdk.core.model_loader.BaseModelLoader import BaseModelLoader

class FaceDetModelLoader(BaseModelLoader):
    def __init__(self, model_path, model_category, model_name, meta_file='model_meta.json'):
        logger.info('Start to analyze the face detection model, model path: %s, model category: %s，model name: %s' %
                    (model_path, model_category, model_name))
        super().__init__(model_path, model_category, model_name, meta_file)
        self.cfg['min_sizes'] = self.meta_conf['min_sizes']
        self.cfg['steps'] = self.meta_conf['steps']
        self.cfg['variance'] = self.meta_conf['variance']
        self.cfg['in_channel'] = self.meta_conf['in_channel']
        self.cfg['out_channel'] = self.meta_conf['out_channel']
        self.cfg['confidence_threshold'] = self.meta_conf['confidence_threshold']
        
    def load_model(self):
        try:
            # model = torch.load(self.cfg['model_file_path'])
            
            #device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            #model = torch.load(self.cfg['model_file_path'], map_location=device)

            device = torch.device("cpu")
            model = torch.load(
                self.cfg['model_file_path'],
                map_location=device,
                weights_only=False  # allow loading full model if trusted
            )
        except Exception as e:
            logger.error('The model failed to load, please check the model path: %s!'
                         % self.cfg['model_file_path'])
            raise e
        else:
            logger.info('Successfully loaded the face detection model!')
            # return model, self.cfg
            return model.to(device), self.cfg
