def extract_exe_from_jpg(combined_path, output_exe_path):
    with open (combined_path, 'rb') as combined_file:
        combined_data = combined_file.read()

    end_marker = b'\xff\xd9'

    jpg_end = combined_data.index(end_marker) + len(end_marker)

    exe_data = combined_data[jpg_end:]

    with open(output_exe_path, 'wb') as outbut_exe_file:
        outbut_exe_file.write(exe_data)

combined_file = 'new_image.jpg'
output_exe = 'output.exe'

extract_exe_from_jpg(combined_file, output_exe)