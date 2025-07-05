from PIL import Image
import glob
import os
import sys

images = glob.glob('*.png')
if images == []:
    print("No images found. You have to use .png")
    sys.exit(-1)
pixels_width = int(input("Enter how many pixels should fit in a width of one block:"))
command = '' 
modifier = 10 / pixels_width
step = -2.0 * modifier
scale_x = round(0.8 * modifier,4)
scale_y = round(0.4 * modifier,4)
scale_z = 0.0

def split_image_columns(image_path):
    column_width = 20
    img = Image.open(image_path)
    width, height = img.size
    num_columns = width // column_width
    last_column_width = width % column_width
    
    columns = []
    for i in range(num_columns):
    # Calculate boundaries for full-width columns
        left = i * column_width
        right = left + column_width
        col = img.crop((left, 0, right, height))
        columns.append(col)
    
    # Add last column if it has remaining pixels
    if last_column_width > 0:
        left = num_columns * column_width
        right = left + last_column_width
        last_col = img.crop((left, 0, right, height))
        columns.append(last_col)    
    return tuple(columns)

# Get pixels hex code and column width
def get_image_data(image_column, step):
    width, height = image_column.size
    pixel_data = list(image_column.getdata())
    step += 0.1 * width
    image_width = width
    pixel_values = []
    for pixel in pixel_data:
        r, g, b, a = pixel
        hex_value = '#' + '{:02x}{:02x}{:02x}'.format(r, g, b)
        alpha_value = a
        pixel_values.append((hex_value, alpha_value))

    return image_width, pixel_values, step


def generate_text_display_command(symbols_colors, scale_x, scale_y, scale_z):
    text_part = []
    for symbol_color_pair in symbols_colors:
        symbol, color = symbol_color_pair.split('/')
        symbol = symbol.strip("\'")  # Remove single quotes from the symbol
        color = color.strip("\'")  # Remove single quotes from the color
        text_part.append('{{"text":"{}","color":"{}"}}'.format(symbol, color))
    
    text_part_str = ','.join(text_part)

    command = f"\nsummon minecraft:text_display ~ ~1 ~ {{line_width:{width*5},text:[{text_part_str}],background:0,transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[{round(step * modifier,4)}f,-0.3f,0f],scale:[{scale_x}f,{scale_y}f,{scale_z}f]}},Passengers:["
    command += f"{{id:\"minecraft:text_display\",line_width:{width*5},text:[{text_part_str}],background:0,transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[{round(step * modifier + 0.02 * modifier,4)}f,-0.3f,0f],scale:[{scale_x}f,{scale_y}f,{scale_z}f]}}}},"
    command += f"{{id:\"minecraft:text_display\",line_width:{width*5},text:[{text_part_str}],background:0,transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[{round(step * modifier + 0.02 * modifier,4)}f,{round(-0.3 - 0.02 * modifier,4)}f,0f],scale:[{scale_x}f,{scale_y}f,{scale_z}f]}}}},"
    command += f"{{id:\"minecraft:text_display\",line_width:{width*5},text:[{text_part_str}],background:0,transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[{round(step * modifier,4)}f,{round(-0.3 - 0.02 * modifier,4)}f,0f],scale:[{scale_x}f,{scale_y}f,{scale_z}f]}}}}"
    return command

for i in images:
    image_name = i.rstrip('.png')
    split_images = split_image_columns(i)
    for column in split_images:
        width, pixels, step = get_image_data(column, step)
        if width < 20:
            step += (20 - width) * 0.1 * 0.5
        symbols_colors = []
        for x, pixel in enumerate(pixels):
            hex_value, alpha_value = pixel
            if alpha_value > 0:
                symbols_colors.append('\'▌\''+ '/' + '\'' + hex_value + '\'')
            else:
                symbols_colors.append('\'▌\'' + '/' + "'#4a4e54'")
        command += generate_text_display_command(symbols_colors, scale_x, scale_y, scale_z)
        command += f"],Tags:[\'{image_name.lstrip('/')}\']" + "}"
    path = f'output/ItBD/data/itbd/function/{image_name}.mcfunction'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding = 'utf-8') as file:
        command += f'\nexecute as @e[tag={image_name.lstrip('/')}] at @s run ride @s mount @e[tag={image_name.lstrip('/')},limit=1,distance=..5]'
        file.write(command)
        command = ''
        step = -2.0 * modifier