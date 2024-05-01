import os
import nibabel as nib
import pandas as pd

# Directorio base donde se encuentran las carpetas NIFTIs
base_dir = 'NIFTIs'

# Obtener la ruta absoluta del directorio actual
current_dir = os.getcwd()

# Lista para almacenar los resultados
results = []

# Recorremos cada carpeta dentro del directorio base
for folder_name in os.listdir(os.path.join(current_dir, base_dir)):
    folder_path = os.path.join(current_dir, base_dir, folder_name)
    print(f"Calculando carpeta:{folder_path}")
    if os.path.isdir(folder_path):
        # Contadores para cada adquisición
        voxel_counts = {
            'acquisition_1': 0,
            'voxel_volume_1': 0.0,
            'total_voxel_volume_1':0.0,
            'acquisition_2': 0,
            'voxel_volume_2': 0.0,
            'total_voxel_volume_2':0.0,
            'acquisition_3': 0,
            'voxel_volume_3': 0.0,
            'total_voxel_volume_3':0.0,
        }
        
        # Recorremos las subcarpetas dentro de la carpeta actual
        for subfolder_name in os.listdir(folder_path):
            subfolder_path = os.path.join(folder_path, subfolder_name)
            if os.path.isdir(subfolder_path):
                # Nombre del archivo dentro de la subcarpeta
                file_path = os.path.join(subfolder_path, 'deformable\correctedForPVE\htv1_4.nii')
                
                # Cargar el archivo y contar los voxels
                if os.path.exists(file_path):
                    image = nib.load(file_path)
                    sx, sy, sz = image.header.get_zooms()
                    volume = sx * sy * sz
                    array = image.get_fdata()
                    contador = 0
                    for i in range(array.shape[0]):
                        for j in range(array.shape[1]):
                            for k in range(array.shape[2]):
                                if array[i, j, k] == 1:
                                    contador += 1
                    # Actualizar el contador correspondiente
                    acquisition_number = subfolder_name.split('_')[-1]
                    voxel_counts[f'acquisition_{acquisition_number}'] = contador
                    voxel_counts[f'voxel_volume_{acquisition_number}'] = volume
                    voxel_counts[f'total_voxel_volume_{acquisition_number}'] = volume * contador

        # Agregar los resultados a la lista
        results.append({'Folder Name': folder_name,
                        'Num Voxels in 1 acquisition_1': voxel_counts['acquisition_1'],
                        'Voxel Value in acquisition_1 ': voxel_counts['voxel_volume_1'],
                        'Total Voxel Value in 1 acquisition_1 ': voxel_counts['total_voxel_volume_1'],
                        'Num Voxels in 1 acquisition_2': voxel_counts['acquisition_2'],
                        'Voxel Value in acquisition_2 ': voxel_counts['voxel_volume_2'],
                        'Total Voxel Value in 1 acquisition_2 ': voxel_counts['total_voxel_volume_2'],
                        'Num Voxels in 1 acquisition_3': voxel_counts['acquisition_3'],
                        'Voxel Value in acquisition_3 ': voxel_counts['voxel_volume_3'],
                        'Total Voxel Value in 1 acquisition_3 ': voxel_counts['total_voxel_volume_3'],
                        })

# Crear DataFrame
df = pd.DataFrame(results)

# Exportar DataFrame a Excel
excel_file = 'resultados.xlsx'
df.to_excel(excel_file, index=False)

print(f"DataFrame exportado a {excel_file}")





