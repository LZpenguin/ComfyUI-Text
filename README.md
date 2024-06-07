# ComfyUI-Text

## Install
1. Clone repo
```
cd /custom_nodes
git clone https://github.com/LZpenguin/ComfyUI-Text.git
```
1. Register folder_path

Edit  `/folder_paths.py`

Add follow code:
```
folder_names_and_paths["font"] = ([os.path.join(models_dir, "font")], [".ttf"])
```

## Example
[Test Workflow](./example/font_merge.json)

![](./example/image.png)