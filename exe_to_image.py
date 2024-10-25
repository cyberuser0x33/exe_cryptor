def embed_exe_in_jpg(jpg_path, exe_path, output_path):
    with open(jpg_path, 'rb') as jpg_file:
        jpg_data = jpg_file.read()
    end_marker = b'\xff\xd9'
    jpg_end = jpg_data.index(end_marker) + len(end_marker)

    with open(exe_path, 'rb') as exe_file:
        exe_data = exe_file.read()
    combined_data = jpg_data[:jpg_end] + exe_data

    with open(output_path, 'wb') as output_file:
        output_file.write(combined_data)


jpg_file = 'image.jpg'
exe_file = 'program.exe'
output_file = 'new_image.jpg'

embed_exe_in_jpg(jpg_file, exe_file, output_file)