@echo off
REM 在 CMD 中运行：
REM   cd /d E:\test\nlp_deberta_rex-uninlu_chinese-base\rex
REM   scripts\train_hier_cls_example.bat

REM 如果 conda activate 不生效，可改成绝对路径，例如：
REM set PYTHON_EXE=E:\Learning\envs\pro3\python.exe
if "%PYTHON_EXE%"=="" set PYTHON_EXE=python

if "%BERT_MODEL_DIR%"=="" set BERT_MODEL_DIR=../
if "%DATA_PATH%"=="" set DATA_PATH=data/hier_cls
if "%RUN_NAME%"=="" set RUN_NAME=hier_cls_exp1
if "%OUTPUT_DIR%"=="" set OUTPUT_DIR=../log
if "%LOAD_CHECKPOINT%"=="" set LOAD_CHECKPOINT=../

if "%LR%"=="" set LR=2e-5
if "%EPOCHS%"=="" set EPOCHS=10
if "%TRAIN_BS%"=="" set TRAIN_BS=8
if "%EVAL_BS%"=="" set EVAL_BS=8
if "%GRAD_ACC%"=="" set GRAD_ACC=2
if "%NEG_RATE%"=="" set NEG_RATE=1

set USE_LIBUV=0

%PYTHON_EXE% -c "import sys; print('[Info] sys.executable =', sys.executable)"

%PYTHON_EXE% main.py ^
  --bert_model_dir=%BERT_MODEL_DIR% ^
  --data_path=%DATA_PATH% ^
  --run_name=%RUN_NAME% ^
  --task_metrics=strict ^
  --do_train=True ^
  --do_eval=True ^
  --per_device_train_batch_size=%TRAIN_BS% ^
  --per_device_eval_batch_size=%EVAL_BS% ^
  --gradient_accumulation_steps=%GRAD_ACC% ^
  --num_train_epochs=%EPOCHS% ^
  --learning_rate=%LR% ^
  --lr_scheduler_type=linear ^
  --negative_sampling_rate=%NEG_RATE% ^
  --output_dir=%OUTPUT_DIR% ^
  --fp16 ^
  --remove_unused_columns=False ^
  --report_to=none ^
  --load_checkpoint=%LOAD_CHECKPOINT%
