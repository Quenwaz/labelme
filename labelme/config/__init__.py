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
import os,shutil,json

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
    
def yolo(targetDir, sourceImages, labelextension):
    if len(sourceImages) == 0:
        return 0
    
    targetImageDir= os.path.join(targetDir, "images")
    if not os.path.exists(targetImageDir):
        os.mkdir(targetImageDir)
    targetLabelDir= os.path.join(targetDir, "labels")
    if not os.path.exists(targetLabelDir):
        os.mkdir(targetLabelDir)
        
    classes_file = os.path.join(targetDir, "classes.txt")
    try:     
        label_list = []
        for idx, image_path in enumerate(sourceImages):
            target_basename = "{:04d}".format(idx)
            filepath, image_ext = os.path.splitext(image_path)
            label_file = filepath + labelextension
            
            lable_json_content = dict()
            with open(label_file, 'r', encoding="utf-8") as fp:
                lable_json_content = json.load(fp)
            
            image_width, image_height = lable_json_content["imageWidth"], lable_json_content["imageHeight"]
            shapes = lable_json_content["shapes"]
            label_describe = []
            for shape in shapes:
                label_name = shape["label"]
                label_index = len(label_list)
                if label_name in label_list:
                    label_index = label_list.index(label_name)
                else:
                    label_list.append(label_name)
                    
                min_point, max_point = shape["points"]
                width, height = abs(max_point[0] - min_point[0]),abs(max_point[1] - min_point[1])
                center_x, center_y = 0.5 * (max_point[0] + min_point[0]), 0.5 * (max_point[1] + min_point[1])
                label_describe.append("%d %f %f %f %f\n" %(label_index, center_x/image_width, center_y / image_height, width/image_width, height / image_height))
            
            target_label_file = os.path.join(targetLabelDir, "%s.txt" % (target_basename,))
            with open(target_label_file, 'w') as fp:
                fp.writelines(label_describe)
                
            shutil.copyfile(image_path, os.path.join(targetImageDir, "%s%s" % (target_basename, image_ext)))
        with open(classes_file, 'w') as fp:
            fp.writelines(["%d: %s\n" % (i, n) for i, n in enumerate(label_list)])
        return len(sourceImages)
    except Exception as e:
        shutil.rmtree(targetImageDir)
        shutil.rmtree(targetLabelDir)
    
    return 0
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
