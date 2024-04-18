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
    try:
        folder_path = os.path.join(current_dir, base_dir, folder_name)
        print(f"Calculando carpeta:{folder_path}")
        file_path_acquisition_1 = os.path.join(folder_path, 'acquisition_1\deformable\correctedForPVE\htv1_4.nii')
        if os.path.exists(file_path_acquisition_1):
            imagen_1 = nib.load(file_path_acquisition_1)
            acquisition_1 = imagen_1.get_fdata()
            temporal_result = {}
            acquisition_2_exists = False
            acquisition_3_exists = False
            acquisition_2_exists
            file_path_acquisition_2 = os.path.join(folder_path, 'acquisition_2\deformable\correctedForPVE\htv1_4.nii')
            if os.path.exists(file_path_acquisition_2):
                imagen_2 = nib.load(file_path_acquisition_2)
                acquisition_2 = imagen_2.get_fdata()
                acquisition_2_exists = True
            file_path_acquisition_3 = os.path.join(folder_path, 'acquisition_3\deformable\correctedForPVE\htv1_4.nii')
            if os.path.exists(file_path_acquisition_3):
                imagen_3 = nib.load(file_path_acquisition_3)
                acquisition_3 = imagen_3.get_fdata()
                acquisition_3_exists = True
            inter_acqui_1_vs_acqui_2 = 0
            inter_acqui_1_vs_acqui_3 = 0
            for i in range(acquisition_1.shape[0]):
                for j in range(acquisition_1.shape[1]):
                    for k in range(acquisition_1.shape[2]):
                        if  acquisition_2_exists and acquisition_1[i, j, k] == acquisition_2[i, j, k]:
                            inter_acqui_1_vs_acqui_2 +=1
                        elif acquisition_3_exists and acquisition_1[i, j, k] == acquisition_3[i, j, k]:
                            inter_acqui_1_vs_acqui_3 +=1
            results.append(
                {
                    "Folder":folder_name,
                    "DSC_acquisition_1_vs_acquisition_2":((2*inter_acqui_1_vs_acqui_2)/(acquisition_1.size + acquisition_2.size)) if acquisition_2_exists else 0,
                    "DSC_acquisition_1_vs_acquisition_3":((2*inter_acqui_1_vs_acqui_3)/(acquisition_1.size + acquisition_3.size)) if acquisition_3_exists else 0,
                    "SENS_acquisition_1_vs_acquisition_2":((inter_acqui_1_vs_acqui_2)/((inter_acqui_1_vs_acqui_2+(acquisition_1.size/acquisition_2.size)))) if acquisition_2_exists else 0,
                    "SENS_acquisition_1_vs_acquisition_3":((inter_acqui_1_vs_acqui_3)/((inter_acqui_1_vs_acqui_3+(acquisition_1.size/acquisition_3.size)))) if acquisition_3_exists else 0,
                    "PPV_acquisition_1_vs_acquisition_2":((inter_acqui_1_vs_acqui_2)/(acquisition_2.size)) if acquisition_2_exists else 0,
                    "PPV_acquisition_1_vs_acquisition_3":((inter_acqui_1_vs_acqui_3)/(acquisition_3.size)) if acquisition_3_exists else 0
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
