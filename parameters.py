import os
import nibabel as nib
import pandas as pd
from utilities.main import (
    dice_coef,
    PPV_coef,
    Sens_coef,
    volumeContour
)
import SimpleITK as sitk
from skimage import metrics

# Directorio base donde se encuentran las carpetas NIFTIs
base_dir = 'NIFTIs'

# Obtener la ruta absoluta del directorio actual
current_dir = os.getcwd()

# Lista para almacenar los resultados
results = []

# Recorremos cada carpeta dentro del directorio base
for folder_name in os.listdir(os.path.join(current_dir, base_dir)):
    try:
        folder_path = os.path.join(current_dir, base_dir, folder_name)
        print(f"Calculando carpeta:{folder_path}")
        acquisition_2_exists = False
        acquisition_3_exists = False
        file_path_acquisition_1 = os.path.join(folder_path, 'acquisition_1\deformable\correctedForPVE\htv10mmHg.nii')
        if os.path.exists(file_path_acquisition_1):
            imagen_1 = sitk.ReadImage(file_path_acquisition_1,imageIO="NiftiImageIO")
            print(f"paso imagen 1")
            imagen_1 = sitk.GetArrayFromImage(imagen_1)
            # imagen_1 = nib.load(file_path_acquisition_1)
            file_path_acquisition_2 = os.path.join(folder_path, 'acquisition_2\deformable\correctedForPVE\htv10mmHg.nii')
            if os.path.exists(file_path_acquisition_2):
                acquisition_2_exists = True
                imagen_2 = sitk.ReadImage(file_path_acquisition_2,imageIO="NiftiImageIO")
                imagen_2 = sitk.GetArrayFromImage(imagen_2)
                #imagen_2 = nib.load(file_path_acquisition_2)
                
            file_path_acquisition_3 = os.path.join(folder_path, 'acquisition_3\deformable\correctedForPVE\htv10mmHg.nii')
            if os.path.exists(file_path_acquisition_3):
                acquisition_3_exists = True
                imagen_3 = sitk.ReadImage(file_path_acquisition_3,imageIO="NiftiImageIO")
                imagen_3 = sitk.GetArrayFromImage(imagen_3)
                # imagen_3 = nib.load(file_path_acquisition_3)
                
            results.append(
                {
                    "Folder":folder_name,
                    "DSC_acquisition_1_vs_acquisition_2":(dice_coef(imagen_1,imagen_2)) if acquisition_2_exists else 0,
                    "DSC_acquisition_1_vs_acquisition_3":(dice_coef(imagen_1,imagen_3)) if acquisition_3_exists else 0,
                    "SENS_acquisition_1_vs_acquisition_2":(Sens_coef(imagen_1,imagen_2)) if acquisition_2_exists else 0,
                    "SENS_acquisition_1_vs_acquisition_3":(Sens_coef(imagen_1,imagen_3)) if acquisition_3_exists else 0,
                    "PPV_acquisition_1_vs_acquisition_2":(PPV_coef(imagen_1, imagen_2)) if acquisition_2_exists else 0,
                    "PPV_acquisition_1_vs_acquisition_3":(PPV_coef(imagen_1, imagen_3)) if acquisition_3_exists else 0
                }
            )
        else:
            results.append(
                {
                    "Folder":folder_name,
                    "DSC_acquisition_1_vs_acquisition_2": 0,
                    "DSC_acquisition_1_vs_acquisition_3": 0,
                    "SENS_acquisition_1_vs_acquisition_2": 0,
                    "SENS_acquisition_1_vs_acquisition_3": 0,
                    "PPV_acquisition_1_vs_acquisition_2": 0,
                    "PPV_acquisition_1_vs_acquisition_3": 0
                }
            )

    except Exception as ex:
        print(ex)

# Crear DataFrame
df = pd.DataFrame(results)

# Exportar DataFrame a Excel
excel_file = 'parameters_result.xlsx'
df.to_excel(excel_file, index=False)

print(f"DataFrame exportado a {excel_file}")
