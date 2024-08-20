<h1 align="center">
  <img src="labelme/icons/icon.png"><br/>labelme
</h1>

<h4 align="center">
  用 Python 进行图像多边形注释
</h4>

<div align="center">
  <a href="https://pypi.python.org/pypi/labelme"><img src="https://img.shields.io/pypi/v/labelme.svg"></a>
  <a href="https://pypi.org/project/labelme"><img src="https://img.shields.io/pypi/pyversions/labelme.svg"></a>
  <a href="https://github.com/Quenwaz/labelme/actions"><img src="https://github.com/Quenwaz/labelme/workflows/ci/badge.svg?branch=main&event=push"></a>
</div>

<div align="center">
  <a href="#入门指南"><b>入门指南</b></a>
  | <a href="#安装"><b>安装</b></a>
  | <a href="#如何使用"><b>如何使用</b></a>
  | <a href="#实例"><b>用例</b></a>
  | <a href="https://x.com/labelmeai"><b>博客</b></a>
</div>

<br/>

<div align="center">
  <img src="examples/instance_segmentation/.readme/annotation.jpg" width="70%">
</div>

## 说明

Labelme 是一款图形图像注释工具，其灵感来自 <http://labelme.csail.mit.edu>。 
它用 Python 编写，图形界面使用 Qt。

<img src="examples/instance_segmentation/data_dataset_voc/JPEGImages/2011_000006.jpg" width="19%" /> <img src="examples/instance_segmentation/data_dataset_voc/SegmentationClass/2011_000006.png" width="19%" /> <img src="examples/instance_segmentation/data_dataset_voc/SegmentationClassVisualization/2011_000006.jpg" width="19%" /> <img src="examples/instance_segmentation/data_dataset_voc/SegmentationObject/2011_000006.png" width="19%" /> <img src="examples/instance_segmentation/data_dataset_voc/SegmentationObjectVisualization/2011_000006.jpg" width="19%" />  
<i>VOC 数据集实例分割示例。</i>

<img src="examples/semantic_segmentation/.readme/annotation.jpg" width="30%" /> <img src="examples/bbox_detection/.readme/annotation.jpg" width="30%" /> <img src="examples/classification/.readme/annotation_cat.jpg" width="35%" />  
<i>其他示例（语义分割、Bbox 检测和分类）。</i>

<img src="https://user-images.githubusercontent.com/4310419/47907116-85667800-de82-11e8-83d0-b9f4eb33268f.gif" width="30%" /> <img src="https://user-images.githubusercontent.com/4310419/47922172-57972880-deae-11e8-84f8-e4324a7c856a.gif" width="30%" /> <img src="https://user-images.githubusercontent.com/14256482/46932075-92145f00-d080-11e8-8d09-2162070ae57c.png" width="32%" />  
<i>各种基元（多边形、矩形、圆、线和点）。</i>


## 特点

- [x] 多边形、矩形、圆形、直线和点的图像注释。([教程](examples/tutorial))
- [x] 用于分类和清理的图像标记注释。 ([#166](https://github.com/wkentaro/labelme/pull/166))
- [x] 视频注释。 ([视频标注](examples/video_annotation))
- [x] 图形用户界面定制（预定义标签/标志、自动保存、标签验证等）。 ([#144](https://github.com/wkentaro/labelme/pull/144))
- [x] 导出 VOC 格式数据集，用于语义/实例分割。 ([语义分割](examples/semantic_segmentation), [实例分割](examples/instance_segmentation))
- [x] 导出 COCO 格式数据集，用于实例分割。([实例分割](examples/instance_segmentation))

以下为作者新增功能：
- [x] 侧边栏支持多级目录， 且可显示标记数目
- [x] 支持导出特定格式标签，会在exe所在目录生成export.py支持扩展， 编写自己的导出模块， 然后在.labelmerc的export中添加导出名称， 该名称与export.py中的方法名一致。

## 入门指南

如果您是 Labelme 的新用户，您可以使用 [Labelme 入门指南](https://labelme.gumroad.com/l/starter-guide) (免费) 开始学习，其中包含以下内容：

- **适用于所有平台的安装指南**： 适用于所有平台：Windows、macOS 和 Linux 💻
- **分步教程**：从注释到编辑、导出以及与其他程序整合 📕
- **宝贵资源汇编**，供进一步探索 🔗.


## 安装

有以下选项

- 与平台无关的安装： [Anaconda](#anaconda)
- 特定平台安装： [Ubuntu](#ubuntu), [macOS](#macos), [Windows](#windows)
- 从 [release section](https://github.com/wkentaro/labelme/releases) 预编译二进制文件

### Anaconda

您需要安装 [Anaconda](https://www.continuum.io/downloads)，然后运行以下程序：

```bash
# python3
conda create --name=labelme python=3
source activate labelme
# conda install -c conda-forge pyside2
# conda install pyqt
# pip install pyqt5  # pyqt5 can be installed via pip on python3
pip install labelme
# or you can install everything by conda command
# conda install labelme -c conda-forge
```

### Ubuntu

```bash
sudo apt-get install labelme

# or
sudo pip3 install labelme

# or install standalone executable from:
# https://github.com/wkentaro/labelme/releases
```

### macOS

```bash
brew install pyqt  # maybe pyqt5
pip install labelme

# or
brew install wkentaro/labelme/labelme  # command line interface
# brew install --cask wkentaro/labelme/labelme  # app

# or install standalone executable/app from:
# https://github.com/wkentaro/labelme/releases
```

### Windows

安装 [Anaconda](https://www.continuum.io/downloads)，然后在 Anaconda 提示符下运行：

```bash
conda create --name=labelme python=3
conda activate labelme
pip install labelme

# or install standalone executable/app from:
# https://github.com/wkentaro/labelme/releases
```


## 如何使用

运行 `labelme --help` 了解详情。 
注释保存为 [JSON](http://www.json.org/) 文件。

```bash
labelme  # just open gui

# tutorial (single image example)
cd examples/tutorial
labelme apc2016_obj3.jpg  # specify image file
labelme apc2016_obj3.jpg -O apc2016_obj3.json  # close window after the save
labelme apc2016_obj3.jpg --nodata  # not include image data but relative image path in JSON file
labelme apc2016_obj3.jpg \
  --labels highland_6539_self_stick_notes,mead_index_cards,kong_air_dog_squeakair_tennis_ball  # specify label list

# semantic segmentation example
cd examples/semantic_segmentation
labelme data_annotated/  # Open directory to annotate all images in it
labelme data_annotated/ --labels labels.txt  # specify label list with a file
```

### 命令行参数
- `--output` 指定注释将被写入的位置。如果位置以 .json 结尾，则单个注释将被写入该文件。如果指定的位置以 .json 结尾，则只能注释一幅图像。如果位置不是以 .json 结尾，程序会认为这是一个目录。注释将存储在该目录中，名称与注释的图像相对应。
- 第一次运行 labelme 时，程序会在 `~/.labelmerc` 中创建一个配置文件。你可以编辑这个文件，修改后的内容将在下次启动 labelme 时应用。如果你想使用其他位置的配置文件，可以用`--config`标记指定该文件。
- 如果不使用"--nosortlabels "标志，程序将按字母顺序列出标签。使用该标志运行程序时，程序将按提供的顺序显示标签。
- 标记会分配给整个图像。[示例]（示例/分类）
- 标签分配给单个多边形。[示例]（示例/方框检测）

### 常见问题

- **如何将 JSON 文件转换为 numpy 数组？** 参见 [示例/教程](examples/tutorial#convert-to-dataset)。
- **如何加载 PNG 标签文件？** 请参见 [例子/教程]（examples/tutorial#how-to-load-label-png-file）。
- **如何获取语义分割注释？** 参见 [示例/语义分割](examples/semantic_segmentation)。
- **如何获取实例分割的注释？** 请参见 [例子/实例分割](examples/instance_segmentation)。


## 实例

* [图像分类](examples/classification)
* [边界框检测](examples/bbox_detection)
* [语义分割](examples/semantic_segmentation)
* [实例分割](examples/instance_segmentation)
* [视频标注](examples/video_annotation)

## 如何开发

```bash
git clone https://github.com/wkentaro/labelme.git
cd labelme

# Install anaconda3 and labelme
curl -L https://github.com/wkentaro/dotfiles/raw/main/local/bin/install_anaconda3.sh | bash -s .
source .anaconda3/bin/activate
pip install -e .
```


### 如何构建独立可执行文件

下面介绍如何在 macOS、Linux 和 Windows 上构建独立可执行文件。 

```bash
# Setup conda
conda create --name labelme python=3.9
conda activate labelme

# Build the standalone executable
pip install .
pip install 'matplotlib<3.3'
pip install pyinstaller
pyinstaller labelme.spec
dist/labelme --version
```


#### 如何贡献

确保以下测试在你的环境中通过。 
更多详情请参见 `.github/workflows/ci.yml`。

```bash
pip install -r requirements-dev.txt

ruff format --check  # `ruff format` to auto-fix
ruff check  # `ruff check --fix` to auto-fix
MPLBACKEND='agg' pytest -vsx tests/
```


## 鸣谢

本 repo 是 [labelmeai/labelme](https://github.com/labelmeai/labelme) 的分叉。
