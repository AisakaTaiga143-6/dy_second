import argparse
import io
import logging
import os
import shutil
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
logging.getLogger("modelscope").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("modelscope").propagate = False
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["MODELSCOPE_LOG_LEVEL"] = "40"

# Ensure custom rex-uninlu pipeline is registered for local inference
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
import ms_wrapper


def main():
    parser = argparse.ArgumentParser()
    default_model_dir = str((Path(__file__).resolve().parents[2] / "log" / "hier_cls_exp1").resolve())
    parser.add_argument("--model_dir", default=default_model_dir, help="finetuned model directory")
    args = parser.parse_args()

    model_dir = str(Path(args.model_dir).resolve())
    if not os.path.exists(model_dir):
        raise FileNotFoundError(f"model_dir does not exist: {model_dir}")

    cfg_path = os.path.join(model_dir, 'configuration.json')
    if not os.path.exists(cfg_path):
        repo_cfg = os.path.join(str(REPO_ROOT), 'configuration.json')
        if os.path.exists(repo_cfg):
            shutil.copyfile(repo_cfg, cfg_path)
        else:
            raise FileNotFoundError(f"configuration.json not found in model_dir ({model_dir}) or repo root ({repo_cfg})")

    semantic_cls = ms_wrapper.RexUniNLUPipeline(model=model_dir, base_model_dir=str(REPO_ROOT))

    schema = {
        "学业困扰": {
            "拖延": None,
            "学习动力不足": None,
            "成绩焦虑": None
        },
        "生涯发展困扰": {
            "就业焦虑": None,
            "考研考公压力": None
        },
        "情绪困扰": {
            "自卑": None,
            "孤独": None
        },
        "人际困扰": {
            "社交矛盾": None,
            "不适应新环境": None,
            "恋爱问题": None
        },
        "经济压力": {
            "经济压力": None
        }
    }

    user_input = input("用户输入：").strip()
    if not user_input:
        print("当前未检测到明显的心理困扰")
        return

    labels_set = set()
    hierarchy_set = set()
    _stdout = sys.stdout
    sys.stdout = io.StringIO()

    full_input = f"[CLASSIFY]{user_input}"
    result = semantic_cls(input=full_input, schema=schema)
    if result.get('output') and len(result['output']) > 0:
        for item in result['output']:
            if not item or not isinstance(item, list):
                continue
            if len(item) >= 2 and isinstance(item[0], dict) and isinstance(item[1], dict):
                l1 = item[0].get('type')
                l2 = item[1].get('type')
                if l2:
                    labels_set.add(l2)
                if l1 and l2:
                    hierarchy_set.add(f"{l1} -> {l2}")
            elif len(item) >= 1 and isinstance(item[0], dict):
                l1 = item[0].get('type')
                if l1:
                    labels_set.add(l1)

    sys.stdout = _stdout

    if labels_set:
        if hierarchy_set:
            print(f"用户当前的心理困扰（二级）为：{', '.join(sorted(labels_set))}")
            print(f"层级路径：{'; '.join(sorted(hierarchy_set))}")
        else:
            print(f"用户当前的心理困扰为：{', '.join(sorted(labels_set))}")
    else:
        print("当前未检测到明显的心理困扰")


if __name__ == "__main__":
    main()
