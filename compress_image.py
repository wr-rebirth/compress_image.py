from os.path import basename, getsize
from PIL import Image
import sys


def convert_size(size_in_byte: int) -> str:
    units = ("B", "KB", "MB", "GB")
    for unit in units:
        if size_in_byte < 1024:
            return f"{round(size_in_byte, 2)}{unit}"
        size_in_byte /= 1024
    return f"{round(size_in_byte, 2)}TB"


def compress_image(image_path: str) -> None:
    """快速压缩单个图片"""
    try:
        img = Image.open(image_path)
        before_size = getsize(image_path)
        if img.mode in ("RGBA", "LA"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")
        img.save(image_path, "JPEG", quality=85, optimize=True)
        after_size = getsize(image_path)
        print(
            f"  正在压缩 {basename(image_path)}: {convert_size(before_size)} -> {convert_size(after_size)}"
        )
    except Exception:
        print(f"  压缩 {basename(image_path)} 失败")
        pass


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("使用方法: python function.py <文件路径>")
        sys.exit(1)
    compress_image(sys.argv[1])
