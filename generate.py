import json
import re
from colormath import color_conversions
from colormath.color_objects import sRGBColor, XYZColor


def hex_to_unreal_color(value: str):
    color = color_conversions.convert_color(
        color=sRGBColor.new_from_rgb_hex(value),
        target_cs=XYZColor,
        target_illuminant="f7"
    )
    color = color.get_value_tuple()

    r, g, b = color[0], color[1], color[2]
    return f"R={r:.6f},G={g:.6f},B={b:.6f}"


def main():
    with open("colors.json", "r") as colors_file, open("template.json", "r") as template_file:
        themes = json.load(colors_file)
        template_lines = template_file.readlines()
        for theme_name, colors in themes.items():
            name = f"Catppuccin-{theme_name}"
            with open(f"dist/{name}.json", "w") as theme_file:
                for line in template_lines:
                    key = re.search("{.*}", line)
                    if key is not None:
                        key = key.group(0)[1:-1]
                        if key == "id":
                            identifier = colors["id"]
                            line = re.sub("{.*}", identifier, line)
                        elif key == "name":
                            line = re.sub("{.*}", name, line)
                        else:
                            color = hex_to_unreal_color(colors[key])
                            line = re.sub("{.*}", color, line)
                    theme_file.write(line)


if __name__ == "__main__":
    main()
