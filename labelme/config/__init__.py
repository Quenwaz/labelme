import os.path as osp
import shutil

import yaml

from labelme.logger import logger

here = osp.dirname(osp.abspath(__file__))


def update_dict(target_dict, new_dict, validate_item=None):
    for key, value in new_dict.items():
        if validate_item:
            validate_item(key, value)
        if key not in target_dict:
            logger.warn("Skipping unexpected key in config: {}".format(key))
            continue
        if isinstance(target_dict[key], dict) and isinstance(value, dict):
            update_dict(target_dict[key], value, validate_item=validate_item)
        else:
            target_dict[key] = value


# -----------------------------------------------------------------------------


def get_default_config():
    config_file = osp.join(here, "default_config.yaml")
    with open(config_file) as f:
        config = yaml.safe_load(f)

    # save default config to ~/.labelmerc
    user_config_file = osp.join(osp.abspath(osp.curdir) , ".labelmerc") # osp.join(osp.expanduser("~"), ".labelmerc")
    if not osp.exists(user_config_file):
        try:
            shutil.copy(config_file, user_config_file)
        except Exception:
            logger.warn("Failed to save config: {}".format(user_config_file))

    return config


def validate_config_item(key, value):
    if key == "validate_label" and value not in [None, "exact"]:
        raise ValueError(
            "Unexpected value for config key 'validate_label': {}".format(value)
        )
    if key == "shape_color" and value not in [None, "auto", "manual"]:
        raise ValueError(
            "Unexpected value for config key 'shape_color': {}".format(value)
        )
    if key == "labels" and value is not None and len(value) != len(set(value)):
        raise ValueError(
            "Duplicates are detected for config key 'labels': {}".format(value)
        )


EXPORT_MODULE="export"

def dump_sample_export_script():
    sample_script_file = "%s.py" %(EXPORT_MODULE)
    if osp.exists(sample_script_file):
        return
    
    with open(sample_script_file, "w") as fp:
        fp.write('''
import os,shutil 

def sample(targetDir, sourceImages, labelextension):
    """Export the current label format to your desired label format

    Args:
        targetDir (str): export directory
        sourceImages (list): list of labeled pictures
        labelextension (str): current annotation file suffix name

    Returns:
        int: return the number of exports
    """
    for idx, image_path in enumerate(sourceImages):
        
        target_basename = "{:04d}".format(idx)
        filepath, image_ext = os.path.splitext(image_path)
        label_file = filepath + labelextension
        
        shutil.copyfile(image_path,  os.path.join(targetDir, "%s%s" % (target_basename, image_ext)))
        shutil.copyfile(label_file,  os.path.join(targetDir, "%s%s" % (target_basename, labelextension)))

    return len(sourceImages)
 ''')
        

def get_config(config_file_or_yaml=None, config_from_args=None):
    # 1. default config
    config = get_default_config()

    # 2. specified as file or yaml
    if config_file_or_yaml is not None:
        config_from_yaml = yaml.safe_load(config_file_or_yaml)
        if not isinstance(config_from_yaml, dict):
            with open(config_from_yaml) as f:
                logger.info("Loading config file from: {}".format(config_from_yaml))
                config_from_yaml = yaml.safe_load(f)
        update_dict(config, config_from_yaml, validate_item=validate_config_item)

    # 3. command line argument or specified config file
    if config_from_args is not None:
        update_dict(config, config_from_args, validate_item=validate_config_item)

    # 4. support export, export sample modules
    dump_sample_export_script()
    
    return config
