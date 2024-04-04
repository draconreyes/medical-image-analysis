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
        file_path = os.path.join(folder_path, 'acquisition_1\deformable\correctedForPVE\htv1_4.nii')
        imagen_1 = nib.load(file_path)
        acquisition_1 = imagen_1.get_fdata()
        file_path = os.path.join(folder_path, 'acquisition_2\deformable\correctedForPVE\htv1_4.nii')
        imagen_2 = nib.load(file_path)
        acquisition_2 = imagen_2.get_fdata()
        file_path = os.path.join(folder_path, 'acquisition_3\deformable\correctedForPVE\htv1_4.nii')
        imagen_3 = nib.load(file_path)
        acquisition_3 = imagen_3.get_fdata()
        union_acqui_1_vs_acqui_2 = 0
        union_acqui_1_vs_acqui_3 = 0
        for i in range(acquisition_1.shape[0]):
            for j in range(acquisition_1.shape[1]):
                for k in range(acquisition_1.shape[2]):
                    if acquisition_1[i, j, k] == acquisition_2[i, j, k]:
                        union_acqui_1_vs_acqui_2 +=1
                    elif acquisition_1[i, j, k] == acquisition_3[i, j, k]:
                        union_acqui_1_vs_acqui_3 +=1
        results.append(
            {
                "Folder":folder_name,
                "DSC_acquisition_1_vs_acquisition_2":((2*union_acqui_1_vs_acqui_2)/(acquisition_1.size + acquisition_2.size)),
                "DSC_acquisition_1_vs_acquisition_3":((2*union_acqui_1_vs_acqui_3)/(acquisition_1.size + acquisition_3.size)),
                "SENS_acquisition_1_vs_acquisition_2":((union_acqui_1_vs_acqui_2)/((union_acqui_1_vs_acqui_2+(acquisition_1.size/acquisition_2.size)))),
                "SENS_acquisition_1_vs_acquisition_3":((union_acqui_1_vs_acqui_3)/((union_acqui_1_vs_acqui_3+(acquisition_1.size/acquisition_3.size)))),
                "PPV_acquisition_1_vs_acquisition_2":((union_acqui_1_vs_acqui_2)/(acquisition_2.size)),
                "PPV_acquisition_1_vs_acquisition_3":((union_acqui_1_vs_acqui_3)/(acquisition_3.size))
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
