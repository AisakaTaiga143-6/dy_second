# Copyright (c) Alibaba, Inc. and its affiliates.
import os
import torch
from typing import Union, Dict, Any

from transformers import AutoTokenizer, AutoModel, AutoConfig, set_seed

from modelscope.models.base import TorchModel
from modelscope.preprocessors.base import Preprocessor
from modelscope.pipelines.base import Model, Pipeline
from modelscope.utils.config import Config
from modelscope.pipelines.builder import PIPELINES
from modelscope.preprocessors.builder import PREPROCESSORS
from modelscope.models.builder import MODELS

from .rex.data_utils import data_loader, token_config
from .rex.arguments import get_args, DataArguments, UIEArguments
from .rex.model.model import RexModel
from .rex.Trainer.trainer import RexModelTrainer
from .rex.Trainer.utils import compute_metrics

@PIPELINES.register_module('rex-uninlu', module_name='nlp_deberta_rex-uninlu_chinese-base-pipe')
class RexUniNLUPipeline(Pipeline):

    def __init__(self, model, preprocessor=None, **kwargs):
        super().__init__(model=model, auto_collate=False)
        self.model, self.trainer = self.init_model(**kwargs)
    
    def init_model(self, **kwargs):
        self.model_dir = 'damo/nlp_deberta_rex-uninlu_chinese-base'
        data_args, training_args, model_args = get_args()
        training_args.bert_model_dir = self.model_dir
        training_args.load_checkpoint = self.model_dir
        # training_args.fp16 = False
        training_args.no_cuda = True
        tokenizer = AutoTokenizer.from_pretrained(training_args.bert_model_dir)
        tokenizer.add_special_tokens({
            "additional_special_tokens": [token_config.PREFIX_TOKEN, token_config.TYPE_TOKEN, token_config.CLASSIFY_TOKEN, token_config.MULTI_CLASSIFY_TOKEN]
        })
        config = AutoConfig.from_pretrained(training_args.bert_model_dir)

        model = RexModel(config, training_args, model_args)
        if training_args.no_cuda:
            model.load_state_dict(torch.load(os.path.join(training_args.load_checkpoint, 'pytorch_model.bin'), map_location=torch.device('cpu')), strict=False)
        else:
            model.load_state_dict(torch.load(os.path.join(training_args.load_checkpoint, 'pytorch_model.bin')), strict=False)


        uie_token_data_loader = data_loader.UIEDataLoader(
            data_args, 
            tokenizer, 
            data_args.data_path, 
            training_args.local_rank, 
            training_args.world_size,
            training_args.no_cuda)
        
        trainer = RexModelTrainer(model, training_args, uie_token_data_loader.get_collate_fn(),
            tokenizer=tokenizer,
            compute_metrics=compute_metrics
        )
        trainer.rex_dl = uie_token_data_loader
        trainer.data_args = data_args
        return model, trainer

    def forward(self, input, **forward_params):
        """ Provide default implementation using self.model and user can reimplement it
        """
        print(input)
        text = input
        print(forward_params)
        schema = forward_params.pop('schema')
        if type(schema) == str:
            schema = json.loads(schema)

        input_dict = {
            'text': text,
            'schema': schema
        }
        pred_info_list = self.trainer.prediction_step(self.model, input_dict, prediction_loss_only=False, do_pred=True)
        return {'output': pred_info_list}

    def preprocess(self, inputs, **preprocess_params) -> Dict[str, Any]:
        return inputs

    def postprocess(self, input, **kwargs) -> Dict[str, Any]:
        return input

    def _sanitize_parameters(self, **pipeline_parameters):
        return {},pipeline_parameters,{}


# # Tips: usr_config_path is the temporary save configuration location， after upload modelscope hub, it is the model_id
# usr_config_path = '/tmp/snapdown/'
# config = Config({
#     "framework": 'pytorch',
#     "task": 'rex-uninlu',
#     "pipeline": {"type": "nlp_deberta_rex-uninlu_chinese-base-pipe"},
#     "allow_remote": True
# })
# config.dump('/tmp/snapdown/' + 'configuration.json')

# if __name__ == "__main__":
#     from modelscope.models import Model
#     from modelscope.pipelines import pipeline
#     # model = Model.from_pretrained(usr_config_path)
#     text = "北大西洋议会春季会议26日在西班牙巴塞罗那闭幕。"
#     inference = pipeline('rex-uninlu', model='/tmp/snapdown')
#     output = inference(text, schema={"人物": None, "地理位置": None, "组织机构": None})
#     print(output)
